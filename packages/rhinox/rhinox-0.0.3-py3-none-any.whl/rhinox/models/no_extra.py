from pydantic import BaseModel, ConfigDict

class NoExtraModel(BaseModel):
    model_config = ConfigDict(extra="forbid")
