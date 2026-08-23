from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
import traceback
from typing import TYPE_CHECKING
import json

if TYPE_CHECKING:
    from .sql_post_processing import SQLPostProcessing

class PostProcessingMcpClient:

    def __init__(self):
        self.max_iteration = 3

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
            server_params = StdioServerParameters(
                command="python",
                args=[
                    "-m",
                    "app.sql_post_processing_component.post_processing_mcp_server"
                ],
            )

            async with stdio_client(server_params) as (reader, writer):
                async with ClientSession(reader, writer) as session:
                    await session.initialize()

                    user_prompt = sql_post_processing_component.prompt_management.fill_prompt(
                        sql_post_processing_component.user_prompt_path,
                        activity_field=activity_field,
                        db_schema=db_schema,
                        generated_query=generated_query,
                        error_message=error_message,
                        intent=",".join(intentions),
                        reasons_of_intentions=",".join(reasons_of_intentions),
                    )

                    system_prompt = sql_post_processing_component.prompt_management.fill_prompt(
                        sql_post_processing_component.system_prompt_path,
                    )

                    first_processed_query =  sql_post_processing_component.llm.get_answer_from_llm(
                        user_prompt,
                        system_prompt,
                    ).final_query

                    tools_result = await session.list_tools()

                    mcp_tools = tools_result.tools

                    intention = intentions[0]

                    groq_tools = self.convert_mcp_tool_list_to_groq_schema_tool_list(mcp_tools)

                    verification_user_prompt = sql_post_processing_component.prompt_management.fill_prompt(
                        sql_post_processing_component.verification_user_prompt_path,
                        activity_field=activity_field,
                        intention=intention,
                        generated_query=first_processed_query,
                        db_schema=db_schema,
                    )

                    verification_system_prompt = sql_post_processing_component.prompt_management.fill_prompt(
                        sql_post_processing_component.verification_system_prompt_path,
                    )

                    messages = [
                        {
                            "role": "system",
                            "content": verification_system_prompt,
                        },
                        {
                            "role": "user",
                            "content": verification_user_prompt,
                        },
                    ]

                    for i in range(1, self.max_iteration + 1):

                        response = await sql_post_processing_component.llm.get_answer_from_llm_with_tools(
                            messages,
                            groq_tools,
                        )

                        message = response.choices[0].message

                        if message.tool_calls:

                            for tool_call in message.tool_calls:
                                tool_name = tool_call.function.name

                                arguments = json.loads(
                                    tool_call.function.arguments
                                )

                                tool_result = await session.call_tool(
                                    tool_name,
                                    arguments,
                                )

                                messages.append({
                                    "role": "tool",
                                    "tool_call_id": tool_call.id,
                                    "content": json.dumps(tool_result),
                                })

                            continue

                    return message.content

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
