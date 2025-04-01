"""
API依赖模块
"""

from typing import Generator
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from sqlalchemy.orm import Session
from app.db.session import get_mysql_db, get_postgres_db, SessionLocal
from app.core.config import settings
from app import models
from app.schemas.common import ResponseModel
import logging

logger = logging.getLogger(__name__)

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/auth/login"
)

def get_db() -> Generator:
    """获取默认数据库会话"""
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

async def get_analytics_dbs(
    mysql_db: Session = Depends(get_mysql_db),
    postgres_db: Session = Depends(get_postgres_db)
):
    """获取两个数据库的会话"""
    return mysql_db, postgres_db

async def get_current_user(
    db: Session = Depends(get_mysql_db),
    token: str = Depends(oauth2_scheme)
) -> models.User:
    """获取当前用户"""
    # 定义一个HTTPException，当无法验证凭证时抛出
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # 使用jwt.decode函数解码token，获取payload
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        # 从payload中获取用户id
        user_id: int = payload.get("sub")
        # 如果用户id不存在，抛出credentials_exception
        if user_id is None:
            raise credentials_exception
    except jwt.JWTError:
        # 如果解码token出错，抛出credentials_exception
        raise credentials_exception
        
    # 从数据库中查询用户信息
    user = db.query(models.User).filter(models.User.id == user_id).first()
    # 如果用户不存在，抛出credentials_exception
    if user is None:
        raise credentials_exception
    # 返回用户信息
    return user 