"""
设备管理API模块

提供设备管理相关功能：
1. 设备注册和认证
2. 设备状态管理
3. 设备配置更新
4. 设备监控
"""

from typing import Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import models, schemas
from app.api import deps
from app.services.device_service import DeviceService
from app.utils.logger import logger

router = APIRouter()
device_service = DeviceService()

@router.post("/register", response_model=schemas.Device)
async def register_device(
    *,
    db: Session = Depends(deps.get_mysql_db),
    device_in: schemas.DeviceRegister,
    current_user: models.User = Depends(deps.get_current_user)
) -> Any:
    """注册新设备"""
    try:
        device = await device_service.register_device(
            db=db,
            device_in=device_in,
            user_id=current_user.id
        )
        return device
    except Exception as e:
        logger.error(f"Register device error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.get("/", response_model=List[schemas.Device])
async def get_devices(
    db: Session = Depends(deps.get_mysql_db),
    skip: int = 0,
    limit: int = 100,
    status: Optional[str] = None,
    current_user: models.User = Depends(deps.get_current_user)
) -> Any:
    """获取设备列表"""
    try:
        devices = await device_service.get_user_devices(
            db=db,
            user_id=current_user.id,
            skip=skip,
            limit=limit,
            status=status
        )
        return devices
    except Exception as e:
        logger.error(f"Get devices error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.put("/{device_id}/config", response_model=schemas.Device)
async def update_device_config(
    *,
    db: Session = Depends(deps.get_mysql_db),
    device_id: int,
    config_in: schemas.DeviceConfigUpdate,
    current_user: models.User = Depends(deps.get_current_user)
) -> Any:
    """更新设备配置"""
    device = await device_service.get_device(db=db, device_id=device_id)
    if not device or device.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Device not found"
        )
    try:
        device = await device_service.update_config(
            db=db,
            device=device,
            config_in=config_in
        )
        return device
    except Exception as e:
        logger.error(f"Update device config error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.post("/{device_id}/heartbeat")
async def device_heartbeat(
    *,
    db: Session = Depends(deps.get_mysql_db),
    device_id: int,
    heartbeat_in: schemas.DeviceHeartbeat
) -> Any:
    """设备心跳更新"""
    try:
        result = await device_service.update_heartbeat(
            db=db,
            device_id=device_id,
            heartbeat_in=heartbeat_in
        )
        return result
    except Exception as e:
        logger.error(f"Device heartbeat error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        ) 