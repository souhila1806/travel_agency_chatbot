from pydantic import BaseModel, Field, field_validator, model_validator, computed_field
from datetime import datetime
from models.travel_stop import TravelStop

class Trip(BaseModel):
    destination: str = Field(description="The destination of the trip")
    trip_name: str = Field(description="The name of the trip")
    arrival_date: str = Field(description="Arrival date of the trip in YYYY-MM-DD format")
    departure_date: str = Field(description="Departure date of the trip in YYYY-MM-DD format")
    other_expenses: float = Field(description="Other expenses for the trip like flights tickets, accommodation, etc.")
    travel_stops: list[TravelStop] = Field(description="List of travel stops in the trip")

    @computed_field
    @property
    def total_stops_budget(self) -> float:
        return sum(stop.budget for stop in self.travel_stops)

    @computed_field
    @property
    def total_budget(self) -> float:
        return self.total_stops_budget + self.other_expenses

    @field_validator("arrival_date", "departure_date")
    @classmethod
    def validate_date_format(cls, value):
        try:
            datetime.strptime(value, "%Y-%m-%d")
        except ValueError:
            raise ValueError(f"date must be in YYYY-MM-DD format, got '{value}'")
        return value


    @model_validator(mode="after")
    def validate_dates_order(self): 
        arrival = datetime.strptime(self.arrival_date, "%Y-%m-%d")
        departure = datetime.strptime(self.departure_date, "%Y-%m-%d")
        if arrival > departure:
            raise ValueError("arrival_date must be before or equal to departure_date")
        return self