from fastapi import FastAPI, HTTPException

from models.reservation import (
    Reservation,
    deleteReservation,
    insertReservation,
    readReservations,
    updateReservation,
)

app = FastAPI()


#GET
@app.get("/getreservations")
def getAll() -> list[Reservation]:
    return readReservations()


@app.get("/getreservations/{id}")
def getOne(id: int) -> Reservation:
    for reservation in readReservations():
        if reservation.id == id:
            return reservation

    raise HTTPException(status_code=404, detail="Reservation not found")


#POST
@app.post("/postreservation", status_code=201)
def postReservation(r: Reservation) -> Reservation:
    return insertReservation(r)


#PUT
@app.put("/putreservation/{id}")
def putReservation(id: int, r: Reservation) -> Reservation:
    return updateReservation(id, r)


#DELETE
@app.delete("/deletereservation/{id}")
def removeReservation(id: int) -> dict:
    deleteReservation(id)
    return {"message": "Reservation deleted"}
