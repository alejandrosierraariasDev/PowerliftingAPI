import pytest
import os
from fastapi.testclient import TestClient
from app.main import app
from dotenv import load_dotenv
from app.database import db_athletes
load_dotenv()
client = TestClient(app)

@pytest.fixture
def auth_headers():
    username = os.getenv("ADMIN_USERNAME")
    password = os.getenv("ADMIN_PASSWORD")

    if not username or not password:
        pytest.fail(" ADMIN_USERNAME or ADMIN_PASSWORD are missed")

    login_data = {"username": username, "password": password}
    response = client.post("/token", data=login_data)

    if response.status_code != 200:
        pytest.fail(f"Failed Login   Status: {response.status_code}")

    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

def test_get_all_athletes_pagination():

    actual_total = len(db_athletes)
    limit_value = 2
    offset_value = 0
    response = client.get(f"/v1/athletes?offset={offset_value}&limit={limit_value}")

    # Assertions
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == actual_total
    assert data["offset"] == offset_value
    assert data["limit"] == limit_value
    expected_results_count = min(actual_total, limit_value)
    assert len(data["results"]) == expected_results_count
    assert "count" in data
    assert data["count"] == expected_results_count


def test_pagination_out_of_bounds():
    actual_total = len(db_athletes)
    offset_value = actual_total + 1
    response = client.get(f"/v1/athletes?offset={offset_value}&limit=10")

    # Assertions
    assert response.status_code == 200
    data = response.json()
    assert data["results"] == []
    assert data["count"] == 0

def test_admin_flow_with_jwt(auth_headers):
    response = client.delete("/v1/athletes/1", headers=auth_headers)
    assert response.status_code == 200

def test_create_athlete_success(auth_headers):
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
    response = client.delete("/v1/athletes/1", headers=auth_headers)
    assert response.status_code == 200

def test_reset_database_auth(auth_headers):
    # 1. Test without token
    res_fail = client.post("/v1/reset")
    assert res_fail.status_code == 401

    # 2. Test with right token
    res_success = client.post("/v1/reset", headers=auth_headers)
    assert res_success.status_code == 200

def test_create_athlete_unauthorized():
    new_athlete = {"name": "Test", "category": "83kg", "age": 25, "country": "USA"}
    response = client.post("/v1/athletes", json=new_athlete)
    assert response.status_code == 401

def test_admin_with_wrong_token():
    wrong_headers = {"Authorization": "Bearer token_falso_123"}
    response = client.delete("/v1/athletes/2", headers=wrong_headers)
    assert response.status_code == 401