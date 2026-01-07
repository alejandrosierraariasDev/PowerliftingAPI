from pydantic import BaseModel, Field
from typing import List, Optional, Union, Dict, Any

class Record(BaseModel):
    # Usamos Dict[str, Any] para permitir tanto {"exercise": "...", "weight_kg": ...}
    # como {"stat": "...", "value": ...}
    data: Dict[str, Any]

    # Esto permite que Pydantic acepte diccionarios flexibles
    class Config:
        extra = "allow"

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
    records: List[Dict[str, Any]] = [] # Flexible para tus distintos deportes

    class Config:
        from_attributes = True