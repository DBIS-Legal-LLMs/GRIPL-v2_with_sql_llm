from .evaluator import Evaluator
from app.pipeline_component.pipeline import PipelineComponent
from app.data_loader_component.data_loader import DataLoader
from app.chroma_database_client.chroma_db_client import ChromaDatabaseClient
from app.find_intention_component.find_intention import FindIntention
from app.sql_execution_component.sql_execution import SQLExecution
from app.sql_generation_component.sql_generation import SQLGenerator
from app.sql_post_processing_component.sql_post_processing import SQLPostProcessing
from sentence_transformers import SentenceTransformer
from app.llm_component.llm import LLM
from app.prompt_management_component.prompt_management import PromptManagement
from app.bpmn_data_pre_processor_component.bpmn_data_pre_processor import BPMNDataPreProcessor
from dotenv import load_dotenv
import os
from app.config.model_name import INTENTION_MODEL, SQL_GENERATION_MODEL, POST_PROCESSING_MODEL
from pathlib import Path

load_dotenv()

prompt_management = PromptManagement()

bpmn_data_pre_processor = BPMNDataPreProcessor()

intention_llm = LLM(
    model_name=INTENTION_MODEL,
    model_url="",
    api_key=os.getenv("OPENAI_API_KEY"),
    schema_output=None
)

sql_generator_llm = LLM(
    model_name=SQL_GENERATION_MODEL,
    model_url="",
    api_key=os.getenv("OPENAI_API_KEY"),
    schema_output=None
)

sql_post_processing_llm = LLM(
    model_name=POST_PROCESSING_MODEL,
    model_url="",
    api_key=os.getenv("OPENAI_API_KEY"),
    schema_output=None
)

model = SentenceTransformer('intfloat/multilingual-e5-small')

chroma_db_client = ChromaDatabaseClient(
    model
)

intention_component = FindIntention(
    llm=intention_llm,
    prompt_management=prompt_management,
)

sql_generator = SQLGenerator(
    llm=sql_generator_llm,
    prompt_management=prompt_management,
)

sql_post_processing = SQLPostProcessing(
    llm=sql_post_processing_llm,
    prompt_management=prompt_management,
)

sql_execution = SQLExecution()

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

evaluator.evaluate()
