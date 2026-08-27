from app.logging_component.logger import Logger
from .evaluator import Evaluator
from app.pipeline_component.pipeline import PipelineComponent
from app.data_loader_component.data_loader import DataLoader
from app.chroma_database_client.chroma_db_client import ChromaDatabaseClient
from app.find_intention_component.find_intention import FindIntention
from app.find_intention_component.schemas import IntentionAnswer
from app.sql_execution_component.sql_execution import SQLExecution
from app.sql_generation_component.sql_generation import SQLGenerator
from app.sql_generation_component.schemas import SQLGenerationAnswer
from app.sql_post_processing_component.sql_post_processing import SQLPostProcessing
from app.sql_post_processing_component.schemas import SQLPostProcessingAnswer, SQLVerificationResultAnswer
from app.sql_post_processing_component.post_processing_mcp_client import PostProcessingMcpClient
from sentence_transformers import SentenceTransformer
from app.llm_component.llm import LLM
from app.prompt_management_component.prompt_management import PromptManagement
from app.bpmn_data_pre_processor_component.bpmn_data_pre_processor import BPMNDataPreProcessor
from dotenv import load_dotenv
import os
from app.config.model_name import INTENTION_MODEL, SQL_GENERATION_MODEL, POST_PROCESSING_MODEL, VERIFICATION_MODEL
from pathlib import Path
import asyncio

load_dotenv()

prompt_management = PromptManagement()

bpmn_data_pre_processor = BPMNDataPreProcessor()

intention_llm = LLM(
    model_name=INTENTION_MODEL,
    model_url="",
    api_key=os.getenv("GROQ_API_KEY"),
    schema_output=IntentionAnswer
)

sql_generator_llm = LLM(
    model_name=SQL_GENERATION_MODEL,
    model_url="",
    api_key=os.getenv("GROQ_API_KEY"),
    schema_output=SQLGenerationAnswer
)

sql_post_processing_llm = LLM(
    model_name=POST_PROCESSING_MODEL,
    model_url="",
    api_key=os.getenv("GROQ_API_KEY"),
    schema_output=SQLPostProcessingAnswer
)

verification_llm = LLM(
    model_name=VERIFICATION_MODEL,
    model_url="",
    api_key=os.getenv("GROQ_API_KEY"),
    schema_output=SQLVerificationResultAnswer
)

post_processing_mcp_client = PostProcessingMcpClient()

model = SentenceTransformer('intfloat/multilingual-e5-small')

chroma_db_client = ChromaDatabaseClient(
    model
)

sql_execution = SQLExecution()

intention_logger = Logger(
    file_name="intention"
)

sql_generation_logger = Logger(
    file_name="sql_generation"
)

post_processed_logger = Logger(
    file_name="post_processing"
)

intention_component = FindIntention(
    llm=intention_llm,
    prompt_management=prompt_management,
    sql_execution=sql_execution,
    logging_component=intention_logger,
)

sql_generator = SQLGenerator(
    llm=sql_generator_llm,
    prompt_management=prompt_management,
    logging_component=sql_generation_logger,
)

sql_post_processing = SQLPostProcessing(
    llm=sql_post_processing_llm,
    verification_llm=verification_llm,
    prompt_management=prompt_management,
    post_processing_mcp_client=post_processing_mcp_client,
    logging_component=post_processed_logger
)

pipeline = PipelineComponent(
    chroma_db_client=chroma_db_client,
    find_intention=intention_component,
    sql_execution=sql_execution,
    sql_generation=sql_generator,
    post_processing=sql_post_processing,
    bpmn_data_pre_processor=bpmn_data_pre_processor,
)

project_root = Path(__file__).resolve().parents[4]

dataset_path = project_root / "dataset" / "evaluation_data.csv"

data_loader = DataLoader(
    str(dataset_path),
)

evaluator = Evaluator(
    pipe_line=pipeline,
    data_loader=data_loader,
)

asyncio.run(evaluator.evaluate())
