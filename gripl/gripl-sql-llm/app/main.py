from fastapi import FastAPI, Depends, HTTPException, status
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
from app.database.db import Base, engine
from app.database.models import *
from app.sql_execution_component.sql_execution import SQLExecution
from jose import jwt, JWTError
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

load_dotenv()

security = HTTPBearer()

STYTCH_DOMAIN = os.getenv("STYTCH_DOMAIN")
STYTCH_PROJECT_ID = os.getenv("STYTCH_PROJECT_ID")
JWKS_URL = f"{STYTCH_DOMAIN}/.well-known/jwks.json"

import requests

jwks = requests.get(JWKS_URL).json()


async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:

        payload = jwt.decode(
            token,
            jwks,
            algorithms=["RS256"],
            audience=STYTCH_PROJECT_ID,
            issuer=STYTCH_DOMAIN
        )

        return payload
    except JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )


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
def analyse(analysis_request: AnalysisSQLRequest = Depends(),
            current_user=Depends(get_current_user)
            ):
    grog_api_key = os.getenv("GROQ_API_KEY")

    user_id = current_user.get("sub")
    print("user id")
    print(user_id)

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
