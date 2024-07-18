from pydantic import BaseModel, Field, constr
from uuid import UUID
from typing import Dict, Any


class ApplicationBase(BaseModel):
    kind: str
    name: str
    version: str
    description: str
    state: str
    json_data: Dict[str, Any] = Field(default_factory=dict)
    
    class Config:
        orm_mode = True
        

class CreateApplication(ApplicationBase):
    class Config:
        orm_mode = True
        

class ApplicationResponse(ApplicationBase):
    id: UUID
    class Config:
        orm_mode = True
        json_encoders = {
            UUID: str,
        }