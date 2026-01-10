import pytest
import os
from fastapi.testclient import TestClient
from app.main import app
from dotenv import load_dotenv

load_dotenv()
client = TestClient(app)

@pytest.fixture
def auth_headers():
    """Obtiene el token usando las credenciales reales del .env sin hardcode"""
    username = os.getenv("ADMIN_USERNAME")
    password = os.getenv("ADMIN_PASSWORD")

    if not username or not password:
        pytest.fail("Faltan las variables ADMIN_USERNAME o ADMIN_PASSWORD en el entorno")

    login_data = {"username": username, "password": password}
    # OAuth2 espera los datos en el cuerpo del formulario (data=), no como JSON
    response = client.post("/token", data=login_data)

    if response.status_code != 200:
        pytest.fail(f"Login fallido en el test. Status: {response.status_code}")

    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

# --- TESTS PÚBLICOS ---

def test_get_all_athletes():
    response = client.get("/v1/athletes")
    assert response.status_code == 200
    assert len(response.json()) == 5

# --- TESTS PROTEGIDOS (JWT) ---

def test_admin_flow_with_jwt(auth_headers):
    """Verifica el flujo completo: login (vía fixture) y borrado"""
    response = client.delete("/v1/athletes/1", headers=auth_headers)
    assert response.status_code == 200

def test_create_athlete_success(auth_headers):
    """Verifica que se puede crear un atleta con el Token dinámico"""
    new_athlete = {
        "name": "Lasha Talakhadze",
        "category": "109kg+",
        "age": 30,
        "country": "Georgia",
        "achievements": ["Olympic Gold 2020"]
    }
    response = client.post("/v1/athletes", json=new_athlete, headers=auth_headers)
    assert response.status_code == 201
    assert response.json()["name"] == "Lasha Talakhadze"

def test_delete_athlete_success(auth_headers):
    """Verifica el borrado con el Token dinámico"""
    response = client.delete("/v1/athletes/1", headers=auth_headers)
    assert response.status_code == 200

def test_reset_database_auth(auth_headers):
    """Verifica que solo el admin con Token puede resetear la DB"""
    # 1. Intento sin token
    res_fail = client.post("/v1/reset")
    assert res_fail.status_code == 401

    # 2. Intento con token correcto
    res_success = client.post("/v1/reset", headers=auth_headers)
    assert res_success.status_code == 200

# --- TESTS DE SEGURIDAD (FALLOS ESPERADOS) ---

def test_create_athlete_unauthorized():
    """Verifica que falla la creación sin cabecera de autorización"""
    new_athlete = {"name": "Test", "category": "83kg", "age": 25, "country": "USA"}
    response = client.post("/v1/athletes", json=new_athlete)
    assert response.status_code == 401

def test_admin_with_wrong_token():
    """Verifica que un token inventado devuelve 401"""
    wrong_headers = {"Authorization": "Bearer token_falso_123"}
    response = client.delete("/v1/athletes/2", headers=wrong_headers)
    assert response.status_code == 401