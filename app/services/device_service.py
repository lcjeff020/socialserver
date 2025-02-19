from typing import List, Optional
from datetime import datetime
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app import models, schemas

class DeviceService:
    async def register_device(
        self,
        db: Session,
        device_data: schemas.DeviceCreate,
        user: models.User
    ) -> models.Device:
        # 检查设备是否已存在
        existing_device = (
            db.query(models.Device)
            .filter(models.Device.device_id == device_data.device_id)
            .first()
        )
        if existing_device:
            raise HTTPException(
                status_code=400,
                detail="Device already registered"
            )
        
        device = models.Device(
            name=device_data.name,
            device_id=device_data.device_id,
            user_id=user.id
        )
        db.add(device)
        db.commit()
        db.refresh(device)
        return device

    async def update_device_status(
        self,
        db: Session,
        device_id: str,
        status: str
    ) -> models.Device:
        device = (
            db.query(models.Device)
            .filter(models.Device.device_id == device_id)
            .first()
        )
        if not device:
            raise HTTPException(
                status_code=404,
                detail="Device not found"
            )
        
        device.status = status
        device.last_seen = datetime.utcnow()
        db.commit()
        db.refresh(device)
        return device 