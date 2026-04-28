from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class TodoBase(BaseModel):
    title: str
    description: Optional[str] = None
    is_completed: bool = False
    deadline: Optional[datetime] = None

class TodoCreate(TodoBase):
    pass

class TodoResponse(TodoBase):
    id: str

    class Config:
        from_attributes = True