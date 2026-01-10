from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional

class Lift(BaseModel):
    exercise: str = Field(..., json_schema_extra={"example": "Squat"})
    weight_kg: float = Field(..., json_schema_extra={"example": 300.0})
    reps: int = Field(..., json_schema_extra={"example": 1})

    model_config = ConfigDict(from_attributes=True)

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
    # En la base de datos es un JSON, Pydantic lo validará como lista de Lifts
    records: List[Lift] = []

    # Esto permite que Pydantic lea los datos directamente de SQLAlchemy
    model_config = ConfigDict(from_attributes=True)

# NUEVA CLASE: Para corregir el error de serialización en el GET masivo
class AthletePagination(BaseModel):
    total: int
    offset: int
    limit: int
    count: int
    results: List[Athlete]

    model_config = ConfigDict(from_attributes=True)