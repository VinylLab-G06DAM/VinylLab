from fastapi import FastAPI, HTTPException;

from models.service import *;

app = FastAPI();

#TEST
@app.get("/")
def introduction() -> None:
    return {"message": "Hello World!"};

#GET
@app.get("/getallservices")
def getServices() -> list:
    try:
        return readServices();
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e;