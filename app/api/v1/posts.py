"""
内容发布相关的API路由
"""

from typing import Any, List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app import schemas
from app.api import deps
from app.services.content_service import ContentService
from app.schemas.common import ResponseModel
import logging

logger = logging.getLogger(__name__)
router = APIRouter()
content_service = ContentService()

@router.get("/", response_model=ResponseModel[List[schemas.Content]])
async def list_contents(
    db: Session = Depends(deps.get_mysql_db),
    skip: int = 0,
    limit: int = 100,
    current_user = Depends(deps.get_current_user)
) -> Any:
    """获取内容列表"""
    try:
        contents = await content_service.get_user_contents(
            db, user_id=current_user.id, skip=skip, limit=limit
        )
        return ResponseModel(
            code=200,
            msg="获取成功",
            data=contents
        )
    except Exception as e:
        logger.error(f"获取内容列表错误: {str(e)}")
        return ResponseModel(
            code=201,
            msg="获取内容列表失败",
            data={"error": f"{str(e)}"}
        )

@router.post("/", response_model=ResponseModel[schemas.Content])
async def create_content(
    *,
    db: Session = Depends(deps.get_mysql_db),
    content_in: schemas.ContentCreate,
    current_user = Depends(deps.get_current_user)
) -> Any:
    """创建新内容"""
    try:
        content = await content_service.create(
            db, obj_in=content_in, user_id=current_user.id
        )
        return ResponseModel(
            code=200,
            msg="创建成功",
            data=content
        )
    except Exception as e:
        logger.error(f"创建内容错误: {str(e)}")
        return ResponseModel(
            code=201,
            msg="创建内容失败",
            data={"error": f"{str(e)}"}
        )

@router.put("/{content_id}", response_model=ResponseModel[schemas.Content])
async def update_content(
    *,
    db: Session = Depends(deps.get_mysql_db),
    content_id: int,
    content_in: schemas.ContentUpdate,
    current_user = Depends(deps.get_current_user)
) -> Any:
    """更新内容"""
    try:
        content = await content_service.get(db, id=content_id)
        if not content or content.user_id != current_user.id:
            return ResponseModel(
                code=201,
                msg="内容不存在或无权限",
                data={}
            )
        
        content = await content_service.update(
            db, db_obj=content, obj_in=content_in
        )
        return ResponseModel(
            code=200,
            msg="更新成功",
            data=content
        )
    except Exception as e:
        logger.error(f"更新内容错误: {str(e)}")
        return ResponseModel(
            code=201,
            msg="更新内容失败",
            data={"error": f"{str(e)}"}
        )

@router.delete("/{content_id}", response_model=ResponseModel[dict])
async def delete_content(
    *,
    db: Session = Depends(deps.get_mysql_db),
    content_id: int,
    current_user = Depends(deps.get_current_user)
) -> Any:
    """删除内容"""
    try:
        content = await content_service.get(db, id=content_id)
        if not content or content.user_id != current_user.id:
            return ResponseModel(
                code=201,
                msg="内容不存在或无权限",
                data={}
            )
        
        await content_service.delete(db, id=content_id)
        return ResponseModel(
            code=200,
            msg="删除成功",
            data={"content_id": content_id}
        )
    except Exception as e:
        logger.error(f"删除内容错误: {str(e)}")
        return ResponseModel(
            code=201,
            msg="删除内容失败",
            data={"error": f"{str(e)}"}
        ) 