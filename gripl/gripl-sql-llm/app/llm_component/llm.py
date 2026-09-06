from groq import Groq
from typing import Type
from pydantic import BaseModel
import traceback
import instructor
from app.config.retry_configuration import MAX_RETRIES


class LLM:

    def __init__(self,
                 model_name: str,
                 model_url: str,
                 api_key: str,
                 schema_output: Type[BaseModel]
                 ):
        self.model_name = model_name
        self.model_url = model_url
        self.api_key = api_key
        self.schema_output = schema_output
        self.max_retries: int = MAX_RETRIES

    def get_answer_from_llm(self,
                            messages: list,
                            tools: list | None = None,
                            ):
        try:

            if not tools:
                return self.get_structured_answer(messages)

            client = instructor.from_provider(
                model=self.model_name,
                api_key=self.api_key,
                mode=instructor.Mode.TOOLS,
            )

            response = client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                tools=tools,
                tool_choice="auto",
                response_model=None,
                max_retries=self.max_retries,
            )

            message = response.choices[0].message

            if message.tool_calls:
                return self.get_tool_use_answer(messages)

            messages.append({
                "role": "assistant",
                "content": message.content,
            })
            return self.get_structured_answer(
                messages,
            )

        except Exception:
            print(traceback.format_exc())
            raise

    def get_structured_answer(self, messages: list):

        try:

            # TODO: had problems with instructor.from_provider with groq , must be changed if not to groq

            client = instructor.from_groq(
                Groq(
                    api_key=self.api_key),
                mode=instructor.Mode.JSON,
            )

            return client.create(
                model=self.model_name,
                response_model=self.schema_output,
                max_retries=self.max_retries,
                messages=messages,
            )

        except Exception as e:
            print(traceback.format_exc())
            return {}

    def get_tool_use_answer(self, messages: list):
        try:
            return messages[-1]
        except Exception:
            print(traceback.format_exc())
            return []
