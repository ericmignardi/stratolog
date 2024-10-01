from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
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

def setup():
    Base.metadata.create_all(bind=engine)

def teardown():
    Base.metadata.drop_all(bind=engine)

def setup_post():
    return client.post("/guitars", json={"brand": "Squier", "model": "Affinity Starcaster Deluxe", "year": "2024", "colour": "Olympic White", "type": "Electric"})

def test_read():
    post_response = setup_post()
    data = post_response.json()
    id = data["id"]
    assert post_response.status_code == 201
    assert post_response.json() == {"id": id, "brand": "Squier", "model": "Affinity Starcaster Deluxe", "year": "2024", "colour": "Olympic White", "type": "Electric"}
    get_response = client.get("/guitars")
    assert get_response.status_code == 200
    assert get_response.json() == [{"id": id, "brand": "Squier", "model": "Affinity Starcaster Deluxe", "year": "2024", "colour": "Olympic White", "type": "Electric"}]

def test_create_status_response():
    post_response = setup_post()
    data = post_response.json()
    id = data["id"]
    assert post_response.status_code == 201
    assert post_response.json() == {"id": id, "brand": "Squier", "model": "Affinity Starcaster Deluxe", "year": "2024", "colour": "Olympic White", "type": "Electric"}
    get_response = client.get(f"/guitars/{id}")
    assert get_response.status_code == 200
    assert get_response.json() == {"id": id, "brand": "Squier", "model": "Affinity Starcaster Deluxe", "year": "2024", "colour": "Olympic White", "type": "Electric"}

def test_read_by_id():
    post_response = setup_post()
    data = post_response.json()
    id = data["id"]
    assert post_response.status_code == 201
    assert post_response.json() == {"id": id, "brand": "Squier", "model": "Affinity Starcaster Deluxe", "year": "2024", "colour": "Olympic White", "type": "Electric"}
    get_response = client.get(f"/guitars/{id}")
    assert get_response.status_code == 200
    assert get_response.json() == {"id": id, "brand": "Squier", "model": "Affinity Starcaster Deluxe", "year": "2024", "colour": "Olympic White", "type": "Electric"}

def test_update():
    post_response = setup_post()
    data = post_response.json()
    id = data["id"]
    assert post_response.status_code == 201
    assert post_response.json() == {"id": id, "brand": "Squier", "model": "Affinity Starcaster Deluxe", "year": "2024", "colour": "Olympic White", "type": "Electric"}
    put_response = client.put(f"/guitars/{id}", json={"brand": "Squier", "model": "Affinity Starcaster Deluxe", "year": "2024", "colour": "Shell Pink", "type": "Electric"})
    assert put_response.status_code == 200
    assert put_response.json() == {"id": id, "brand": "Squier", "model": "Affinity Starcaster Deluxe", "year": "2024", "colour": "Shell Pink", "type": "Electric"}

def test_delete():
    post_response = setup_post()
    data = post_response.json()
    id = data["id"]
    assert post_response.status_code == 201
    assert post_response.json() == {"id": id, "brand": "Squier", "model": "Affinity Starcaster Deluxe", "year": "2024", "colour": "Olympic White", "type": "Electric"}
    delete_response = client.delete(f"/guitars/{id}")
    assert delete_response.status_code == 200
    assert delete_response.json() == {"id": id, "brand": "Squier", "model": "Affinity Starcaster Deluxe", "year": "2024", "colour": "Olympic White", "type": "Electric"}