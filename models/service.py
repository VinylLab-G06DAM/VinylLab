from pydantic import BaseModel


class Service(BaseModel):
    """Catalog service schema shared across mobile and desktop APIs."""

    id: int
    name: str
    description: str = ""
    price: float
    is_active: bool = True
