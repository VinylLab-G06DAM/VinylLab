from fastapi import FastAPI, HTTPException;

from models.vinyl import *;

app = FastAPI();

#TEST
@app.get("/")
def introduction() -> None:
    return {"message": "Hello World!"};

#GET
@app.get("/getvinyls")
def getAll() -> list:
    return readVinyls();

@app.get("/getvinyls/{id}")
def getAll(id: int) -> Vinyl:
    items = readVinyls();
        
    for vinyl in items:
        if vinyl.id == id:
            return vinyl;

    raise HTTPException(status_code=404, detail="Vinyl not found");

#POST
@app.post("/postvinyl/{vinyl}")
def postVinyl(v: Vinyl):
    insertVinyl(v);

#PUT
@app.put("/putvinyl/{id}")
def updateVinyl(id: int, v: Vinyl):
    for v in readVinyls():
        if v.id == id:
            updateVinyl(v);

            return;

    raise HTTPException(status_code=404, detail="Vinyl not found");