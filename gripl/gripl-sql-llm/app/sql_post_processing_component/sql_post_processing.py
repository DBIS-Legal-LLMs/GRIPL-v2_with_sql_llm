from app.llm_component.llm import LLM
from app.prompt_management_component.prompt_management import PromptManagement
from .post_processing_mcp_client import PostProcessingMcpClient
from pathlib import Path
import traceback


class SQLPostProcessing:

    def __init__(self,
                 llm: LLM,
                 prompt_management: PromptManagement,
                 post_processing_mcp_client: PostProcessingMcpClient
                 ):
        self.llm = llm
        self.prompt_management = prompt_management
        self.post_processing_mcp_client = post_processing_mcp_client

        base_dir = Path(__file__).parent

        self.system_prompt_path = base_dir / "system_prompt.txt"
        self.user_prompt_path = base_dir / "user_prompt.txt"

    async def post_process_generated_query(self,
                                     db_schema: str,
                                     activity_field: str,
                                     generated_query: str,
                                     error_message: str,
                                     intentions: list[str],
                                     reasons_of_intentions: list[str],
                                     )->str:
        try:

            mcp_result = await self.post_processing_mcp_client.get_mcp_client_answer()
            print("res mcp ")
            print(mcp_result)

            return ""

            user_prompt = self.prompt_management.fill_prompt(
                self.user_prompt_path,
                activity_field=activity_field,
                db_schema=db_schema,
                generated_query=generated_query,
                error_message=error_message,
                intent=",".join(intentions),
                reasons_of_intentions=",".join(reasons_of_intentions),
            )

            system_prompt = self.prompt_management.fill_prompt(
                self.system_prompt_path,
            )

            return self.llm.get_answer_from_llm(
                user_prompt,
                system_prompt,
            ).final_query

        except Exception as e:
            print("e in post_processing")
            print(traceback.format_exc())
            print(e)
            return ""
