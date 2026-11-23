# VinylLab — Recommended File Structure / Estructura de Archivos Recomendada

---

## English

A simple, conflict-free structure aligned with `SCOPE.md` and `TASK.md` so each team member can work in their own files.

```text
VinylLab/
├── main.py                      # Single FastAPI entry point (registers all routers)
├── requirements.txt             # Python dependencies
├── .env.example                 # Example environment variables (DATABASE_URL)
├── .gitignore
├── README.md
├── SCOPE.md
├── TASK.md
│
├── app/                         # Backend application
│   ├── __init__.py
│   ├── database.py              # PostgreSQL connection & get_db()
│   ├── models/                  # Database models (1 file per entity)
│   │   ├── __init__.py
│   │   ├── user.py              # Users / Clients (Qingfei)
│   │   ├── vinyl.py             # Vinyls (Victor)
│   │   ├── service.py           # Services (Victor)
│   │   └── reservation.py       # Reservations (Eric)
│   ├── schemas/                 # Pydantic schemas (request / response)
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── vinyl.py
│   │   ├── service.py
│   │   └── reservation.py
│   └── routers/                 # API endpoints (FastAPI APIRouter)
│       ├── __init__.py
│       ├── auth.py              # Register, login, password (Qingfei)
│       ├── users.py             # Profile & client CRUD (Qingfei)
│       ├── vinyls.py            # Vinyl endpoints (Victor)
│       ├── services.py          # Service endpoints (Victor)
│       └── reservations.py      # Reservations & slot check (Eric)
│
├── sql/                         # Task 1 — PostgreSQL scripts
│   ├── 01_schema_ddl.sql        # CREATE TABLE, PK, FK, constraints
│   └── 02_seed_dml.sql          # INSERT dummy test data
│
├── docs/                        # Task 3 — Documentation & API tests
│   ├── Design_Thinking_Proyecto_2_Revisado.pdf
│   ├── erd.png                  # Entity-Relationship Diagram
│   ├── technical_report.md      # DB & API summary
│   ├── openapi.json             # Exported from /openapi.json
│   └── postman_collection.json  # Postman / Insomnia collection
│
└── tests/                       # Automated API tests (pytest)
    ├── test_users.py
    ├── test_vinyls_services.py
    └── test_reservations.py
```

### Key Guidelines
1. **One FastAPI app (`main.py`):** Per `SCOPE.md`, Mobile and Desktop share one API. Keep `main.py` at the root and split endpoints into `app/routers/` (instead of separate `movil/` and `desktop/` apps).
2. **One entity per file:** Separating `user`, `vinyl`, `service`, and `reservation` avoids Git merge conflicts between Victor, Qingfei, and Eric.
3. **JSON prototype -> PostgreSQL:** Current prototype files (`vinyl.py`, `vinyl_ddbb.json`, `movil/vinyl_api.py`) can be moved into `app/models/`, `app/schemas/`, and `app/routers/` once PostgreSQL is connected.

---

## Español

Una estructura sencilla y sin conflictos, alineada con `SCOPE.md` y `TASK.md` para que cada miembro del equipo trabaje en sus propios archivos.

```text
VinylLab/
├── main.py                      # Punto de entrada único de FastAPI (registra los routers)
├── requirements.txt             # Dependencias de Python
├── .env.example                 # Variables de entorno de ejemplo (DATABASE_URL)
├── .gitignore
├── README.md
├── SCOPE.md
├── TASK.md
│
├── app/                         # Aplicación backend
│   ├── __init__.py
│   ├── database.py              # Conexión a PostgreSQL y get_db()
│   ├── models/                  # Modelos de base de datos (1 archivo por entidad)
│   │   ├── __init__.py
│   │   ├── user.py              # Usuarios / Clientes (Qingfei)
│   │   ├── vinyl.py             # Vinilos (Victor)
│   │   ├── service.py           # Servicios (Victor)
│   │   └── reservation.py       # Reservas (Eric)
│   ├── schemas/                 # Esquemas Pydantic (petición / respuesta)
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── vinyl.py
│   │   ├── service.py
│   │   └── reservation.py
│   └── routers/                 # Endpoints de la API (FastAPI APIRouter)
│       ├── __init__.py
│       ├── auth.py              # Registro, login, contraseña (Qingfei)
│       ├── users.py             # Perfil y CRUD de clientes (Qingfei)
│       ├── vinyls.py            # Endpoints de vinilos (Victor)
│       ├── services.py          # Endpoints de servicios (Victor)
│       └── reservations.py      # Reservas y control de franjas (Eric)
│
├── sql/                         # Tarea 1 — Scripts de PostgreSQL
│   ├── 01_schema_ddl.sql        # CREATE TABLE, PK, FK, restricciones
│   └── 02_seed_dml.sql          # INSERT de datos de prueba
│
├── docs/                        # Tarea 3 — Documentación y pruebas de API
│   ├── Design_Thinking_Proyecto_2_Revisado.pdf
│   ├── erd.png                  # Diagrama Entidad-Relación
│   ├── technical_report.md      # Resumen de BD y API
│   ├── openapi.json             # Exportado desde /openapi.json
│   └── postman_collection.json  # Colección de Postman / Insomnia
│
└── tests/                       # Pruebas automáticas de la API (pytest)
    ├── test_users.py
    ├── test_vinyls_services.py
    └── test_reservations.py
```

### Reglas básicas
1. **Una única app FastAPI (`main.py`):** Según `SCOPE.md`, Móvil y Desktop comparten una sola API. Mantener `main.py` en la raíz y dividir los endpoints en `app/routers/` (en lugar de apps separadas en `movil/` y `desktop/`).
2. **Una entidad por archivo:** Separar `user`, `vinyl`, `service` y `reservation` evita conflictos de Git entre Victor, Qingfei y Eric.
3. **Prototipo JSON -> PostgreSQL:** Los archivos actuales del prototipo (`vinyl.py`, `vinyl_ddbb.json`, `movil/vinyl_api.py`) pueden integrarse en `app/models/`, `app/schemas/` y `app/routers/` al conectar PostgreSQL.
