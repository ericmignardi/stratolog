from fastapi.testclient import TestClient
import pytest
from main import app

client = TestClient(app)

# Helper Functions
def get_post_response():
    return client.post("/guitars", json={"brand": "Squier", "model": "Affinity Starcaster Deluxe", "year": "2024", "colour": "Olympic White", "type": "Electric"})

# Pytest Fixtures
@pytest.fixture
def setup():
    pass

@pytest.fixture
def teardown():
    pass

def test_create_status_response():
    post_response = get_post_response()
    data = post_response.json()
    id = data["id"]
    assert post_response.status_code == 201
    assert post_response.json() == {"id": id, "brand": "Squier", "model": "Affinity Starcaster Deluxe", "year": "2024", "colour": "Olympic White", "type": "Electric"}
    get_response = client.get(f"/guitars/{id}")
    assert get_response.status_code == 200

def test_read():
    post_response = get_post_response()
    data = post_response.json()
    id = data["id"]
    assert post_response.status_code == 201
    assert post_response.json() == {"id": id, "brand": "Squier", "model": "Affinity Starcaster Deluxe", "year": "2024", "colour": "Olympic White", "type": "Electric"}
    get_response = client.get("/guitars")
    assert get_response.status_code == 200
    assert get_response.json() == [{"id": id, "brand": "Squier", "model": "Affinity Starcaster Deluxe", "year": "2024", "colour": "Olympic White", "type": "Electric"}]

def test_read_by_id():
    post_response = get_post_response()
    data = post_response.json()
    id = data["id"]
    assert post_response.status_code == 201
    assert post_response.json() == {"id": id, "brand": "Squier", "model": "Affinity Starcaster Deluxe", "year": "2024", "colour": "Olympic White", "type": "Electric"}
    get_response = client.get(f"/guitars/{id}")
    assert get_response.status_code == 200
    assert get_response.json() == {"id": id, "brand": "Squier", "model": "Affinity Starcaster Deluxe", "year": "2024", "colour": "Olympic White", "type": "Electric"}

def test_update():
    post_response = get_post_response()
    data = post_response.json()
    id = data["id"]
    assert post_response.status_code == 201
    assert post_response.json() == {"id": id, "brand": "Squier", "model": "Affinity Starcaster Deluxe", "year": "2024", "colour": "Olympic White", "type": "Electric"}
    put_response = client.put(f"/guitars/{id}", json={"brand": "Squier", "model": "Affinity Starcaster Deluxe", "year": "2024", "colour": "Shell Pink", "type": "Electric"})
    assert put_response.status_code == 200
    assert put_response.json() == {"id": id, "brand": "Squier", "model": "Affinity Starcaster Deluxe", "year": "2024", "colour": "Shell Pink", "type": "Electric"}

def test_delete():
    post_response = get_post_response()
    data = post_response.json()
    id = data["id"]
    assert post_response.status_code == 201
    assert post_response.json() == {"id": id, "brand": "Squier", "model": "Affinity Starcaster Deluxe", "year": "2024", "colour": "Olympic White", "type": "Electric"}
    delete_response = client.delete(f"/guitars/{id}")
    assert delete_response.status_code == 200
    assert delete_response.json() == {"id": id, "brand": "Squier", "model": "Affinity Starcaster Deluxe", "year": "2024", "colour": "Olympic White", "type": "Electric"}