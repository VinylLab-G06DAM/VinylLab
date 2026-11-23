from fastapi import FastAPI, HTTPException;

import json;

from pathlib import Path;

from vinyl import Vinyl;

app = FastAPI();

def readVinyls():
    VINYL_DDBB_PATH = Path("../").with_name("vinyl_ddbb.json");
    
    content = VINYL_DDBB_PATH.read_text(encoding="utf-8");
            
    if not content.strip():
        return [];
            
    return [Vinyl.model_validate(item) for item in json.loads(content)];

def insertVinyl(v: Vinyl):
    VINYL_DDBB_PATH = Path("../").with_name("vinyl_ddbb.json");

    data = json.loads(VINYL_DDBB_PATH.read_text(encoding="utf-8") or '{}');
    data.setdefault("vinyls", []).append(v.model_dump());

    VINYL_DDBB_PATH.write_text(json.dumps(data, indent=4), encoding="utf-8");

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

@app.post("/postvinyl/{vinyl}")
def postVinyl(v: Vinyl):
    insertVinyl(v);