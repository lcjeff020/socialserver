"""
内容发布相关的Pydantic模型
"""

from typing import List, Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel

class PostBase(BaseModel):
    title: str
    content: str
    platforms: List[str]  # ["tiktok", "instagram"]
    schedule_time: Optional[datetime] = None
    tags: Optional[List[str]] = []
    config: Optional[Dict[str, Any]] = {}

class PostCreate(PostBase):
    publish_now: Optional[bool] = False

class PostUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    platforms: Optional[List[str]] = None
    schedule_time: Optional[datetime] = None
    tags: Optional[List[str]] = None
    config: Optional[Dict[str, Any]] = None

class PostInDBBase(PostBase):
    id: int
    user_id: int
    status: str  # draft, scheduled, published, failed
    created_at: datetime
    updated_at: datetime
    media_urls: List[str]
    analytics: Optional[Dict[str, Any]] = {}

    class Config:
        from_attributes = True

class Post(PostInDBBase):
    pass 