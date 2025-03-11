from pydantic import BaseModel, Field

class Hotel(BaseModel):
    id: int | None = None
    title: str | None = None
    name: str | None = None

class Error(BaseModel):
    Error: str