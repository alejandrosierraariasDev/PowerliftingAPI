from fastapi import FastAPI, HTTPException, status, Query
from typing import List
from app.schemas import Athlete, AthleteCreate
from app.database import db_athletes, reload_defaults

app = FastAPI(
    title="Powerlifting Legends API",
    description="API specialized in IPF Powerlifting athletes and their records",
    version="1.2.0"
)

# --- QUERIES ---

@app.get("/v1/athletes", response_model=List[Athlete], tags=["Athletes"])
async def get_all_athletes():
    """Returns the full list of powerlifters"""
    return db_athletes

@app.get("/v1/athletes/search", response_model=List[Athlete], tags=["Queries"])
async def search_athlete_by_name(name: str = Query(..., description="Name or partial name of the athlete")):
    """Search athletes by name or last name"""
    filtered = [a for a in db_athletes if name.lower() in a["name"].lower()]
    if not filtered:
        raise HTTPException(status_code=404, detail=f"No athlete found with name: {name}")
    return filtered

@app.get("/v1/athletes/category/{weight_class}", response_model=List[Athlete], tags=["Queries"])
async def get_by_weight_class(weight_class: str):
    """Filter athletes by weight class (e.g., 120kg+, 83kg)"""
    filtered = [a for a in db_athletes if a["category"].lower() == weight_class.lower()]
    if not filtered:
        raise HTTPException(status_code=404, detail="No athletes found in that category")
    return filtered

@app.get("/v1/athletes/{athlete_id}", response_model=Athlete, tags=["Athletes"])
async def get_athlete(athlete_id: int):
    """Find a specific athlete by their unique ID"""
    athlete = next((a for a in db_athletes if a["id"] == athlete_id), None)
    if not athlete:
        raise HTTPException(status_code=404, detail="Athlete not found")
    return athlete

# --- ADMINISTRATION ---

@app.post("/v1/athletes", response_model=Athlete, status_code=201, tags=["Admin"])
async def create_athlete(athlete_data: AthleteCreate):
    """Register a new athlete in the system"""
    new_id = max([a["id"] for a in db_athletes], default=0) + 1
    new_athlete = {**athlete_data.model_dump(), "id": new_id, "records": []}
    db_athletes.append(new_athlete)
    return new_athlete

@app.delete("/v1/athletes/{athlete_id}", tags=["Admin"])
async def delete_athlete(athlete_id: int):
    """Remove an athlete from the database"""
    global db_athletes
    db_athletes[:] = [a for a in db_athletes if a["id"] != athlete_id]
    return {"message": "Athlete deleted successfully"}

@app.post("/v1/reset", tags=["Admin"])
async def reset_db():
    """Restore the database to the original 5 default athletes"""
    reload_defaults()
    return {"message": "Database successfully restored"}