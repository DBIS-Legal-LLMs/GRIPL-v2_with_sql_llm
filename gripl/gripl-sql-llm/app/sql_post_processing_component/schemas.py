from pydantic import BaseModel, ConfigDict

class SQLPostProcessingAnswer(BaseModel):
    model_config = ConfigDict(extra="forbid")
    final_query: str