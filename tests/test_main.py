from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

HEADERS = {"X-API-KEY": "dev_key"}

def test_get_all_athletes():
    """Check if the default 5 athletes are returned"""
    response = client.get("/v1/athletes")
    assert response.status_code == 200
    assert len(response.json()) == 5

def test_search_by_name():
    """Check if searching for 'Jesus' returns Jesus Olivares"""
    response = client.get("/v1/athletes/search?name=Jesus")
    assert response.status_code == 200
    data = response.json()
    assert data[0]["name"] == "Jesus Olivares"

def test_filter_by_weight_class():
    """Check if searching for '83kg' returns Russel Orhii"""
    response = client.get("/v1/athletes/category/83kg")
    assert response.status_code == 200
    assert response.json()[0]["name"] == "Russel Orhii"

def test_delete_and_reset():
    """Test the administration flow: Delete an athlete and then reset the DB"""
    # 1. Delete ID 1 (Añadimos HEADERS)
    delete_res = client.delete("/v1/athletes/1", headers=HEADERS)
    assert delete_res.status_code == 200

    # 2. Verify it's gone
    get_res = client.get("/v1/athletes/1")
    assert get_res.status_code == 404

    # 3. Trigger Reset (Añadimos HEADERS)
    reset_res = client.post("/v1/reset", headers=HEADERS)
    assert reset_res.status_code == 200

    # 4. Verify it's back
    final_res = client.get("/v1/athletes/1")
    assert final_res.status_code == 200
    assert final_res.json()["name"] == "Jesus Olivares"

def test_admin_without_key():
    """Test security: Verify that admin actions fail without a key"""
    response = client.delete("/v1/athletes/1")
    assert response.status_code == 403 # Forbidden