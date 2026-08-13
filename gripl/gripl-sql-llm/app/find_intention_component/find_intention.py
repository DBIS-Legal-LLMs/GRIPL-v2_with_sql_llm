from app.llm_component.llm import LLM
from app.prompt_management_component.prompt_management import PromptManagement
from app.sql_execution_component.sql_execution import SQLExecution
from pathlib import Path
import traceback

class FindIntention:

    def __init__(self,
                 llm: LLM,
                 prompt_management: PromptManagement,
                 sql_execution: SQLExecution
                 ):
        self.llm = llm
        self.prompt_management = prompt_management
        self.sql_execution = sql_execution

        base_dir = Path(__file__).parent

        self.system_prompt_path = base_dir / "system_prompt.txt"
        self.user_prompt_path = base_dir / "user_prompt.txt"

    def find_intention_of_current_activity_field(self, activity_field: str)->list[str]:
        try:

            available_intents = self.get_all_intentions()

            user_prompt = self.prompt_management.fill_prompt(
                self.user_prompt_path,
                activity_field=activity_field,
                available_intents=available_intents,
            )

            system_prompt = self.prompt_management.fill_prompt(
                self.system_prompt_path,
            )

            return self.llm.get_answer_from_llm(
                user_prompt,
                system_prompt,
            ).intents

        except Exception as e:
            print(traceback.format_exc())
            print(e)
            return []

    def get_all_intentions(self,)->list[str]:
        try:
            row = self.sql_execution.get_sql_query_results("SELECT category.name FROM category")

            return [r.get('name', '') for r in row ]
        except Exception as e:
            print(e)
            return []

