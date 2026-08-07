from typing import List
from pydantic import BaseModel, ConfigDict

class IntentionAnswer(BaseModel):
    model_config = ConfigDict(extra="forbid")
    intents: List[str]