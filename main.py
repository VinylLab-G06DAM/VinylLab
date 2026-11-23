import json;
from fastapi import FastAPI, HTTPException;

from pathlib import Path;
from pydantic import BaseModel;

app = FastAPI();

DDBB_PATH = Path(__file__).with_name("ddbb.json");

class Vinyl(BaseModel):
    id: int;
    name: str;
    author: str;

def load() -> list:
    content = DDBB_PATH.read_text(encoding="utf-8");

    if not content.strip():
        return [];

    return [Vinyl.model_validate(item) for item in json.loads(content)];

items = load();

@app.get("/")
def introduction() -> None:
    return {"message": "Hello World!"};

@app.get("/get")
def getAll() -> list:
    return items;

@app.get("/get/{id}")
def getAll(id: int) -> Vinyl:
    for vinyl in items:
        if vinyl.id == id:
            return vinyl;

    raise HTTPException(status_code=404, detail="Vinyl not found");

@app.delete("/delete/{id}")
def delete(id: int) -> Vinyl:
    for vinyl in items:
        if vinyl.id == id:
            items.remove(vinyl);
            return vinyl;

    raise HTTPException(status_code=404, detail="Vinyl not found");