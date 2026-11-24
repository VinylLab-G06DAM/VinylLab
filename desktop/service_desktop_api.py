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

#POST
@app.post("/postservice/{service}")
def postService(s: Service) -> None:
    try:
        insertService(s);
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e;

#PUT
@app.put("/putservice/{id}")
def putService(id:int, s: Service) -> None:
    try:
        updateService(id, s);
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e;

#DELETE
@app.delete("/deleteservice/{id}")
def delService(id: int) -> None:
    try:
        deleteService(id);
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e;
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e;