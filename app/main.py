from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="API de Tareas", version="1.0.0")

# Almacenamiento en memoria (en la Evaluación 2 se reemplazará por una base de datos)
_db = {"tareas": {}, "siguiente_id": 1}


class TareaEntrada(BaseModel):
    titulo: str
    hecha: bool = False


@app.get("/health")
def estado():
    return {"status": "ok"}


@app.post("/tareas", status_code=201)
def crear_tarea(tarea: TareaEntrada):
    tarea_id = _db["siguiente_id"]
    _db["siguiente_id"] += 1
    _db["tareas"][tarea_id] = {"id": tarea_id, **tarea.model_dump()}
    return _db["tareas"][tarea_id]


@app.get("/tareas")
def listar_tareas():
    return list(_db["tareas"].values())


@app.get("/tareas/{tarea_id}")
def obtener_tarea(tarea_id: int):
    if tarea_id not in _db["tareas"]:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    return _db["tareas"][tarea_id]