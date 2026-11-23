from datetime import date, time

from fastapi import HTTPException
from pydantic import BaseModel

from data.json_db import read_collection, write_collection

RESERVATIONS_FILE = "reservations_ddbb.json"
RESERVATIONS_KEY = "reservations"


class Reservation(BaseModel):
    """Reservation schema shared across mobile and desktop APIs (same names as the SQL table)."""

    id: int
    client_id: int
    service_id: int
    reservation_date: date
    starts_at: time
    ends_at: time
    status: str = "PENDING"
    notes: str | None = None


def readReservations() -> list[Reservation]:
    return [Reservation.model_validate(item) for item in read_collection(RESERVATIONS_FILE, RESERVATIONS_KEY)]


def saveReservations(reservations: list[Reservation]) -> None:
    write_collection(RESERVATIONS_FILE, RESERVATIONS_KEY, [r.model_dump(mode="json") for r in reservations])


def insertReservation(r: Reservation) -> Reservation:
    reservations = readReservations()

    if r.starts_at >= r.ends_at:
        raise HTTPException(status_code=400, detail="Invalid time range")

    # Two active reservations can't overlap on the same day.
    for other in reservations:
        if (other.status in ("PENDING", "CONFIRMED")
                and other.reservation_date == r.reservation_date
                and r.starts_at < other.ends_at
                and other.starts_at < r.ends_at):
            raise HTTPException(status_code=409, detail="Slot not available")

    r.id = max((other.id for other in reservations), default=0) + 1
    reservations.append(r)
    saveReservations(reservations)
    return r
