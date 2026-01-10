from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

HEADERS = {"X-API-KEY": "dev_key"}


# --- TESTS  ---

def test_get_all_athletes():
    response = client.get("/v1/athletes")
    assert response.status_code == 200
    assert len(response.json()) == 5


# --- TESTS (POST) ---

def test_create_athlete_success():
    """Verifica que se puede crear un atleta con la llave correcta"""
    new_athlete = {
        "name": "Lasha Talakhadze",
        "category": "109kg+",
        "age": 30,
        "country": "Georgia",
        "achievements": ["Olympic Gold 2020"]
    }
    response = client.post("/v1/athletes", json=new_athlete, headers=HEADERS)
    assert response.status_code == 201
    assert response.json()["name"] == "Lasha Talakhadze"


def test_create_athlete_unauthorized():
    new_athlete = {
        "name": "Lasha Talakhadze",
        "category": "109kg+",
        "age": 30,
        "country": "Georgia",
        "achievements": ["Olympic Gold 2020"]
    }
    response = client.post("/v1/athletes", json=new_athlete)  # Sin headers
    assert response.status_code == 401


# --- TESTS (DELETE) ---

def test_delete_athlete_success():
    """Verifica que se puede borrar un atleta con la llave correcta"""
    # Primero creamos uno para borrarlo con seguridad
    response = client.delete("/v1/athletes/1", headers=HEADERS)
    assert response.status_code == 200


def test_delete_athlete_unauthorized():
    """Verifica que falla el borrado sin llave"""
    response = client.delete("/v1/athletes/1")
    assert response.status_code == 401


# --- TESTS ADMIN (RESET) ---

def test_reset_database_auth():
    """Verifica que solo el admin puede resetear la DB"""
    # 1. Intento sin llave
    res_fail = client.post("/v1/reset")
    assert res_fail.status_code == 401

    # 2. Intento con llave correcta
    res_success = client.post("/v1/reset", headers=HEADERS)
    assert res_success.status_code == 200


def test_admin_with_wrong_key():
    """Verifica que una llave incorrecta devuelve 403 (Prohibido)"""
    wrong_headers = {"X-API-KEY": "llave_inventada_123"}
    # Probamos con cualquier ruta protegida, por ejemplo DELETE
    response = client.delete("/v1/athletes/2", headers=wrong_headers)
    assert response.status_code == 403