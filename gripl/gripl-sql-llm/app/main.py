from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from .schemas import AnalysisSQLRequest
from dotenv import load_dotenv
import os
from app.llm_component.llm import LLM
from pydantic import BaseModel, ConfigDict
from typing import List

load_dotenv()

class UserData(BaseModel):
    model_config = ConfigDict(extra="forbid")
    name: str
    age: int
    hobbies: List[str]


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
    print("received request")
    print(analysis_request)
    print("in analys")


    grog_api_key = os.getenv("GROQ_API_KEY")
    

    system_prompt = f"Gib die Profildaten exakt im JSON-Format aus. Verwende keine Erklärungen."

    user_name = "Max"
    user_age = 28
    user_hobbies = ["Lesen", "schreiben"]

    user_prompt = f"Der Nutzer heißt {user_name}, ist {user_age} Jahre alt und mag {', '.join(user_hobbies)}."

    llm_component = LLM(
        api_key=grog_api_key,
        model_url="",
        model_name="openai/gpt-oss-120b",
        schema_output=UserData
    )

    ans = llm_component.get_answer_from_llm(user_prompt, system_prompt)



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