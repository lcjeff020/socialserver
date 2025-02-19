"""
认证服务模块

处理用户认证相关的业务逻辑：
1. 用户注册
2. 用户登录
3. Token生成和验证
4. 密码加密和验证
5. 权限检查
"""

from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app import models, schemas
from app.core.config import settings
from app.utils.logger import logger

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AuthService:
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """验证密码"""
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def get_password_hash(password: str) -> str:
        """生成密码哈希"""
        return pwd_context.hash(password)

    @staticmethod
    def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
        """创建访问令牌"""
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm="HS256")
        return encoded_jwt

    def authenticate_user(self, db: Session, email: str, password: str) -> Optional[models.User]:
        """验证用户"""
        user = db.query(models.User).filter(models.User.email == email).first()
        if not user:
            return None
        if not self.verify_password(password, user.hashed_password):
            return None
        return user

    async def register_user(
        self, 
        db: Session, 
        user_create: schemas.UserCreate
    ) -> models.User:
        """注册新用户"""
        # 检查邮箱是否已存在
        if db.query(models.User).filter(models.User.email == user_create.email).first():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        try:
            # 创建新用户
            db_user = models.User(
                email=user_create.email,
                hashed_password=self.get_password_hash(user_create.password),
                is_active=True
            )
            db.add(db_user)
            db.commit()
            db.refresh(db_user)
            return db_user
            
        except Exception as e:
            logger.error(f"Failed to register user: {str(e)}")
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to register user"
            ) 