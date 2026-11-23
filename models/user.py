from pydantic import BaseModel


class User(BaseModel):
    """User / client schema shared across mobile and desktop APIs."""

    id: int
    name: str
    email: str
    avatar: str | None = None
    is_active: bool = True
