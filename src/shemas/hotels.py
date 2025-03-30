from pydantic import BaseModel, Field

class Hotel(BaseModel):
    title: str | None = None
    location: str | None = None
    
class HotelPATCH(BaseModel):
    title: str | None = None
    location: str | None = None

class Error(BaseModel):
    Error: str