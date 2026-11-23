from fastapi import FastAPI, HTTPException

from models.reservation import Reservation, insertReservation, readReservations

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
