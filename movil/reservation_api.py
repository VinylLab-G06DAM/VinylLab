from fastapi import FastAPI, HTTPException

from models.reservation import Reservation, insertReservation, readReservations, updateReservation
from models.user import get_user_or_404

app = FastAPI()


#TEST
@app.get("/")
def introduction() -> dict:
    return {"message": "VinylLab Mobile - Reservations API"}


#GET
@app.get("/getreservations")
def getMine(client_id: int) -> list[Reservation]:
    get_user_or_404(client_id)
    return [r for r in readReservations() if r.client_id == client_id]


#POST
@app.post("/postreservation", status_code=201)
def postReservation(r: Reservation) -> Reservation:
    get_user_or_404(r.client_id)

    # A client can't create an already confirmed or finished reservation.
    r.status = "PENDING"
    return insertReservation(r)


#PUT
@app.put("/putreservation/{id}")
def putReservation(id: int, r: Reservation) -> Reservation:
    for current in readReservations():
        if current.id == id:
            if current.client_id != r.client_id:
                raise HTTPException(status_code=403, detail="Reservation belongs to another client")

            if current.status not in ("PENDING", "CONFIRMED"):
                raise HTTPException(status_code=400, detail="Reservation can no longer be changed")

            # The client can only keep the current status or cancel.
            if r.status not in (current.status, "CANCELLED"):
                raise HTTPException(status_code=400, detail="Status can only be changed to CANCELLED")

            return updateReservation(id, r)

    raise HTTPException(status_code=404, detail="Reservation not found")
