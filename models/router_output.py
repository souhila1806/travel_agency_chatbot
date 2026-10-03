from pydantic import BaseModel, Field, field_validator, model_validator, computed_field
from typing import Literal

class RouterOutput(BaseModel):
    intent: Literal["question", "action"] = Field(description="The type of the output, either 'question' or 'action'")