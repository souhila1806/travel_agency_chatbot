from pydantic import BaseModel, Field

class TargetResponse(BaseModel):
    is_correct: bool = Field(
        description="Whether the AI response meets the expected answer"
    )
    reason: str = Field(
        description="Explanation supporting the evaluation"
    )