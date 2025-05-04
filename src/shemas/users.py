from pydantic import BaseModel, ConfigDict


class UserAddRequest(BaseModel):
    login: str
    password: str
    
class UserAdd(BaseModel):
    login: str
    hashed_password: str
    
class User(BaseModel):
    id: int
    login: str
    
    model_config = ConfigDict(from_attributes=True)