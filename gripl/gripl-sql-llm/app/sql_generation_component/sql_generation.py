from app.llm_component.llm import LLM
from app.prompt_management_component.prompt_management import PromptManagement
from pathlib import Path
import traceback




class SQLGenerator:

    def __init__(self,
                 llm: LLM,
                 prompt_management: PromptManagement,
                 ):
        self.llm = llm
        self.prompt_management = prompt_management

        base_dir = Path(__file__).parent

        self.system_prompt_path = base_dir / "system_prompt.txt"
        self.user_prompt_path = base_dir / "user_prompt.txt"


    def generate_query(self,
                       activity_field: str,
                       db_schema:str,
                       intentions: list[str],
                       reasons_of_intentions: list[str],
                       )->str:
        try:
            user_prompt = self.prompt_management.fill_prompt(
                self.user_prompt_path,
                activity_field=activity_field,
                db_schema=db_schema,
                intent=intentions,
                reasons_of_intentions=reasons_of_intentions,
            )

            system_prompt = self.prompt_management.fill_prompt(
                self.system_prompt_path,
            )

            messages = [
                {
                    "role": "system",
                    "content": system_prompt,
                },
                {
                    "role": "user",
                    "content": user_prompt,
                },
            ]

            return self.llm.get_answer_from_llm(
                messages
            ).query
        except Exception as e:
            print("in sql generating ")
            print(traceback.format_exc())
            print(e)
            return ""

