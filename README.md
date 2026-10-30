# API de Tareas — Evaluación Parcial 1 (DOY0101 Ingeniería DevOps)

API REST mínima para gestionar tareas, hecha con FastAPI. El foco de este repositorio no es la
aplicación, sino el flujo de trabajo: control de versiones, colaboración mediante pull requests
y automatización con GitHub Actions. Es la base del pipeline CI/CD de la Evaluación Parcial 2.

## Ejecución local

```bash
python -m venv .venv
.venv\Scripts\activate            # En Linux/Mac: source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload     # http://localhost:8000/docs
python -m pytest                  # ejecuta las pruebas
```

## Endpoints

| Método | Ruta           | Descripción                                |
|--------|----------------|--------------------------------------------|
| GET    | `/health`      | Estado del servicio                        |
| POST   | `/tareas`      | Crea una tarea (el título no puede ser vacío) |
| GET    | `/tareas`      | Lista todas las tareas                     |
| GET    | `/tareas/{id}` | Obtiene una tarea                          |
| DELETE | `/tareas/{id}` | Elimina una tarea                          |

## Estrategia de ramificación: GitFlow

Se eligió **GitFlow** en lugar de trunk-based development o GitHub Flow.

**Justificación**

- Existe una rama `develop` donde se integra el trabajo en curso, y `main` queda siempre con
  código estable y etiquetado (`vX.Y.Z`). Esto separa lo que se está construyendo de lo que ya
  está listo, y da trazabilidad.
- Los hotfix tienen un camino propio (`hotfix/*` desde `main`), así que una corrección urgente
  no depende de que `develop` esté estable.
- Es adecuado para un proyecto con versiones explícitas y revisión por pull request. Trunk-based
  exige integración muy frecuente y feature flags; GitHub Flow no tiene una rama de integración
  previa a producción.

**Contra asumido:** más ramas y más pasos de merge que trunk-based. Para un equipo pequeño es un
costo aceptable a cambio de orden y claridad.

### Ramas

| Rama               | Se crea desde | Se integra en          | Propósito                                  |
|--------------------|---------------|------------------------|--------------------------------------------|
| `main`             | —             | —                      | Código estable. Cada release lleva un tag. |
| `develop`          | `main`        | `main` (release)       | Integración del trabajo en curso.          |
| `feature/<nombre>` | `develop`     | `develop`              | Una funcionalidad o mejora.                |
| `hotfix/<nombre>`  | `main`        | `main` y `develop`     | Corrección urgente de un error.            |

Ramas usadas en este repositorio: `feature/eliminar-tarea`, `feature/ci-github-actions`,
`feature/documentacion` y `hotfix/validar-titulo-vacio`.

## Convenciones

### Naming de ramas

Formato `tipo/descripcion-en-kebab-case`: minúsculas, sin espacios ni tildes.
Ejemplos: `feature/eliminar-tarea`, `hotfix/validar-titulo-vacio`.

### Mensajes de commit (Conventional Commits)

```
<tipo>(<alcance opcional>): <descripción en imperativo, minúscula, sin punto final>
```

| Tipo       | Uso                                         |
|------------|---------------------------------------------|
| `feat`     | Nueva funcionalidad                         |
| `fix`      | Corrección de un error                      |
| `test`     | Agregar o modificar pruebas                 |
| `docs`     | Documentación                               |
| `ci`       | Cambios en GitHub Actions                   |
| `chore`    | Mantenimiento (configuración, dependencias) |
| `refactor` | Cambio de código sin alterar comportamiento |

Ejemplos: `feat(api): agrega endpoint para eliminar tareas`, `fix(api): rechaza tareas con título vacío`.

### Flujo de merge

1. **Feature:** `develop` → rama `feature/x` → commits → **pull request a `develop`** → merge con
   commit de merge.
2. **Release:** cuando `develop` está estable → **PR de `develop` a `main`** → el CI debe pasar →
   merge → tag `vX.Y.0`.
3. **Hotfix:** `main` → rama `hotfix/x` → **PR a `main`** → tag `vX.Y.Z` → **PR de vuelta a
   `develop`** para no perder la corrección.
4. No se hace push directo a `main` ni a `develop`: todo entra por pull request.

### Estrategia de revisión

- Todo cambio entra por pull request, con título en formato Conventional Commits y una
  descripción de qué cambia y por qué.
- Antes de fusionar se revisa que el cambio haga lo que dice, que tenga pruebas y que el CI esté
  en verde.
- Los PR son pequeños y de un solo propósito.

### Estructura de carpetas

```
.
├── app/                    # Código de la aplicación
│   ├── __init__.py
│   └── main.py
├── tests/                  # Pruebas automatizadas (pytest)
│   └── test_api.py
├── .github/workflows/      # Pipelines de GitHub Actions
│   └── ci.yml
├── requirements.txt        # Dependencias
├── pytest.ini
└── README.md
```

### Control de versiones

[Versionado semántico](https://semver.org/lang/es/) `MAJOR.MINOR.PATCH`, con tags anotados en `main`:

- `v1.0.0`: primera versión estable (API con endpoint de eliminación y CI).
- `v1.0.1`: hotfix que rechaza tareas con título vacío.

## Automatización (GitHub Actions)

El workflow `.github/workflows/ci.yml` se ejecuta en cada **push a `develop`** y en cada **pull
request hacia `main`**. Instala las dependencias y ejecuta `pytest`.

En CI/CD cumple el rol de **integración continua**: cada cambio que llega a una rama de
integración se valida automáticamente, y un cambio que rompe las pruebas se detecta antes de
llegar a `main`. Corre en un entorno cloud simulado (runner `ubuntu-latest` de GitHub), sin
depender de la máquina de ninguna persona.

## Trazabilidad

El historial de Git muestra qué rama originó cada cambio, qué pull request lo integró y qué tag
lo liberó. Se puede revisar con `git log --oneline --graph --all` y en la pestaña *Pull requests*
del repositorio.

## Declaración de uso de IA

- Herramienta: Claude (Anthropic).
- Uso: El usado dado a la IA fue apoyo para generar el proyecto base, explicar comandos de Git y
  borradores de configuración, todo revisado y validado por mí_

## Conclusiones y reflexión individual

### Reflexión de _Benjamin Tapia_

_Aprendí a utilizar el workflow, actions, entre otras funciones, además de poder entender de mejor manera el funcionamiento de GITHUB_