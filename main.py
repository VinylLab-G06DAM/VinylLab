from fastapi import FastAPI, HTTPException;

import json;

from pathlib import Path;

from vinyl import Vinyl;

app = FastAPI();

def readVinyls(self):
    DDBB_PATH = Path(__file__).with_name("ddbb.json");
    
    content = DDBB_PATH.read_text(encoding="utf-8");
            
    if not content.strip():
        return [];
            
    return [Vinyl.model_validate(item) for item in json.loads(content)];

@app.get("/")
def introduction() -> None:
    return {"message": "Hello World!"};

@app.get("/get")
def getAll(self) -> list:
    return self.readVinyls();

@app.get("/get/{id}")
def getAll(self, id: int) -> Vinyl:
    items = self.readVinyls();
        
    for vinyl in items:
        if vinyl.id == id:
            return vinyl;

    raise HTTPException(status_code=404, detail="Vinyl not found");