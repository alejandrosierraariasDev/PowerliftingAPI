import pytest
import os
from fastapi.testclient import TestClient
from app.main import app
from dotenv import load_dotenv

load_dotenv()
client = TestClient(app)


@pytest.fixture
def auth_headers():
    username = os.getenv("ADMIN_USERNAME")
    password = os.getenv("ADMIN_PASSWORD")
    login_data = {"username": username, "password": password}
    response = client.post("/token", data=login_data)
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


# --- TEST DE FLUJO COMPLETO (CREATE + DELETE) ---

def test_athlete_lifecycle(auth_headers):
    """Prueba crear un atleta y luego borrarlo usando su ID real"""

    # 1. CREAR
    new_athlete = {
        "name": "Test Athlete",
        "category": "105kg",
        "age": 25,
        "country": "Spain",
        "achievements": ["Testing Champion"]
    }
    create_res = client.post("/v1/athletes", json=new_athlete, headers=auth_headers)
    assert create_res.status_code == 201

    # Capturamos el ID que la base de datos le ha asignado
    athlete_id = create_res.json()["id"]

    # 2. VERIFICAR (Opcional pero recomendado)
    get_res = client.get(f"/v1/athletes/{athlete_id}")
    assert get_res.status_code == 200
    assert get_res.json()["name"] == "Test Athlete"

    # 3. BORRAR (Usando el ID dinámico)
    delete_res = client.delete(f"/v1/athletes/{athlete_id}", headers=auth_headers)
    assert delete_res.status_code == 200
    assert delete_res.json()["message"] == "Athlete deleted successfully from database"

    # 4. CONFIRMAR BORRADO
    final_res = client.get(f"/v1/athletes/{athlete_id}")
    assert final_res.status_code == 404


# --- OTROS TESTS ACTUALIZADOS ---

def test_get_all_athletes(client_db=client):
    response = client.get("/v1/athletes")
    assert response.status_code == 200
    assert "results" in response.json()


def test_reset_database(auth_headers):
    response = client.post("/v1/reset", headers=auth_headers)
    assert response.status_code == 200