from app.llm_component.llm import LLM
from app.prompt_management_component.prompt_management import PromptManagement
from .post_processing_mcp_client import PostProcessingMcpClient
from pathlib import Path
import traceback


class SQLPostProcessing:

    def __init__(self,
                 llm: LLM,
                 verification_llm: LLM,
                 prompt_management: PromptManagement,
                 post_processing_mcp_client: PostProcessingMcpClient
                 ):
        self.llm = llm
        self.verification_llm = verification_llm
        self.prompt_management = prompt_management
        self.post_processing_mcp_client = post_processing_mcp_client

        base_dir = Path(__file__).parent

        self.system_prompt_path = base_dir / "system_prompt.txt"
        self.user_prompt_path = base_dir / "user_prompt.txt"

        self.verification_system_prompt_path = base_dir / "verification_system_prompt.txt"
        self.verification_user_prompt_path = base_dir / "verification_user_prompt.txt"

    async def post_process_generated_query(self,
                                           db_schema: str,
                                           activity_field: str,
                                           generated_query: str,
                                           error_message: str,
                                           intentions: list[str],
                                           reasons_of_intentions: list[str],
                                           ) -> str:
        try:

            return await self.post_processing_mcp_client.get_mcp_client_answer(
                db_schema,
                activity_field,
                generated_query,
                error_message,
                intentions,
                reasons_of_intentions,
                self
            )

        except Exception as e:
            print("e in post_processing")
            print(traceback.format_exc())
            print(e)
            return ""
