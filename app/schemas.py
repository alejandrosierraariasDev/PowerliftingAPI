from pydantic import BaseModel
from typing import List, Dict, Any

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

# For the endpoint to add records individually
class RecordUpdate(BaseModel):
    data: Dict[str, Any]