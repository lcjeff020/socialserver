"""
内容相关的Pydantic模型
"""

from typing import Optional, Dict, Any, List
from datetime import datetime
from pydantic import BaseModel, HttpUrl

class ContentBase(BaseModel):
    title: str
    content: str
    content_type: str  # text, image, video
    platform: str
    status: str = "draft"
    scheduled_time: Optional[datetime] = None
    metadata: Optional[Dict[str, Any]] = {}

class ContentCreate(ContentBase):
    account_id: int
    media_urls: Optional[List[HttpUrl]] = None

class ContentUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    status: Optional[str] = None
    scheduled_time: Optional[datetime] = None
    metadata: Optional[Dict[str, Any]] = None

class ContentInDBBase(ContentBase):
    id: int
    user_id: int
    account_id: int
    created_at: datetime
    updated_at: datetime
    published_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class Content(ContentInDBBase):
    pass 