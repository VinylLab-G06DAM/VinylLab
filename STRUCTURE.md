# VinylLab — Recommended File Structure / Estructura de Archivos Recomendada

---

## English

A simple structure adapted to the team's decision: **separate Phone (`movil/`) and Desktop (`desktop/`) API logic first, using JSON files (`data/`) as storage** before migrating to PostgreSQL.

```text
VinylLab/
├── requirements.txt             # Python dependencies
├── .gitignore
├── README.md
├── SCOPE.md
├── TASK.md
├── STRUCTURE.md
│
├── models/                      # Shared Pydantic models (used by both movil & desktop)
│   ├── __init__.py
│   ├── user.py                  # User / Client model (Qingfei)
│   ├── vinyl.py                 # Vinyl model (Victor)
│   ├── service.py               # Service model (Victor)
│   └── reservation.py           # Reservation model (Eric)
│
├── data/                        # Temporary JSON databases (before PostgreSQL)
│   ├── json_db.py               # Shared JSON read/write helper
│   ├── users_ddbb.json
│   ├── vinyl_ddbb.json
│   ├── services_ddbb.json
│   └── reservations_ddbb.json
│
├── movil/                       # Mobile (Phone) API endpoints & logic
│   ├── __init__.py
│   ├── main.py                  # Mobile FastAPI app (`uvicorn movil.main:app --reload`)
│   ├── user_api.py              # (Qingfei)
│   ├── vinyl_api.py             # (Victor)
│   ├── service_api.py           # (Victor)
│   └── reservation_api.py       # (Eric)
│
├── desktop/                     # Desktop (Admin) API endpoints & logic
│   ├── __init__.py
│   ├── main.py                  # Desktop FastAPI app (`uvicorn desktop.main:app --reload`)
│   ├── client_api.py            # (Qingfei)
│   ├── vinyl_api.py             # (Victor)
│   ├── service_api.py           # (Victor)
│   └── reservation_api.py       # (Eric)
│
├── sql/                         # Later: PostgreSQL DDL & DML scripts (Task 1)
├── docs/                        # Documentation, ERD, OpenAPI & Postman collection (Task 3)
│   └── Design_Thinking_Proyecto_2_Revisado.pdf
└── tests/                       # Automated API tests (pytest)
```

### Key Guidelines
1. **Separate `movil/` and `desktop/`:** Each client has its own endpoints and logic (`movil/main.py` and `desktop/main.py`), while sharing the same `models/` and `data/*.json` files.
2. **One entity per file:** Keeping `user`, `vinyl`, `service`, and `reservation` in separate files prevents Git conflicts between Victor, Qingfei, and Eric.
3. **JSON first, PostgreSQL later:** Both `movil/` and `desktop/` read and write the same JSON files inside `data/`. When moving to PostgreSQL later, only the data-access functions need to change.

---

## Español

Una estructura sencilla adaptada a la decisión del equipo: **separar primero la lógica de Móvil (`movil/`) y Escritorio (`desktop/`), trabajando con archivos JSON (`data/`)** antes de migrar a PostgreSQL.

```text
VinylLab/
├── requirements.txt             # Dependencias de Python
├── .gitignore
├── README.md
├── SCOPE.md
├── TASK.md
├── STRUCTURE.md
│
├── models/                      # Modelos Pydantic compartidos (para movil y desktop)
│   ├── __init__.py
│   ├── user.py                  # Modelo User / Client (Qingfei)
│   ├── vinyl.py                 # Modelo Vinyl (Victor)
│   ├── service.py               # Modelo Service (Victor)
│   └── reservation.py           # Modelo Reservation (Eric)
│
├── data/                        # Bases de datos JSON temporales (antes de PostgreSQL)
│   ├── json_db.py               # Helper compartido para leer/escribir JSON
│   ├── users_ddbb.json
│   ├── vinyl_ddbb.json
│   ├── services_ddbb.json
│   └── reservations_ddbb.json
│
├── movil/                       # Endpoints y lógica de la API Móvil
│   ├── __init__.py
│   ├── main.py                  # App FastAPI móvil (`uvicorn movil.main:app --reload`)
│   ├── user_api.py              # (Qingfei)
│   ├── vinyl_api.py             # (Victor)
│   ├── service_api.py           # (Victor)
│   └── reservation_api.py       # (Eric)
│
├── desktop/                     # Endpoints y lógica de la API Escritorio (Admin)
│   ├── __init__.py
│   ├── main.py                  # App FastAPI escritorio (`uvicorn desktop.main:app --reload`)
│   ├── client_api.py            # (Qingfei)
│   ├── vinyl_api.py             # (Victor)
│   ├── service_api.py           # (Victor)
│   └── reservation_api.py       # (Eric)
│
├── sql/                         # Más adelante: scripts DDL y DML de PostgreSQL (Tarea 1)
├── docs/                        # Documentación, ERD, OpenAPI y colección Postman (Tarea 3)
│   └── Design_Thinking_Proyecto_2_Revisado.pdf
└── tests/                       # Pruebas automáticas de la API (pytest)
```

### Reglas básicas
1. **Separar `movil/` y `desktop/`:** Cada cliente tiene sus propios endpoints y lógica (`movil/main.py` y `desktop/main.py`), pero ambos comparten `models/` y los mismos archivos JSON en `data/`.
2. **Una entidad por archivo:** Separar `user`, `vinyl`, `service` y `reservation` evita conflictos de Git entre Victor, Qingfei y Eric.
3. **Primero JSON, luego PostgreSQL:** Tanto `movil/` como `desktop/` leen y escriben los mismos JSON en `data/`. Al pasar a PostgreSQL más adelante, solo habrá que cambiar las funciones de lectura/escritura.
