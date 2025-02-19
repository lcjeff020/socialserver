"""
认证API模块

提供认证相关的API端点：
1. 用户注册
2. 用户登录
3. Token刷新
4. 密码重置
"""

from datetime import timedelta
from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app import schemas, models
from app.api import deps
from app.core.config import settings
from app.services.auth import AuthService
from app.utils.logger import logger

router = APIRouter()
auth_service = AuthService()

@router.post("/register", response_model=schemas.User)
async def register(
    *,
    db: Session = Depends(deps.get_db),
    user_in: schemas.UserCreate,
) -> Any:
    """
    注册新用户
    """
    try:
        user = await auth_service.register_user(db, user_in)
        return user
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Registration error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error registering user"
        )

@router.post("/login", response_model=schemas.Token)
async def login(
    db: Session = Depends(deps.get_db),
    form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """
    OAuth2 兼容的token登录，获取访问令牌
    """
    user = auth_service.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    elif not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth_service.create_access_token(
        data={"sub": user.email},
        expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

@router.post("/password-reset-request")
async def password_reset_request(
    email: str,
    db: Session = Depends(deps.get_db)
) -> Any:
    """
    请求密码重置
    """
    user = db.query(models.User).filter(models.User.email == email).first()
    if user:
        # TODO: 发送密码重置邮件
        pass
    return {"msg": "If email exists, password reset instructions will be sent"} 