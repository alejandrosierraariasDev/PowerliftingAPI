import os
import json
from fastapi import FastAPI, HTTPException, status, Query, Depends
from typing import List
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import RedirectResponse
from dotenv import load_dotenv
from fastapi.openapi.utils import get_openapi
from contextlib import asynccontextmanager
from sqlalchemy.orm import Session

# Importaciones de tu estructura profesional
from app.database import get_db, engine, Base, reload_defaults
from app import models, schemas, auth
from app.auth import get_current_user, create_access_token

load_dotenv()

# Crea las tablas en Supabase (o SQLite) al arrancar la aplicación
models.Base.metadata.create_all(bind=engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Generación automática del contrato OpenAPI
    os.makedirs("app/contracts", exist_ok=True)
    openapi_schema = get_openapi(
        title="Powerlifting API",
        version="1.0.0",
        description="API for managing athletes and records",
        routes=app.routes,
    )
    with open("app/contracts/openapi.json", "w") as f:
        json.dump(openapi_schema, f, indent=2)
    yield

app = FastAPI(
    title="Powerlifting API",
    description="""
### 👤 Author Information
* **Name:** Alejandro Sierra
* **Portfolio:** [GitHub](https://github.com/alejandrosierraariasDev)
* **Email:** [alejandrosierraarias@gmail.com](mailto:alejandrosierraarias@gmail.com)

### 📖 About this API
Now powered by **SQLAlchemy & PostgreSQL (Supabase)**.
Features automated nightly resets and a full CI/CD pipeline.
    """,
    version="1.0.0",
    lifespan=lifespan
)

# --- AUTHENTICATION ---
ADMIN_USER = os.getenv("ADMIN_USERNAME")
ADMIN_PASS = os.getenv("ADMIN_PASSWORD")

@app.post("/token", tags=["Auth"])
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    if form_data.username == ADMIN_USER and form_data.password == ADMIN_PASS:
        access_token = create_access_token(data={"sub": form_data.username})
        return {"access_token": access_token, "token_type": "bearer"}

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Wrong credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

# --- SYSTEM ---
@app.get("/health", tags=["System"])
async def health_check(db: Session = Depends(get_db)):
    # Contamos los registros directamente en la BBDD
    count = db.query(models.Athlete).count()
    return {"status": "healthy", "database": "connected", "records": count}

@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse(url="/docs")

# --- QUERIES ---

@app.get("/v1/athletes", response_model=dict, tags=["Athletes"])
def get_athletes(
        db: Session = Depends(get_db),
        offset: int = Query(0, ge=0),
        limit: int = Query(10, ge=1, le=100)
):
    total_count = db.query(models.Athlete).count()
    athletes = db.query(models.Athlete).offset(offset).limit(limit).all()

    return {
        "total": total_count,
        "offset": offset,
        "limit": limit,
        "count": len(athletes),
        "results": athletes
    }

@app.get("/v1/athletes/search", response_model=List[schemas.Athlete], tags=["Queries"])
async def search_athlete_by_name(
        name: str = Query(..., description="Name or partial name"),
        db: Session = Depends(get_db)
):
    # Búsqueda dinámica en SQL usando ILIKE (no distingue mayúsculas)
    results = db.query(models.Athlete).filter(models.Athlete.name.ilike(f"%{name}%")).all()
    if not results:
        raise HTTPException(status_code=404, detail=f"No athlete found with name: {name}")
    return results

@app.get("/v1/athletes/category/{weight_class}", response_model=List[schemas.Athlete], tags=["Queries"])
async def get_by_weight_class(weight_class: str, db: Session = Depends(get_db)):
    # Filtro por categoría de peso
    results = db.query(models.Athlete).filter(models.Athlete.weight_class == weight_class).all()
    if not results:
        raise HTTPException(status_code=404, detail="No athletes found in that category")
    return results

@app.get("/v1/athletes/{athlete_id}", response_model=schemas.Athlete, tags=["Athletes"])
async def get_athlete(athlete_id: int, db: Session = Depends(get_db)):
    athlete = db.query(models.Athlete).filter(models.Athlete.id == athlete_id).first()
    if not athlete:
        raise HTTPException(status_code=404, detail="Athlete not found")
    return athlete

# --- ADMINISTRATION ---

@app.post("/v1/athletes", response_model=schemas.Athlete, status_code=201, tags=["Admin"])
def create_athlete(
        athlete: schemas.AthleteCreate,
        db: Session = Depends(get_db),
        current_user: str = Depends(get_current_user)
):
    db_athlete = models.Athlete(**athlete.model_dump())
    db.add(db_athlete)
    db.commit()
    db.refresh(db_athlete)
    return db_athlete

@app.delete("/v1/athletes/{athlete_id}", tags=["Admin"])
async def delete_athlete(
        athlete_id: int,
        db: Session = Depends(get_db),
        current_user: str = Depends(get_current_user)
):
    athlete = db.query(models.Athlete).filter(models.Athlete.id == athlete_id).first()
    if not athlete:
        raise HTTPException(status_code=404, detail="Athlete not found")

    db.delete(athlete)
    db.commit()
    return {"message": "Athlete deleted successfully from database"}

@app.post("/v1/reset", tags=["Admin"])
async def reset_db(
        db: Session = Depends(get_db),
        current_user: str = Depends(get_current_user)
):
    # Llamamos a la función de recarga pasándole la sesión activa
    reload_defaults(db)
    return {"message": "Database successfully restored in Supabase"}