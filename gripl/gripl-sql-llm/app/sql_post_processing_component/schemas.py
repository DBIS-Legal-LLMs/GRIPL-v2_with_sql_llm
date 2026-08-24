from typing import Literal

from pydantic import BaseModel, ConfigDict

class SQLPostProcessingAnswer(BaseModel):
    model_config = ConfigDict(extra="forbid")
    final_query: str

class SQLVerificationResultAnswer(BaseModel):
    intention_status: Literal["unchanged", "changed"]
    reason_status: Literal["unchanged", "changed"]

    intention: str
    reason: str

    final_query: str