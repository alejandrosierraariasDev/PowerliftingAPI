import os
import json
from datetime import datetime, timedelta, timezone
from fastapi import FastAPI, HTTPException, status, Query,Security, Depends
from typing import List
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.schemas import Athlete, AthleteCreate
from app.database import db_athletes, reload_defaults
from fastapi.responses import RedirectResponse
from fastapi.security.api_key import APIKeyHeader
from dotenv import load_dotenv
from fastapi.openapi.utils import get_openapi
from contextlib import asynccontextmanager
from jose import jwt, JWTError

load_dotenv()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
@asynccontextmanager
async def lifespan(app: FastAPI):
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
* **Portfolio:** [ GitHub](https://github.com/alejandrosierraariasDev)
* **Email:** [alejandrosierraarias@gmail.com](mailto:alejandrosierraarias@gmail.com)

### 📖 About this API
This is a specialized API for **IPF Powerlifting** athletes and their world records. 
It features automated nightly resets and a full CI/CD pipeline.

**Quick Links:**
* [View JSON Athletes List](/v1/athletes)
---
    """,
    version="1.0.0",
    lifespan=lifespan

)

# --- AUTHENTICATION ---
SECRET_KEY = os.getenv("JWT_SECRET", "dev_secret_key_123")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 10080 # 1 week

ADMIN_USER = os.getenv("ADMIN_USERNAME")
ADMIN_PASS = os.getenv("ADMIN_PASSWORD")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token inválido o expirado",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        return username
    except JWTError:
        raise credentials_exception


@app.post("/token", tags=["Auth"])
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Endpoint para obtener el token.
    Usa el usuario y contraseña definidos en las variables de entorno.
    """
    if form_data.username == ADMIN_USER and form_data.password == ADMIN_PASS:
        access_token = create_access_token(data={"sub": form_data.username})
        return {"access_token": access_token, "token_type": "bearer"}

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Usuario o contraseña incorrectos",
        headers={"WWW-Authenticate": "Bearer"},
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

@app.post("/v1/athletes", response_model=Athlete, status_code=201, tags=["Admin"],dependencies=[Depends(get_current_user)])
async def create_athlete(athlete_data: AthleteCreate):
    """Register a new athlete in the system"""
    new_id = max([a["id"] for a in db_athletes], default=0) + 1
    new_athlete = {**athlete_data.model_dump(), "id": new_id, "records": []}
    db_athletes.append(new_athlete)
    return new_athlete

@app.delete("/v1/athletes/{athlete_id}", tags=["Admin"],dependencies=[Depends(get_current_user)])
async def delete_athlete(athlete_id: int):
    """Remove an athlete from the database"""
    global db_athletes
    db_athletes[:] = [a for a in db_athletes if a["id"] != athlete_id]
    return {"message": "Athlete deleted successfully"}

@app.post("/v1/reset", tags=["Admin"],dependencies=[Depends(get_current_user)])
async def reset_db():
    """Restore the database to the original 5 default athletes"""
    reload_defaults()
    return {"message": "Database successfully restored"}