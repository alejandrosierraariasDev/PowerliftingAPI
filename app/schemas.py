from pydantic import BaseModel, Field, ConfigDict
from typing import List, Dict, Any


class Lift(BaseModel):
    # Modern Pydantic V2 way to add examples
    exercise: str = Field(..., json_schema_extra={"example": "Squat"})
    weight_kg: float = Field(..., json_schema_extra={"example": 300.0})
    reps: int = Field(..., json_schema_extra={"example": 1})


class AthleteBase(BaseModel):
    name: str
    category: str
    age: int
    country: str
    achievements: List[str] = []


class AthleteCreate(AthleteBase):
    pass


class Athlete(AthleteBase):
    id: int
    records: List[Lift] = []


    model_config = ConfigDict(from_attributes=True)