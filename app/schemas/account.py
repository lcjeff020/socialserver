"""
账号相关的Pydantic模型
"""

from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import BaseModel, HttpUrl

class AccountBase(BaseModel):
    platform: str
    username: str
    profile_url: HttpUrl
    is_active: bool = True
    platform_id: Optional[str] = None
    description: Optional[str] = None
    avatar_url: Optional[HttpUrl] = None
    config: Optional[Dict[str, Any]] = {}

class AccountCreate(AccountBase):
    access_token: str
    refresh_token: Optional[str] = None
    token_expires_at: Optional[datetime] = None

class AccountUpdate(BaseModel):
    username: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None
    config: Optional[Dict[str, Any]] = None
    access_token: Optional[str] = None
    refresh_token: Optional[str] = None
    token_expires_at: Optional[datetime] = None

class AccountInDBBase(AccountBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
    followers_count: Optional[int] = 0
    following_count: Optional[int] = 0
    total_posts: Optional[int] = 0

    class Config:
        from_attributes = True

class Account(AccountInDBBase):
    pass 