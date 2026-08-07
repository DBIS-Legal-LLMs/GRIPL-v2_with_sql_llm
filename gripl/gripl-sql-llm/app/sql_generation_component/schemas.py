from pydantic import BaseModel, ConfigDict

class SQLGenerationAnswer(BaseModel):
    model_config = ConfigDict(extra="forbid")
    query: str