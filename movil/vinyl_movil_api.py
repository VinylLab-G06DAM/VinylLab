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
    try:
        return readVinyls();
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e;

@app.get("/getvinyls/{id}")
def getAll(id: int) -> Vinyl:
    try:
        items = readVinyls();
        
        for vinyl in items:
            if vinyl.id == id:
                return vinyl;

        raise HTTPException(status_code=404, detail="Vinyl not found");
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e;