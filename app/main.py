from fastapi import FastAPI, HTTPException, status
from typing import List
from .schemas import Athlete, AthleteCreate, LiftCreate
from .database import db_athletes

app = FastAPI(
    title="Powerlifting & Athletes API",
    description="API de pruebas para control de atletas y récords",
    version="1.0.0"
)

@app.get("/v1/athletes", response_model=List[Athlete], tags=["Atletas"])
async def get_athletes():
    return db_athletes

@app.post("/v1/athletes", response_model=Athlete, status_code=201)
async def create_athlete(athlete: AthleteCreate):
    """
    Crea un nuevo atleta.
    Ejemplo de logros: ["MVP 2024", "World Record Holder"]
    """
    new_id = max([a["id"] for a in db_athletes], default=0) + 1
    new_athlete = athlete.dict()
    new_athlete.update({"id": new_id, "records": []})
    db_athletes.append(new_athlete)
    return new_athlete

@app.get("/v1/athletes/{athlete_id}", response_model=Athlete, tags=["Atletas"])
async def get_athlete(athlete_id: int):
    athlete = next((a for a in db_athletes if a["id"] == athlete_id), None)
    if not athlete:
        raise HTTPException(status_code=404, detail="Atleta no encontrado")
    return athlete

@app.post("/v1/lifts/{athlete_id}", tags=["Récords"])
async def add_lift(athlete_id: int, lift: LiftCreate):
    athlete = next((a for a in db_athletes if a["id"] == athlete_id), None)
    if not athlete:
        raise HTTPException(status_code=404, detail="Atleta no encontrado")
    athlete["records"].append(lift.dict())
    return {"message": "Récord añadido"}

@app.delete("/v1/athletes/{athlete_id}", tags=["Atletas"])
async def delete_athlete(athlete_id: int):
    global db_athletes
    initial_len = len(db_athletes)
    db_athletes[:] = [a for a in db_athletes if a["id"] != athlete_id]
    if len(db_athletes) == initial_len:
        raise HTTPException(status_code=404, detail="Atleta no encontrado")
    return {"message": "Atleta eliminado"}