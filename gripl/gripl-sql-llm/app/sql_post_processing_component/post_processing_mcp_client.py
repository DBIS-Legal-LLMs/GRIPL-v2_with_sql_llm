from mcp import ClientSession
from mcp.client.sse import sse_client
import traceback
from app.bpmn_data_pre_processor_component.bpmn_data_pre_processor import BPMNDataPreProcessor
from app.reranker_component.reranker import Reranker
from typing import TYPE_CHECKING
import json
from app.find_intention_component.schemas import IntentionAnswer

from pydantic_core._pydantic_core import ValidationError

if TYPE_CHECKING:
    from .sql_post_processing import SQLPostProcessing
from dotenv import load_dotenv
import os

load_dotenv()



class PostProcessingMcpClient:

    def __init__(self):
        self.max_iteration = 3
        self.bpmn_data_pre_processor = BPMNDataPreProcessor()
        self.server_url = os.getenv("MCP_SERVER_URL", "")

    async def get_mcp_client_answer(self,
                                    db_schema: str,
                                    activity_field: str,
                                    generated_query: str,
                                    error_message: str,
                                    intentions: list[str],
                                    reasons_of_intentions: list[str],
                                    sql_post_processing_component: "SQLPostProcessing"
                                    ):

        try:

            async with sse_client(self.server_url) as (reader, writer):
                async with ClientSession(reader, writer) as session:
                    await session.initialize()

                    tools_result = await session.list_tools()

                    mcp_tools = tools_result.tools

                    current_intention = intentions[0]

                    current_query = generated_query

                    current_reasons_list = reasons_of_intentions

                    groq_tools = self.convert_mcp_tool_list_to_groq_schema_tool_list(mcp_tools)

                    verification_system_prompt = sql_post_processing_component.prompt_management.fill_prompt(
                        sql_post_processing_component.verification_system_prompt_path,
                    )

                    messages = [
                        {"role": "system",
                         "content": verification_system_prompt
                         },
                    ]

                    for i in range(1, self.max_iteration + 1):

                        try:
                            tool_result = await session.call_tool("get_all_intentions", {})

                            if hasattr(tool_result, 'structuredContent') and tool_result.structuredContent:
                                intentions_list = tool_result.structuredContent.get('result', [])
                            else:
                                intentions_list = [item.text for item in tool_result.content if item.type == 'text']

                        except ValidationError:
                            valid_intentions = ["Collection", "Storage", "Usage", "Transferal", "Modification", "Deletion", "Access"]
                            messages.append({
                                "role": "user",
                                "content": f"Their was an error in getting all intentions: only values from {','.join(valid_intentions)}",
                            })
                            continue
                        except Exception as e:
                            messages.append({
                                "role": "user",
                                "content": f"There was an error in getting all intentions: {traceback.format_exc()}",
                            })
                            continue

                        messages.append({
                            "role": "user",
                            "content": f"All available intentions: {json.dumps(intentions_list)}"
                        })

                        try:

                            validated = IntentionAnswer(
                                intents=[intention]
                            )

                            reason_of_intention_answer = await session.call_tool(
                                "get_all_reasons_of_category",
                                {"category_name": current_intention}
                            )

                            if hasattr(reason_of_intention_answer, 'structuredContent') and reason_of_intention_answer.structuredContent:
                                reasons_list = reason_of_intention_answer.structuredContent.get('result', [])
                            else:
                                reasons_list = [item.text for item in reason_of_intention_answer.content if item.type == 'text']

                        except ValidationError:
                            valid_intentions = ["Collection", "Storage", "Usage", "Transferal", "Modification",
                                                "Deletion", "Access"]
                            messages.append({
                                "role": "user",
                                "content": f"Their was an error in getting all reasons of one intention "
                                           f"becaused used intention didnt exists: only intentions from {','.join(valid_intentions)}",
                            })
                            continue
                        except Exception as e:
                            messages.append({
                                "role": "user",
                                "content": f"Their was an error in getting all reasons of one intention: {traceback.format_exc()}."
                            })
                            continue

                        messages.append({
                            "role": "user",
                            "content": f"The available reasons of the intention: {json.dumps(reasons_list)}"
                        })

                        verification_user_prompt = sql_post_processing_component.prompt_management.fill_prompt(
                            sql_post_processing_component.verification_user_prompt_path,
                            activity_field=activity_field,
                            intention=current_intention,
                            generated_query=current_query,
                            reasons_of_intentions=current_reasons_list,
                            db_schema=db_schema,
                        )

                        messages.append({
                            "role": "user",
                            "content": verification_user_prompt
                        })

                        result = sql_post_processing_component.verification_llm_handler.get_answer_with_fallback(
                            messages
                        )

                        sql_post_processing_component.logging_component.log(
                            str(messages),
                            verification_system_prompt,
                            result,
                        )

                        if (
                                result.intention_status == "unchanged"
                                and result.reason_status == "unchanged"
                        ):
                            return result.final_query

                        intention = result.intention

                        messages.append({
                            "role": "user",
                            "content": (
                                "The previous validation changed the intention or reason. "
                                "Validate the corrected query again.\n\n"
                                f"Current intention: {result.intention}\n"
                                f"Current reason: {result.reason}\n"
                                f"Current SQL query:\n{result.final_query}"
                            ),
                        })

                        current_intention = result.intention
                        current_reasons_list = result.reason
                        current_query = result.final_query


                    final_query =  sql_post_processing_component.llm_handler.get_answer_with_fallback(
                        messages
                    ).final_query

                    sql_post_processing_component.logging_component.log(
                        str(messages),
                        verification_system_prompt,
                        final_query,
                    )
                    return final_query

        except Exception as e:
            print("error in mcp client")
            print(traceback.format_exc())

    def convert_mcp_tool_list_to_groq_schema_tool_list(self, mcp_tools: list):
        groq_tools = []
        for tool in mcp_tools:
            params = tool.inputSchema.copy()

            params.pop('title', None)
            params.pop('description', None)

            if 'type' not in params or params['type'] != 'object':
                params['type'] = 'object'

            properties = params.get('properties', {})
            if not isinstance(properties, dict):
                properties = {}
            for prop_name, prop_schema in list(properties.items()):
                if not isinstance(prop_schema, dict):
                    properties[prop_name] = {"type": "string"}
                prop_schema.pop('title', None)
                if 'description' not in prop_schema:
                    prop_schema['description'] = prop_name.replace('_', ' ')
                if 'type' not in prop_schema:
                    prop_schema['type'] = 'string'
            params['properties'] = properties

            if 'required' not in params and properties:
                params['required'] = list(properties.keys())

            groq_tools.append({
                "type": "function",
                "function": {
                    "name": tool.name,
                    "description": tool.description or "",
                    "parameters": params
                }
            })
        return groq_tools
