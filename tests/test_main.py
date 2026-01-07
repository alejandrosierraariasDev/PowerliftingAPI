from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_athletes():
    # Comprueba que el GET funciona y devuelve los 5 atletas por defecto
    response = client.get("/v1/athletes")
    assert response.status_code == 200
    assert len(response.json()) == 5

def test_get_single_athlete():
    # Comprueba que Jesus Olivares (ID 1) existe
    response = client.get("/v1/athletes/1")
    assert response.status_code == 200
    assert response.json()["name"] == "Jesus Olivares"

def test_create_athlete_error():
    # Comprueba que falla si enviamos datos incompletos
    response = client.post("/v1/athletes", json={"name": "Incompleto"})
    assert response.status_code == 422 # Error de validación de Pydantic