from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from .schemas import AnalysisSQLRequest
from dotenv import load_dotenv
import os
from app.llm_component.llm import LLM
from app.find_intention_component.find_intention import FindIntention
from app.find_intention_component.schemas import IntentionAnswer
from app.prompt_management_component.prompt_management import PromptManagement
from app.sql_generation_component.sql_generation import SQLGenerator
from app.sql_generation_component.schemas import SQLGenerationAnswer


load_dotenv()




app = FastAPI(
    title="GRIPL SQL LLM Service",
    description=(
        "Use Identification with SLQ LLM "
    ),
    version="0.1.0",
    root_path="/sql-llm",
)

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


@app.post("/analyze", include_in_schema=False,response_model=None)
def analyse(analysis_request: AnalysisSQLRequest = Depends()):
    grog_api_key = os.getenv("GROQ_API_KEY")






    ## TODO replace dummy response with correct answer

    return {
        "criticalElements": [
            {
                "id": "Activity_1",
                "name": "Read customer data",
                "type": "task",
                "reason": "Dummy output",
                "references": []
            },
            {
                "id": "Activity_2",
                "name": "Store customer data",
                "type": "task",
                "reason": "Dummy output",
                "references": []
            }
        ],
        "amountOfRetries": 1,
        "ragContext": None,
        "ragPromptContext": None
    }