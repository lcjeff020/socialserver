"""
内容发布API模块

提供内容管理相关的端点：
1. 创建内容
2. 更新内容
3. 删除内容
4. 获取内容列表
5. 内容发布控制
"""

from typing import Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session

from app import models, schemas
from app.api import deps
from app.services.content_service import ContentService
from app.utils.logger import logger

router = APIRouter()
content_service = ContentService()

@router.post("/", response_model=schemas.Post)
async def create_post(
    *,
    db: Session = Depends(deps.get_db),
    post_in: schemas.PostCreate,
    files: Optional[List[UploadFile]] = File(None),
    current_user: models.User = Depends(deps.get_current_user)
) -> Any:
    """
    创建新内容
    """
    try:
        post = await content_service.create_content(
            db=db,
            content_data=post_in,
            media_files=files or [],
            user=current_user
        )
        return post
    except Exception as e:
        logger.error(f"Create post error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.get("/", response_model=List[schemas.Post])
async def get_posts(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    status: Optional[str] = None,
    platform: Optional[str] = None,
    current_user: models.User = Depends(deps.get_current_user)
) -> Any:
    """
    获取内容列表
    """
    try:
        posts = await content_service.get_user_posts(
            db=db,
            user=current_user,
            skip=skip,
            limit=limit,
            status=status,
            platform=platform
        )
        return posts
    except Exception as e:
        logger.error(f"Get posts error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.put("/{post_id}", response_model=schemas.Post)
async def update_post(
    *,
    db: Session = Depends(deps.get_db),
    post_id: int,
    post_in: schemas.PostUpdate,
    current_user: models.User = Depends(deps.get_current_user)
) -> Any:
    """
    更新内容
    """
    post = await content_service.get_post(db=db, post_id=post_id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )
    if post.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    try:
        post = await content_service.update_post(
            db=db, 
            post=post,
            post_in=post_in
        )
        return post
    except Exception as e:
        logger.error(f"Update post error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.delete("/{post_id}")
async def delete_post(
    *,
    db: Session = Depends(deps.get_db),
    post_id: int,
    current_user: models.User = Depends(deps.get_current_user)
) -> Any:
    """
    删除内容
    """
    post = await content_service.get_post(db=db, post_id=post_id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )
    if post.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    try:
        await content_service.delete_post(db=db, post_id=post_id)
        return {"msg": "Post deleted successfully"}
    except Exception as e:
        logger.error(f"Delete post error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.post("/{post_id}/publish")
async def publish_post(
    *,
    db: Session = Depends(deps.get_db),
    post_id: int,
    current_user: models.User = Depends(deps.get_current_user)
) -> Any:
    """
    立即发布内容
    """
    post = await content_service.get_post(db=db, post_id=post_id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )
    if post.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    try:
        result = await content_service.publish_post(db=db, post_id=post_id)
        return result
    except Exception as e:
        logger.error(f"Publish post error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        ) 