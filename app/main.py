from fastapi import FastAPI, HTTPException, status
from typing import List
from app.schemas import Athlete, AthleteCreate
from app.database import db_athletes, reload_defaults

app = FastAPI(
    title="Powerlifting API",
    description="API for Athlete and Record Management",
    version="1.0.0"
)

@app.get("/v1/athletes", response_model=List[Athlete], tags=["Athletes"])
async def get_all_athletes():
    return db_athletes

@app.get("/v1/athletes/{athlete_id}", response_model=Athlete, tags=["Athletes"])
async def get_athlete_by_id(athlete_id: int):
    athlete = next((a for a in db_athletes if a["id"] == athlete_id), None)
    if not athlete:
        raise HTTPException(status_code=404, detail="Athlete not found")
    return athlete

@app.post("/v1/athletes", response_model=Athlete, status_code=201, tags=["Athletes"])
async def create_athlete(athlete_data: AthleteCreate):
    new_id = max([a["id"] for a in db_athletes], default=0) + 1
    new_athlete = {**athlete_data.model_dump(), "id": new_id, "records": []}
    db_athletes.append(new_athlete)
    return new_athlete

@app.delete("/v1/athletes/{athlete_id}", tags=["Athletes"])
async def delete_athlete(athlete_id: int):
    global db_athletes
    athlete = next((a for a in db_athletes if a["id"] == athlete_id), None)
    if not athlete:
        raise HTTPException(status_code=404, detail="Athlete not found")
    db_athletes[:] = [a for a in db_athletes if a["id"] != athlete_id]
    return {"message": f"Athlete {athlete_id} deleted correctly"}

@app.post("/v1/reset", tags=["Admin"])
async def reset_database():
    """Manual route to return to the initial state of 5 athletes"""
    reload_defaults()
    return {"message": "Database reset"}