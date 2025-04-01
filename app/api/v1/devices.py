"""
设备相关的API路由
"""

from typing import Any, List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app import schemas
from app.api import deps
from app.services.device_service import DeviceService
from app.schemas.common import ResponseModel
import logging

logger = logging.getLogger(__name__)
router = APIRouter()
device_service = DeviceService()

@router.get("/", response_model=ResponseModel[List[schemas.Device]])
async def list_devices(
    db: Session = Depends(deps.get_mysql_db),
    current_user = Depends(deps.get_current_user)
) -> Any:
    """获取用户的设备列表"""
    try:
        devices = await device_service.get_user_devices(db, user_id=current_user.id)
        return ResponseModel(
            code=200,
            msg="获取成功",
            data=devices
        )
    except Exception as e:
        logger.error(f"获取设备列表错误: {str(e)}")
        return ResponseModel(
            code=201,
            msg="获取设备列表失败",
            data={"error": f"{str(e)}"}
        )

@router.post("/register", response_model=ResponseModel[schemas.Device])
async def register_device(
    *,
    db: Session = Depends(deps.get_mysql_db),
    device_in: schemas.DeviceRegister,
    current_user = Depends(deps.get_current_user)
) -> Any:
    """注册新设备"""
    try:
        device = await device_service.register_device(
            db, device_in=device_in, user_id=current_user.id
        )
        return ResponseModel(
            code=200,
            msg="注册成功",
            data=device
        )
    except Exception as e:
        logger.error(f"注册设备错误: {str(e)}")
        return ResponseModel(
            code=201,
            msg="注册设备失败",
            data={"error": f"{str(e)}"}
        )

@router.put("/{device_id}/config", response_model=ResponseModel[schemas.Device])
async def update_device_config(
    *,
    db: Session = Depends(deps.get_mysql_db),
    device_id: str,
    config_in: schemas.DeviceConfigUpdate,
    current_user = Depends(deps.get_current_user)
) -> Any:
    """更新设备配置"""
    try:
        device = await device_service.get_device(db, device_id=device_id)
        if not device or device.user_id != current_user.id:
            return ResponseModel(
                code=201,
                msg="设备不存在或无权限",
                data={}
            )
        
        device = await device_service.update_config(db, device=device, config=config_in.config)
        return ResponseModel(
            code=200,
            msg="更新成功",
            data=device
        )
    except Exception as e:
        logger.error(f"更新设备配置错误: {str(e)}")
        return ResponseModel(
            code=201,
            msg="更新设备配置失败",
            data={"error": f"{str(e)}"}
        )

@router.post("/{device_id}/heartbeat", response_model=ResponseModel[dict])
async def device_heartbeat(
    *,
    db: Session = Depends(deps.get_mysql_db),
    device_id: str,
    heartbeat_in: schemas.DeviceHeartbeat
) -> Any:
    """设备心跳"""
    try:
        await device_service.update_heartbeat(
            db, device_id=device_id, status=heartbeat_in.status
        )
        return ResponseModel(
            code=200,
            msg="心跳更新成功",
            data={"device_id": device_id}
        )
    except Exception as e:
        logger.error(f"设备心跳更新错误: {str(e)}")
        return ResponseModel(
            code=201,
            msg="心跳更新失败",
            data={"error": f"{str(e)}"}
        ) 