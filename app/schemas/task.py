from typing import Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel

class TaskBase(BaseModel):
    name: str
    type: str
    platform: str
    config: Dict[str, Any]
    account_id: int

class TaskCreate(TaskBase):
    pass

class TaskUpdate(TaskBase):
    name: Optional[str] = None
    type: Optional[str] = None
    platform: Optional[str] = None
    config: Optional[Dict[str, Any]] = None
    status: Optional[str] = None

class TaskInDBBase(TaskBase):
    id: int
    status: str
    created_at: datetime
    updated_at: datetime
    user_id: int

    class Config:
        orm_mode = True

class Task(TaskInDBBase):
    pass 