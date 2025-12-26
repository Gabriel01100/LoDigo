from pydantic import BaseModel

class SchoolBase(BaseModel):
    name : str
    location : str | None

class SchoolCreate(SchoolBase):
    pass

class SchoolResponse(SchoolBase):
    id:int
    model_config = {
        "from_attributes": True
    }