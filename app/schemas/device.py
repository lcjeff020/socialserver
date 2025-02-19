"""
设备相关的Pydantic模型
"""

from typing import Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel

class DeviceBase(BaseModel):
    name: str
    device_type: str
    status: str = "active"
    is_online: bool = True
    config: Optional[Dict[str, Any]] = {}

class DeviceRegister(DeviceBase):
    device_id: str
    secret_key: str

class DeviceCreate(DeviceBase):
    user_id: int
    device_id: str
    secret_key: str

class DeviceUpdate(BaseModel):
    name: Optional[str] = None
    status: Optional[str] = None
    is_online: Optional[bool] = None
    config: Optional[Dict[str, Any]] = None

class DeviceConfigUpdate(BaseModel):
    config: Dict[str, Any]

class DeviceHeartbeat(BaseModel):
    device_id: str
    status: str
    metrics: Optional[Dict[str, Any]] = None

class DeviceInDBBase(DeviceBase):
    id: int
    user_id: int
    device_id: str
    created_at: datetime
    updated_at: datetime
    last_active: Optional[datetime] = None

    class Config:
        from_attributes = True

class Device(DeviceInDBBase):
    pass 