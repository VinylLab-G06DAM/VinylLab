import json
from datetime import date, time
from pathlib import Path

from fastapi import HTTPException
from pydantic import BaseModel

RESERVATIONS_PATH = Path(__file__).resolve().parents[1] / "ddbb" / "reservations_ddbb.json"
RESERVATIONS_KEY = "reservations"


class Reservation(BaseModel):
    """Reservation schema shared across mobile and desktop APIs (same names as the SQL table)."""

    id: int = 0  # assigned by insertReservation
    client_id: int
    service_id: int
    reservation_date: date
    starts_at: time
    ends_at: time
    status: str = "PENDING"
    notes: str | None = None


def readReservations() -> list[Reservation]:
    if not RESERVATIONS_PATH.exists():
        return []

    content = RESERVATIONS_PATH.read_text(encoding="utf-8")
    if not content.strip():
        return []

    return [Reservation.model_validate(item) for item in json.loads(content).get(RESERVATIONS_KEY, [])]


def saveReservations(reservations: list[Reservation]) -> None:
    data = {RESERVATIONS_KEY: [r.model_dump(mode="json") for r in reservations]}
    RESERVATIONS_PATH.write_text(json.dumps(data, indent=4, ensure_ascii=False) + "\n", encoding="utf-8")


def findIndex(reservations: list[Reservation], id: int) -> int:
    for i, reservation in enumerate(reservations):
        if reservation.id == id:
            return i

    raise HTTPException(status_code=404, detail="Reservation not found")


def checkSlot(reservations: list[Reservation], r: Reservation) -> None:
    if r.starts_at >= r.ends_at:
        raise HTTPException(status_code=400, detail="Invalid time range")

    if r.status not in ("PENDING", "CONFIRMED"):
        return

    # Two active reservations can't overlap on the same day.
    for other in reservations:
        if (other.id != r.id
                and other.status in ("PENDING", "CONFIRMED")
                and other.reservation_date == r.reservation_date
                and r.starts_at < other.ends_at
                and other.starts_at < r.ends_at):
            raise HTTPException(status_code=409, detail="Slot not available")


def insertReservation(r: Reservation) -> Reservation:
    reservations = readReservations()

    r.id = max((other.id for other in reservations), default=0) + 1
    checkSlot(reservations, r)

    reservations.append(r)
    saveReservations(reservations)
    return r


def updateReservation(id: int, r: Reservation) -> Reservation:
    reservations = readReservations()
    index = findIndex(reservations, id)

    r.id = id
    checkSlot(reservations, r)

    reservations[index] = r
    saveReservations(reservations)
    return r


def deleteReservation(id: int) -> None:
    reservations = readReservations()
    reservations.pop(findIndex(reservations, id))
    saveReservations(reservations)
