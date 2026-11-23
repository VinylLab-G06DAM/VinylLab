from fastapi import FastAPI

from models.user import (
    ClientCreate,
    ClientUpdate,
    UserPublic,
    create_user_record,
    delete_user_record,
    get_user_or_404,
    read_users,
    to_public,
    update_user_record,
)

app = FastAPI(title="VinylLab Desktop - Clients API")


@app.get("/")
def introduction() -> dict[str, str]:
    """Health check endpoint for Desktop Clients API."""
    return {"message": "VinylLab Desktop Clients API"}


@app.get("/clients", response_model=list[UserPublic])
def get_all_clients() -> list[UserPublic]:
    """List all registered clients."""
    return [to_public(user) for user in read_users()]


@app.get("/clients/{client_id}", response_model=UserPublic)
def get_client(client_id: int) -> UserPublic:
    """Retrieve a client by ID."""
    return to_public(get_user_or_404(client_id))


@app.post("/clients", status_code=201, response_model=UserPublic)
def create_client(payload: ClientCreate) -> UserPublic:
    """Create a new client from the desktop admin panel."""
    record = create_user_record(
        name=payload.name,
        email=payload.email,
        password=payload.password,
        phone=payload.phone,
        avatar=payload.avatar,
        is_active=payload.is_active,
        explicit_id=payload.id,
    )
    return to_public(record)


@app.put("/clients/{client_id}", response_model=UserPublic)
def update_client(client_id: int, payload: ClientUpdate) -> UserPublic:
    """Update an existing client from the desktop admin panel."""
    updated = update_user_record(client_id, payload.model_dump(exclude_unset=True))
    return to_public(updated)


@app.delete("/clients/{client_id}")
def delete_client(client_id: int) -> dict[str, object]:
    """Delete a client by ID."""
    deleted = delete_user_record(client_id)
    return {"message": "Client deleted", "client": to_public(deleted)}
