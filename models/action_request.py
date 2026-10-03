from pydantic import BaseModel, Field
from typing import Optional

class ActionRequest(BaseModel):
    destination: str = Field(description="The user requested destination")
    arrival_date: Optional[str] = Field(description="user requested arrival date of the trip in YYYY-MM-DD format", default=None)
    departure_date: Optional[str] = Field(description="user requested departure date of the trip in YYYY-MM-DD format",default=None)
    preferences: Optional[str] = Field(description="user preferences in the trip. Example: meuseums and arts, adventures, shopping, relaxation and spa, etc",default=None)
    budget: Optional[float] = Field(description="user budget for the travel stop",default=None)
