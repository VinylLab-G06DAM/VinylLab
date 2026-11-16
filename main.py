import json;
from fastapi import FastAPI, HTTPException;

app = FastAPI();

@app.get("/")
def introduction():
    return {"message": "Hello World!"};