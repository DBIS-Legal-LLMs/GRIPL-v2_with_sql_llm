from typing import List, Literal
from pydantic import BaseModel, ConfigDict

class IntentionAnswer(BaseModel):
    model_config = ConfigDict(extra="forbid")
    intents: List[
        Literal[
            "Collection",
            "Storage",
            "Usage",
            "Transferal",
            "Modification",
            "Deletion",
            "Access"
        ]
    ]