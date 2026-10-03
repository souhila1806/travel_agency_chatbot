from pydantic import BaseModel, Field
from typing import Optional, Literal

class RAGQuery(BaseModel):
    destination: Optional[str] = Field(default=None, description="The destination mentioned in the user's question, if any")
    type: Literal["general_info", "hotel_offer", "flight_offer"] = Field(description="The category of information being requested")