from app.llm_component.llm import LLM
from app.prompt_management_component.prompt_management import PromptManagement
from pathlib import Path

class FindIntention:

    def __init__(self,
                 llm: LLM,
                 prompt_management: PromptManagement,
                 ):
        self.llm = llm
        self.prompt_management = prompt_management

        base_dir = Path(__file__).parent

        self.system_prompt_path = base_dir / "system_prompt.txt"
        self.user_prompt_path = base_dir / "user_prompt.txt"

    def find_intention(self, question: str)->list[str]:
        try:

            user_prompt = self.prompt_management.fill_prompt(
                self.user_prompt_path,
                question=question,)

            system_prompt = self.prompt_management.fill_prompt(
                self.system_prompt_path,
            )

            return self.llm.get_answer_from_llm(
                user_prompt,
                system_prompt,
            ).intents

        except Exception as e:
            print(e)
            return []
