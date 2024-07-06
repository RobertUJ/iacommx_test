import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.database.helpers import get_db
from src.database.session import Base
from src.main import app
from src.solicitudes.models import EstatusSolicitud, MagicAffinity, Solicitud

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"  # Usar SQLite para pruebas

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


@pytest.fixture(scope="module")
def setup_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


def test_create_solicitud(setup_db):
    response = client.post("/solicitudes/", json={
        "name": "JuanPerez123",
        "last_name": "Perez456",
        "identification": "12345abc",
        "age": 25,
        "magic_affinity": "FIRE",
        "email": "juan@example.com"
    })
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "JuanPerez123"
    assert data["email"] == "juan@example.com"
    assert data["status"] == "PENDING"


def test_read_solicitud(setup_db):
    response = client.post("/solicitudes/", json={
        "name": "AnaGomez789",
        "last_name": "Gomez321",
        "identification": "67890def",
        "age": 30,
        "magic_affinity": "WATER",
        "email": "ana@example.com"
    })
    solicitud_id = response.json()["id"]

    response = client.get(f"/solicitudes/{solicitud_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "AnaGomez789"


def test_update_solicitud(setup_db):
    response = client.post("/solicitudes/", json={
        "name": "LuisLopez111",
        "last_name": "Lopez222",
        "identification": "11111ghi",
        "age": 22,
        "magic_affinity": "EARTH",
        "email": "luis@example.com"
    })
    solicitud_id = response.json()["id"]

    response = client.put(f"/solicitudes/{solicitud_id}", json={
        "name": "LuisLopez222"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "LuisLopez222"


def test_update_solicitud_estatus(setup_db):
    response = client.post("/solicitudes/", json={
        "name": "CarlosDiaz333",
        "last_name": "Diaz444",
        "identification": "22222jkl",
        "age": 28,
        "magic_affinity": "WIND",
        "email": "carlos@example.com"
    })
    solicitud_id = response.json()["id"]

    response = client.patch(f"/solicitudes/{solicitud_id}/estatus", json={
        "status": "APPROVED"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "APPROVED"


def test_read_solicitudes(setup_db):
    response = client.get("/solicitudes/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


def test_delete_solicitud(setup_db):
    response = client.post("/solicitudes/", json={
        "name": "MariaLopez555",
        "last_name": "Lopez666",
        "identification": "33333mno",
        "age": 32,
        "magic_affinity": "LIGHT",
        "email": "maria@example.com"
    })
    solicitud_id = response.json()["id"]

    response = client.delete(f"/solicitudes/{solicitud_id}")
    assert response.status_code == 204

    response = client.get(f"/solicitudes/{solicitud_id}")
    assert response.status_code == 404
