from pydantic import BaseModel
from datetime import datetime

#usuario crea algo
class UserBase(BaseModel):
    role:str | None= "user"

#crear usuario anonimo
class UserCreate(BaseModel):
    anon_key:str

#Lo que se devuelve al cliente
class UserResponse(BaseModel):
    id: int
    role: str 
    created_at: datetime
    model_config = {
        "from_attributes": True
    }
