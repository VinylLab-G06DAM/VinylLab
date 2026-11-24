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

#POST
@app.post("/postvinyl/{vinyl}")
def postVinyl(v: Vinyl) -> None:
    try:
        insertVinyl(v);
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e;

#PUT
@app.put("/putvinyl/{id}")
def putVinyl(id: int, v: Vinyl) -> None:
    try:
        updateVinyl(id, v);
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e;
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e;

#DELETE
@app.delete("/deletevinyl/{id}")
def delVinyl(id: int) -> None:
    try:
        deleteVinyl(id);
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e;
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e;