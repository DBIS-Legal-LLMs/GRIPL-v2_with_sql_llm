import traceback
from typing import Type
from pydantic import BaseModel
from app.llm_component.llm import LLM
from app.sql_execution_component.sql_execution import SQLExecution
from app.llm_component.llm import LLM
from dotenv import load_dotenv
import os

load_dotenv()

class LLMFallBackManager:

    def __init__(self,
                 llm_component_name: str,
                 schema_output: Type[BaseModel]
                 ):
        self.llm_component_name = llm_component_name
        self.schema_output = schema_output
        self.current_llm_index = 0
        self.sql_execution_component = SQLExecution()


    def get_answer_with_fallback(self,
                                 messages: list,
                                 tools: list | None = None,
                                 ):

        try:

             all_models, env_api_key_name = self.get_all_possible_llm_models_of_component(self.llm_component_name)

             for model, env_api_key_name in all_models:

                 self.get_answer_from_current_llm(
                     messages=messages,
                     tools=tools,
                     model_name=model,
                     api_key_env_name=env_api_key_name,
                 )

             return {}

        except Exception as e:
            print(traceback.format_exc())

    def get_all_possible_llm_models_of_component(self, component_name: str) -> list:

        try:

            return [(execution_result.get("reason", ""), execution_result.get("reason", "") )for execution_result in
                                    self.sql_execution_component.get_sql_query_results(f"""
                                                                            SELECT
                                                                            name,
                                                                            env_api_key_name
                                                                        FROM fallback_llm
                                                                        WHERE corresponding_comment = '{component_name}'
                                                                        ORDER BY "order" ASC;
                                                                            """)]

        except Exception as e:
            print(traceback.format_exc())
            return []

    def get_answer_from_current_llm(self,
                                    messages: list,
                                    model_name: str,
                                    api_key_env_name: str,
                                    tools: list | None = None,
                                    ):
        try:

            llm = LLM(
                model_name= model_name,
            model_url="",
            api_key= os.getenv(api_key_env_name),
            schema_output=self.schema_output
            )

            llm.get_answer_from_llm(
                messages=messages,
                tools=tools,
            )

        except Exception as e:
            print(traceback.format_exc())
            raise




