import re
import json
from json_repair import repair_json
from groq import Groq
from typing import Type
from pydantic import BaseModel
import traceback

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

    def get_answer_from_llm(self,
                            user_prompt: str,
                            system_prompt: str,
                            ):
        try:
            client = Groq(api_key=self.api_key)
            response = client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                response_format={
                    "type": "json_schema",
                    "json_schema": {
                        "name": "user_data_schema",
                        "strict": True,
                        "schema": self.schema_output.model_json_schema()
                    }
                }
            )

            raw_output = response.choices[0].message.content
            return self.post_process_answer(raw_output)
        except Exception as e:
            print(traceback.format_exc())
            return {}


    def post_process_answer(self, raw_output: str):

        code_block_pattern = r'```(?:json)?\s*\n?(.*?)\n?```'
        match = re.search(code_block_pattern, raw_output, re.DOTALL)
        if match:
            raw_output = match.group(1).strip()
        else:
            start = raw_output.find('{')
            end = raw_output.rfind('}')
            if start != -1 and end != -1 and end > start:
                raw_output = raw_output[start:end + 1]

        try:
            repaired = repair_json(raw_output)
            data = json.loads(repaired)
        except Exception as e:
            try:
                data = json.loads(raw_output)
            except json.JSONDecodeError:
                #raise ValueError(f"Could not parse JSON from output: {raw_output}") from e
                return {}

        try:
            validated = self.schema_output.model_validate(data)
        except Exception as e:
            #raise ValueError(f"Validation failed: {e}") from e
            return {}


        return validated