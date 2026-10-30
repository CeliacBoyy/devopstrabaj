import pytest
from fastapi.testclient import TestClient

from app.main import _db, app

cliente = TestClient(app)


@pytest.fixture(autouse=True)
def limpiar_db():
    _db["tareas"].clear()
    _db["siguiente_id"] = 1


def test_estado():
    r = cliente.get("/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}


def test_crear_tarea():
    r = cliente.post("/tareas", json={"titulo": "Estudiar DevOps"})
    assert r.status_code == 201
    assert r.json() == {"id": 1, "titulo": "Estudiar DevOps", "hecha": False}


def test_listar_tareas():
    cliente.post("/tareas", json={"titulo": "A"})
    cliente.post("/tareas", json={"titulo": "B"})
    r = cliente.get("/tareas")
    assert r.status_code == 200
    assert [t["titulo"] for t in r.json()] == ["A", "B"]


def test_obtener_tarea():
    cliente.post("/tareas", json={"titulo": "A"})
    r = cliente.get("/tareas/1")
    assert r.status_code == 200
    assert r.json()["titulo"] == "A"


def test_obtener_tarea_inexistente():
    assert cliente.get("/tareas/99").status_code == 404

def test_eliminar_tarea():
    cliente.post("/tareas", json={"titulo": "A"})
    assert cliente.delete("/tareas/1").status_code == 204
    assert cliente.get("/tareas/1").status_code == 404


def test_eliminar_tarea_inexistente():
    assert cliente.delete("/tareas/99").status_code == 404    

def test_titulo_vacio_es_rechazado():
    r = cliente.post("/tareas", json={"titulo": ""})
    assert r.status_code == 422