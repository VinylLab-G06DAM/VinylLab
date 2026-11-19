# VinylLab — Project Scope (Backend, Database & Documentation)

This document defines the **current project scope** for **VinylLab**.  
At this stage, the scope is strictly limited to the **Database (PostgreSQL)**, the **RESTful API (FastAPI)** serving both the **Mobile** and **Desktop** applications, and **Technical Documentation & API Testing**.

> **Current Prototype Status:**  
> [main.py](main.py) and [ddbb.json](ddbb.json) are currently used for initial FastAPI experimentation. The production target database is **PostgreSQL**, and the initial endpoint draft is tracked in [notes.txt](notes.txt).

---

## In Scope vs. Out of Scope

- **In Scope:**
  - Relational database design and implementation in **PostgreSQL** (with dummy test data).
  - RESTful API built with **FastAPI** covering all required Mobile and Desktop operations.
  - Business validation rules (such as reservation slot control) and standard HTTP/JSON conventions.
  - Technical documentation and an exported API test collection / OpenAPI specification.
- **Out of Scope (Current Phase):**
  - Building the Mobile App UI and Desktop Admin Web UI (only the API and database supporting them are in scope).

---

## 1. Database Design & Implementation (Task 1 — PostgreSQL)

The database will be implemented in **PostgreSQL** following relational design best practices:

- **Entity-Relationship / Relational Model:**
  - Design the complete schema (e.g., via ERD tools) defining all tables, **Primary Keys (PK)**, **Foreign Keys (FK)**, and relationships.
  - Core entities identified so far in [notes.txt](notes.txt): `users` / `clients`, `vinyls`, `services`, and `reservations`.
- **Normalization & Data Types:**
  - Apply normalization rules to avoid data redundancy.
  - Choose appropriate PostgreSQL data types and constraints (`NOT NULL`, `UNIQUE`, `CHECK`, etc.) for each field.
- **SQL Scripts (DDL & DML):**
  - **DDL script:** `CREATE TABLE`, `ALTER TABLE`, and constraints (`PK`, `FK`, indexes, etc.).
  - **DML script:** `INSERT` statements to populate dummy test data.
- **Test-Ready Database:**
  - Ensure PostgreSQL is populated with dummy data so all endpoints can be tested immediately.

---

## 2. RESTful API Specification & Design (Task 2 — FastAPI)

The FastAPI backend acts as the single API serving two clients: **Mobile (Client)** and **Desktop (Administrator)**.

### Functional Modules

1. **User & Client Management**
   - **Mobile:** User registration, login, profile consultation, and profile editing (avatar, basic data, password change).
   - **Desktop:** Full client management (list all, get by ID, create, update, delete).
2. **Service & Vinyl Catalog**
   - **Mobile:** List available services and vinyls, view item details.
   - **Desktop:** Full catalog administration—create, modify, deactivate, or remove services and vinyls.
3. **Reservation & Agenda Management**
   - **Mobile:** Create a reservation, consult personal reservation history, and update/cancel a reservation.
   - **Desktop:** Consult the daily agenda, search/filter reservations by date or client, and create, modify, or delete reservations.
4. **Slot Control & Consistency (Shared Rule)**
   - Implement a centralized validation rule in the API (and database constraints/transactions where applicable) to verify time-slot availability and **prevent simultaneous double reservations**.

### API Format & Standards

- **Payload Format:** JSON for all requests and responses.
- **Parameters:** Clean separation of **Path** (`/vinyls/{id}`), **Query** (`?date=...&client_id=...`), and **Body** (Pydantic schemas) parameters.
- **HTTP Status Codes:**
  - `200 OK` — Successful read, update, or action.
  - `201 Created` — New resource successfully created.
  - `400 Bad Request` — Invalid request data or failed business rule.
  - `401 Unauthorized` — Missing or invalid authentication credentials.
  - `404 Not Found` — Requested resource ID does not exist.
  - `409 Conflict` — Duplicate record or overlapping/double-booked reservation slot.

---

## 3. Technical Documentation & API Testing (Task 3)

- **Technical Report:**
  - Concise explanation of all PostgreSQL tables, fields, and relationships.
  - Description of the main API endpoints, parameters, and validation rules.
- **API Test Collection / Specification:**
  - Exported **Postman** or **Insomnia** collection covering the endpoints and test cases.
  - **OpenAPI / Swagger** specification (`.json` / `.yaml`), which FastAPI automatically generates at `/openapi.json` and exposes interactively at `/docs` (see [README.md](README.md)).

---

## Alignment Notes with [notes.txt](notes.txt)

When expanding [notes.txt](notes.txt) into the full PostgreSQL + FastAPI implementation, make sure to include these requirements from Tasks 1–3 that are not yet detailed in [notes.txt](notes.txt):

- **Authentication & Profile endpoints:** `register`, `login`, `password change`, and `avatar` field/update.
- **Service deactivation:** Ability to deactivate a service (e.g., an `is_active` boolean) rather than only hard-deleting it.
- **Agenda filtering & cancellation:** Query parameters on reservations to filter by `date` and `client`, plus explicit reservation cancellation and slot-overlap checks (`409 Conflict`).
