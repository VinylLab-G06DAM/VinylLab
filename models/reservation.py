from pydantic import BaseModel


class Reservation(BaseModel):
    """Reservation schema shared across mobile and desktop APIs."""

    id: int
    client_id: int
    service_id: int
    date: str
    time_slot: str
    status: str = "confirmed"
