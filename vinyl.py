from pydantic import BaseModel;

class Vinyl(BaseModel):
    id:     int;
    name:   str;
    author: str;
    price:  float;