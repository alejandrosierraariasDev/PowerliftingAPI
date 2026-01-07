from fastapi import FastAPI, HTTPException, status
from typing import List
from app.schemas import Athlete, AthleteCreate, LiftCreate # <-- Verifica este import
from app.database import db_athletes

app = FastAPI(
    title="Powerlifting & Athletes API",
    version="1.0.0"
)

@app.get("/v1/athletes", response_model=List[Athlete])
async def get_athletes():
    return db_athletes

@app.post("/v1/athletes", response_model=Athlete, status_code=201)
async def create_athlete(athlete: AthleteCreate):
    new_id = max([a["id"] for a in db_athletes], default=0) + 1
    new_athlete = athlete.dict()
    new_athlete.update({"id": new_id, "records": []})
    db_athletes.append(new_athlete)
    return new_athlete

@app.post("/v1/lifts/{athlete_id}")
async def add_lift(athlete_id: int, lift: LiftCreate):
    athlete = next((a for a in db_athletes if a["id"] == athlete_id), None)
    if not athlete:
        raise HTTPException(status_code=404, detail="Atleta no encontrado")
    athlete["records"].append(lift.dict())
    return {"message": "Récord añadido"}