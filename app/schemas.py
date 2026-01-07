from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

# Definimos el esquema para los récords (Lifts, Stats, etc.)
class Record(BaseModel):
    # Usamos dict para que sea flexible (NBA, UFC, Powerlifting)
    data: Dict[str, Any]

# Este es el que te está dando el error de importación
class LiftCreate(BaseModel):
    exercise: str
    weight_kg: float
    reps: int

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
    records: List[Dict[str, Any]] = []

    class Config:
        from_attributes = True