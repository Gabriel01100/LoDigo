from pydantic import BaseModel, field_validator, Field
from datetime import datetime
from typing import Optional

class PostBase(BaseModel):
    title: Optional[str] = None
    content: str
    school_id: Optional[int] = None

    @field_validator("content")
    @classmethod
    def validate_content(cls, v: str):
        v = v.strip()
        if not v:
            raise ValueError("El contenido no puede estar vacío.")
        
        if len(v) < 5:
            raise ValueError("Contenido demasiado corto.")
        
        if len(v) > 2000:
            raise ValueError("Contenido demasiado largo.")
        
        return v
    
    @field_validator("title")
    @classmethod
    def validate_title(cls, v:Optional[str]):
        if v and len(v) > 150:
            raise ValueError("Titulo demasiado largo.")
        return v

class PostCreate(PostBase):
    # title: str | None = Field(default=None, max_length=100)
    # content: str = Field(min_length=1, max_length=2000)
    # school_id: int
    pass

class PostUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    school_id: Optional[int] = None


class PostResponse(PostBase):
    id :int
    user_id: int
    created_at:datetime
    updated_at : datetime

    model_config = {
        "from_attributes": True
    }