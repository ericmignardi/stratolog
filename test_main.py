from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def setup_function():
    pass

# CREATE Tests
def test_create():
    response = client.post("/guitars", json={"brand": "Squier", "model": "Affinity Starcaster Deluxe", "year": "2024", "colour": "Olympic White", "type": "Electric"})
    assert response.status_code == 201
    assert response.json() == {"brand": "Squier", "model": "Affinity Starcaster Deluxe", "year": "2024", "colour": "Olympic White", "type": "Electric"}

def test_create_invalid():
    response = client.post("/guitars", json={"brand": "Squier", "year": "2024", "colour": "Olympic White", "type": "Electric"})
    assert response.status_code == 422

def test_create_response():
    response = client.post("/guitars", json={"brand": "Squier", "model": "Affinity Starcaster Deluxe", "year": "2024", "colour": "Olympic White", "type": "Electric"})
    assert response.json() == {"brand": "Squier", "model": "Affinity Starcaster Deluxe", "year": "2024", "colour": "Olympic White", "type": "Electric"}

# READ Tests
def test_read_all():
    response = client.get("/guitars")
    assert response.status_code == 200

def test_read_by_id():
    response = client.get("/guitars/1")
    assert response.status_code == 200

def test_read_by_id_invalid():
    response = client.get("/guitars/-1")
    assert response.status_code == 404

def test_read_by_id_response():
    client.post("/guitars", json={"brand": "Squier", "model": "Affinity Starcaster Deluxe", "year": "2024", "colour": "Olympic White", "type": "Electric"})
    response = client.get("/guitars/1")
    assert response.json() == {"id": 1, "brand": "Squier", "model": "Affinity Starcaster Deluxe", "year": "2024", "colour": "Olympic White", "type": "Electric"}

# UPDATE Tests
def test_update():
    # client.post("/guitars", json={"brand": "Epiphone", "model": "ES-333", "year": "2004", "colour": "Olive Drab", "type": "Electric"})
    response = client.put("guitars/7", json={"brand": "Epiphone", "model": "ES-333", "year": "2004", "colour": "Black", "type": "Electric"})
    assert response.status_code == 200
    assert response.json() == {"brand": "Epiphone", "model": "ES-333", "year": "2004", "colour": "Black", "type": "Electric"}

# DELETE Tests
def test_delete():
    response = client.delete("/guitars/1")
    assert response.status_code == 200

def test_delete_invalid():
    response = client.delete("/guitars/-1")
    assert response.status_code == 404

def teardown_function():
    pass