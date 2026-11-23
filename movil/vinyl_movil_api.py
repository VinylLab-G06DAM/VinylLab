from fastapi import FastAPI, HTTPException;

from vinyl import *;

app = FastAPI();

@app.get("/")
def introduction() -> None:
    return {"message": "Hello World!"};

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