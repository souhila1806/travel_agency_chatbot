from pydantic import BaseModel
from typing import Optional

class SafetyCheck(BaseModel):
    safe: bool
    reason: Optional[str] = None  # worth having, for debugging/logging why something was flagged