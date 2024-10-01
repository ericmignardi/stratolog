from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pytest
from main import app, get_db
from database import Base
from models import Guitar

engine = create_engine("mysql+mysqlconnector://root:password@localhost:3306/StratologTest")
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

client = TestClient(app)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture
def setup():
    post_response = client.post("/guitars", json={"brand": "Squier", "model": "Affinity Starcaster Deluxe", "year": "2024", "colour": "Olympic White", "type": "Electric"})

def test_read(setup):
    get_response = client.get("/guitars")
    assert get_response.status_code == 200
    assert get_response.json() == [{"id": 1, "brand": "Squier", "model": "Affinity Starcaster Deluxe", "year": "2024", "colour": "Olympic White", "type": "Electric"}]

def test_create():
    post_response_2 = client.post("/guitars", json={"brand": "JET", "model": "JT-300", "year": "2024", "colour": "Shell Pink", "type": "Electric"})
    data = post_response_2.json()
    id = data["id"]
    assert post_response_2.status_code == 201
    assert post_response_2.json() == {"id": id, "brand": "JET", "model": "JT-300", "year": "2024", "colour": "Shell Pink", "type": "Electric"}

def test_read_by_id(setup):
    get_response = client.get("/guitars/1")
    assert get_response.status_code == 200
    assert get_response.json() == {"id": 1, "brand": "Squier", "model": "Affinity Starcaster Deluxe", "year": "2024", "colour": "Olympic White", "type": "Electric"}

def test_update(setup):
    put_response = client.put("/guitars/1", json={"brand": "Squier", "model": "Affinity Starcaster Deluxe", "year": "2024", "colour": "Shell Pink", "type": "Electric"})
    assert put_response.status_code == 200
    assert put_response.json() == {"id": 1, "brand": "Squier", "model": "Affinity Starcaster Deluxe", "year": "2024", "colour": "Shell Pink", "type": "Electric"}

def test_delete(setup):
    delete_response = client.delete("/guitars/1")
    assert delete_response.status_code == 200
    assert delete_response.json() == {"id": 1, "brand": "Squier", "model": "Affinity Starcaster Deluxe", "year": "2024", "colour": "Shell Pink", "type": "Electric"}
    response = client.get("/guitars/1")
    assert response.status_code == 404