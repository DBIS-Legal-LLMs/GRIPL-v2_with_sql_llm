from app.chroma_database_client.chroma_db_client import ChromaDatabaseClient
from app.find_intention_component.find_intention import FindIntention
from app.sql_execution_component.sql_execution import SQLExecution
from app.sql_generation_component.sql_generation import SQLGenerator
from app.sql_post_processing_component.sql_post_processing import SQLPostProcessing
from app.bpmn_data_pre_processor_component.bpmn_data_pre_processor import BPMNDataPreProcessor
from app.database.utils import get_db_schema_string

class PipelineComponent:

    def __init__(self,
            chroma_db_client: ChromaDatabaseClient,
            find_intention: FindIntention,
            sql_execution: SQLExecution,
            sql_generation: SQLGenerator,
            post_processing: SQLPostProcessing,
            bpmn_data_pre_processor: BPMNDataPreProcessor,
                 ):
        self.chroma_db_client = chroma_db_client
        self.find_intention = find_intention
        self.sql_execution = sql_execution
        self.sql_generation = sql_generation
        self.post_processing = post_processing
        self.bpmn_data_pre_processor = bpmn_data_pre_processor


    def get_only_activity_fields(self, bpmn_file_content: str):
        try:
            return self.bpmn_data_pre_processor.get_only_activity_field_of_bpmn_file(
                bpmn_content=bpmn_file_content,
            )
        except Exception as e:
            print(e)
            return []

    async def get_sid_and_reason_if_critical(self, activity_field: str)->dict[str, str]:
        try:



            post_processed_query = await self.post_processing.post_process_generated_query(
                db_schema="",
                activity_field=activity_field,
                generated_query="",
                error_message="",
                intentions=[],
                reasons_of_intentions=[],
            )

            results_of_post_processed_query = self.sql_execution.get_sql_query_results(post_processed_query)[0].get("reason", "")

            if results_of_post_processed_query:
                return {
                    "value": self.bpmn_data_pre_processor.get_sid_from_activity_field_of_bpmn_file(activity_field),
                    "reason": results_of_post_processed_query ,
                }

            return {}

        except Exception as e:
            print(e)
            return {}
