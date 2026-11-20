import json
import logging
import time

from fastapi import FastAPI, HTTPException, Request
from prometheus_client import Gauge
from prometheus_fastapi_instrumentator import Instrumentator
from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# Logs estructurados (JSON): una línea por evento, fáciles de consultar en Loki
# ---------------------------------------------------------------------------
class FormatoJson(logging.Formatter):
    CAMPOS_EXTRA = ("method", "path", "status", "duration_ms")

    def format(self, record):
        datos = {
            "ts": self.formatTime(record, "%Y-%m-%dT%H:%M:%S%z"),
            "level": record.levelname,
            "logger": record.name,
            "msg": record.getMessage(),
        }
        for campo in self.CAMPOS_EXTRA:
            if hasattr(record, campo):
                datos[campo] = getattr(record, campo)
        if record.exc_info:
            datos["exception"] = self.formatException(record.exc_info)
        return json.dumps(datos, ensure_ascii=False)


logger = logging.getLogger("tareas-api")
if not logger.handlers:
    _handler = logging.StreamHandler()
    _handler.setFormatter(FormatoJson())
    logger.addHandler(_handler)
    logger.setLevel(logging.INFO)
    logger.propagate = False

app = FastAPI(title="API de Tareas", version="1.1.0")

# Almacenamiento en memoria (sin persistencia)
_db = {"tareas": {}, "siguiente_id": 1}

# ------------------------
# Métricas para Prometheus
# ------------------------
TAREAS_TOTAL = Gauge("tareas_total", "Cantidad de tareas almacenadas")
TAREAS_TOTAL.set_function(lambda: len(_db["tareas"]))

Instrumentator().instrument(app).expose(app, endpoint="/metrics", include_in_schema=False)

# Rutas que no se registran en los logs (generan ruido: healthchecks y scraping)
RUTAS_SIN_LOG = {"/health", "/metrics"}


@app.middleware("http")
async def registrar_peticiones(request: Request, call_next):
    inicio = time.perf_counter()
    try:
        respuesta = await call_next(request)
    except Exception:
        logger.exception(
            "error no controlado",
            extra={"method": request.method, "path": request.url.path, "status": 500},
        )
        raise
    if request.url.path not in RUTAS_SIN_LOG:
        logger.info(
            "peticion",
            extra={
                "method": request.method,
                "path": request.url.path,
                "status": respuesta.status_code,
                "duration_ms": round((time.perf_counter() - inicio) * 1000, 2),
            },
        )
    return respuesta


class TareaEntrada(BaseModel):
    titulo: str = Field(min_length=1)
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


@app.delete("/tareas/{tarea_id}", status_code=204)
def eliminar_tarea(tarea_id: int):
    if tarea_id not in _db["tareas"]:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    del _db["tareas"][tarea_id]


@app.get("/simular-error")
def simular_error():
    """Genera un error 500 a propósito, para probar métricas, logs y alertas."""
    raise RuntimeError("error simulado para pruebas de observabilidad")