from pydantic import BaseModel, Field, field_validator, model_validator
from datetime import datetime


class TravelStop(BaseModel):
    location: str = Field(description="The location of the travel stop")
    arrival_date: str = Field(description="Arrival date of the travel stop in YYYY-MM-DD format")
    departure_date: str = Field(description="Departure date of the travel stop in YYYY-MM-DD format")
    activities: list[str] = Field(description="List of activities to do in the location")
    budget: float = Field(description="Estimated budget for the travel stop")

    @field_validator("arrival_date", "departure_date")
    @classmethod
    def validate_date_format(cls, value):
        try:
            datetime.strptime(value, "%Y-%m-%d")
        except ValueError:
            raise ValueError(f"date must be in YYYY-MM-DD format, got '{value}'")
        return value

    @field_validator("activities")
    @classmethod
    def validate_activities_not_empty(cls, value):
        if not value or len(value) == 0:
            raise ValueError("activities list cannot be empty")
        return value

    @field_validator("budget")
    @classmethod
    def validate_budget_positive(cls, value):
        if value < 0:
            raise ValueError("budget must be a positive number")
        return value


    @field_validator("location")
    @classmethod
    def validate_not_blank(cls, value):
        if not value or not value.strip():
            raise ValueError("field cannot be blank")
        return value.strip()


    @model_validator(mode="after")
    def validate_dates_order(self): 
        arrival = datetime.strptime(self.arrival_date, "%Y-%m-%d")
        departure = datetime.strptime(self.departure_date, "%Y-%m-%d")
        if arrival > departure:
            raise ValueError("arrival_date must be before or equal to departure_date")
        return self