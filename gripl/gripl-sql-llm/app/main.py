from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from .schemas import AnalysisSQLRequest
import os
from app.database.db import Base, engine
from app.database.models import *
import json
import traceback
from app.pipeline_component.pipeline import PipelineComponent
from app.data_loader_component.data_loader import DataLoader
from app.chroma_database_client.chroma_db_client import ChromaDatabaseClient
from app.find_intention_component.find_intention import FindIntention
from app.reranker_component.reranker import Reranker
from app.find_intention_component.schemas import IntentionAnswer
from app.sql_execution_component.sql_execution import SQLExecution
from app.sql_generation_component.sql_generation import SQLGenerator
from app.sql_generation_component.schemas import SQLGenerationAnswer
from app.sql_post_processing_component.sql_post_processing import SQLPostProcessing
from app.sql_post_processing_component.schemas import SQLPostProcessingAnswer, SQLVerificationResultAnswer
from app.sql_post_processing_component.post_processing_mcp_client import PostProcessingMcpClient
from sentence_transformers import SentenceTransformer
from app.llm_fallback_manager_component.llm_fallback_manager import LLMFallBackManager
from app.prompt_management_component.prompt_management import PromptManagement
from app.bpmn_data_pre_processor_component.bpmn_data_pre_processor import BPMNDataPreProcessor
from dotenv import load_dotenv
from app.config.component_name import (INTENTION_MODEL, SQL_GENERATION_MODEL, POST_PROCESSING_MODEL, VERIFICATION_MODEL,
                                       EMBEDDING_MODEL, CROSS_ENCODING_MODEL)
from app.logging_component.logger import Logger

load_dotenv()

app = FastAPI(
    title="GRIPL SQL LLM Service",
    description=(
        "Use Identification with SLQ LLM "
    ),
    version="0.1.0",
    root_path="/sql-llm",
)

# --------------------------------------------------------------------------
# DB initialisation
# --------------------------------------------------------------------------

Base.metadata.create_all(bind=engine)

# ---------------------------------------------------------------------------
# CORS
# ---------------------------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    # TODO: Change this to only allow the frontend and backend origins later
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/analyze", include_in_schema=False, response_model=None)
async def analyse(analysis_request: AnalysisSQLRequest = Depends(),
            ):
    try:

        print("request")
        print(vars(analysis_request))

        fill_in_db_models_and_env(
            json.loads(analysis_request.llmProps_raw).get("modelName", ""),
            json.loads(analysis_request.llmProps_raw).get("apiKey", ""),
        )



        pipeline_component = get_pipeline()

        bpmn_file = await analysis_request.bpmnFile.read()

        result = await pipeline_component.get_analysis(bpmn_file)

        return {
            "criticalElements": result
        }
    except Exception:
        print(traceback.format_exc())
        return []


def fill_in_db_models_and_env(
        models:str,
        api_keys_in_envy:str,
):
    try:

        sql_execution_component = SQLExecution()

        def parse_components(s: str):
            result = {}
            if not s:
                return result
            for part in s.split(';'):
                if not part:
                    continue
                if ':' not in part:
                    continue
                key, values = part.split(':', 1)
                items = [v.strip() for v in values.split(',') if v.strip()]
                if items:
                    result[key] = items
            return result

        models_map = parse_components(models)
        api_keys_map = parse_components(api_keys_in_envy)

        for comp_key, model_list in models_map.items():
            api_key_list = api_keys_map.get(comp_key, [])

            for idx, model_name in enumerate(model_list):

                api_key_name = api_key_list[idx] if idx < len(api_key_list) else ""

                sql = """
                      INSERT INTO fallback_llm
                          (corresponding_comment, name, "order", model_url, env_api_key_name)
                      VALUES (?, ?, ?, ?, ?) \
                      """
                params = (
                    comp_key,
                    model_name,
                    idx + 1,
                    "",
                    api_key_name
                )


                sql_execution_component.insert_sql(sql, params)

    except Exception:
        print(traceback.format_exc())


def get_pipeline(
):
    try:


        prompt_management = PromptManagement()

        bpmn_data_pre_processor = BPMNDataPreProcessor()

        intention_llm_handler = LLMFallBackManager(
            llm_component_name=INTENTION_MODEL,
            schema_output=IntentionAnswer,
        )

        sql_generation_llm_handler = LLMFallBackManager(
            llm_component_name=SQL_GENERATION_MODEL,
            schema_output=SQLGenerationAnswer,
        )

        post_processing_llm_handler = LLMFallBackManager(
            llm_component_name=POST_PROCESSING_MODEL,
            schema_output=SQLPostProcessingAnswer,
        )

        verification_llm_handler = LLMFallBackManager(
            llm_component_name=VERIFICATION_MODEL,
            schema_output=SQLVerificationResultAnswer,
        )

        post_processing_mcp_client = PostProcessingMcpClient()

        embedding_model_name = get_embedding_or_reranker(
            EMBEDDING_MODEL
        )

        model = SentenceTransformer(embedding_model_name)

        dictionary_name = "activity_example"

        collection_name = "activity_example"

        chroma_db_client = ChromaDatabaseClient(
            embedding_model=model,
            dictionary_name=dictionary_name,
            collection_name=collection_name,
        )

        sql_execution = SQLExecution()

        intention_logger = Logger(
            file_name="intention.csv"
        )

        sql_generation_logger = Logger(
            file_name="sql_generation.csv"
        )

        post_processed_logger = Logger(
            file_name="post_processing.csv"
        )

        intention_component = FindIntention(
            llm_handler=intention_llm_handler,
            prompt_management=prompt_management,
            sql_execution=sql_execution,
            logging_component=intention_logger,
        )

        sql_generator = SQLGenerator(
            llm_handler=sql_generation_llm_handler,
            prompt_management=prompt_management,
            logging_component=sql_generation_logger,
        )

        sql_post_processing = SQLPostProcessing(
            llm_handler=post_processing_llm_handler,
            verification_llm_handler=verification_llm_handler,
            prompt_management=prompt_management,
            post_processing_mcp_client=post_processing_mcp_client,
            logging_component=post_processed_logger
        )

        reranker_mode_name = get_embedding_or_reranker(CROSS_ENCODING_MODEL)

        reranker = Reranker(reranker_mode_name)

        return PipelineComponent(
            chroma_db_client=chroma_db_client,
            find_intention=intention_component,
            reranker=reranker,
            sql_execution=sql_execution,
            sql_generation=sql_generator,
            post_processing=sql_post_processing,
            bpmn_data_pre_processor=bpmn_data_pre_processor,
        )

    except Exception:
        print(traceback.format_exc())
        return PipelineComponent()


def get_embedding_or_reranker(
        component_name: str,
    ):
        try:

            sql_execution_component = SQLExecution()

            sql = f"""
                                SELECT name
                                FROM fallback_llm
                                 WHERE corresponding_comment = '{component_name}'
                                ORDER BY "order" ASC
                                LIMIT 1;
                                
                        """

            return  [execution_result.get("name", "") for execution_result in
                    sql_execution_component.get_sql_query_results(sql)][0]

        except Exception:
            print(traceback.format_exc())
            return []
