# Tasks API

API REST mínima para gestionar tareas, hecha con FastAPI. Proyecto base para la asignatura
DOY0101 Ingeniería DevOps (Evaluaciones Parciales 1 y 2).

## Ejecución local

```bash
python -m venv .venv
source .venv/bin/activate        # En Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload    # http://localhost:8000/docs
pytest                           # ejecuta las pruebas
```

## Endpoints

| Método | Ruta            | Descripción            |
|--------|-----------------|------------------------|
| GET    | `/health`       | Estado del servicio    |
| POST   | `/tareas`       | Crea una tarea         |
| GET    | `/tareas`       | Lista todas las tareas |
| GET    | `/tareas/{id}`  | Obtiene una tarea      |