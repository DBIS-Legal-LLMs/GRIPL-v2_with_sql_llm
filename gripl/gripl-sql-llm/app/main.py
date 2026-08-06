from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware


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


@app.post("/analyse", include_in_schema=False)
def analyse(request: Request):
    print("in analys")