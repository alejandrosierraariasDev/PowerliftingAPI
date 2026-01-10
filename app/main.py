import os
from fastapi import FastAPI, HTTPException, status, Query,Security, Depends
from typing import List
from app.schemas import Athlete, AthleteCreate
from app.database import db_athletes, reload_defaults
from fastapi.responses import RedirectResponse
from fastapi.security.api_key import APIKeyHeader
from dotenv import load_dotenv
load_dotenv()

app = FastAPI(
    title="Powerlifting API",
    description="""
### 👤 Author Information
* **Name:** Alejandro Sierra
* **Portfolio:** [ GitHub](https://github.com/alejandrosierraariasDev)
* **Email:** [alejandrosierraarias@gmail.com](mailto:alejandrosierraarias@gmail.com)

### 📖 About this API
This is a specialized API for **IPF Powerlifting** athletes and their world records. 
It features automated nightly resets and a full CI/CD pipeline.

**Quick Links:**
* [View JSON Athletes List](/v1/athletes)
---
    """,
    version="1.2.0"
)


# --- AUTHENTICATION ---

API_KEY_NAME = "X-API-KEY"
API_KEY = os.getenv("ADMIN_API_KEY", "dev_key")
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=True)
async def get_api_key(api_key: str = Security(api_key_header)):
    if api_key == API_KEY:
        return api_key
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Acceso denegado: API Key inválida"
    )

# --- SYSTEM ---
@app.get("/health", tags=["System"])
async def health_check():
    return {"status": "healthy", "database": "connected", "records": len(db_athletes)}

@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse(url="/docs")

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

@app.post("/v1/athletes", response_model=Athlete, status_code=201, tags=["Admin"],dependencies=[Depends(get_api_key)])
async def create_athlete(athlete_data: AthleteCreate):
    """Register a new athlete in the system"""
    new_id = max([a["id"] for a in db_athletes], default=0) + 1
    new_athlete = {**athlete_data.model_dump(), "id": new_id, "records": []}
    db_athletes.append(new_athlete)
    return new_athlete

@app.delete("/v1/athletes/{athlete_id}", tags=["Admin"],dependencies=[Depends(get_api_key)])
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