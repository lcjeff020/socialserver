"""
团队相关的Pydantic模型
"""

from typing import Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel

class TeamBase(BaseModel):
    name: str
    description: Optional[str] = None
    is_active: bool = True
    config: Optional[Dict[str, Any]] = {}

class TeamCreate(TeamBase):
    pass

class TeamUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None
    config: Optional[Dict[str, Any]] = None

class TeamInDBBase(TeamBase):
    id: int
    owner_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class Team(TeamInDBBase):
    pass

class TeamMemberCreate(BaseModel):
    user_id: int
    role: str = "member"

class TeamMember(TeamMemberCreate):
    id: int
    team_id: int
    created_at: datetime

    class Config:
        orm_mode = True 