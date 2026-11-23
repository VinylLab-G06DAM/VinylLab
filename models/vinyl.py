from pydantic import BaseModel


class Vinyl(BaseModel):
    """Vinyl record schema shared across mobile and desktop APIs."""

    id: int
    name: str
    author: str
    price: float
