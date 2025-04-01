"""
用户服务模块
"""

from typing import Optional
from sqlalchemy.orm import Session
from app import models, schemas
from app.core.security import get_password_hash, verify_password

class UserService:
    """用户服务类"""

    async def get_by_email(self, db: Session, *, email: str) -> Optional[models.User]:
        """通过邮箱获取用户"""
        return db.query(models.User).filter(models.User.email == email).first()

    async def create(self, db: Session, *, obj_in: schemas.UserCreate) -> models.User:
        """创建新用户"""
        db_obj = models.User(
            email=obj_in.email,
            hashed_password=get_password_hash(obj_in.password),
            full_name=obj_in.full_name,
            is_active=True,
            is_superuser=False,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    async def authenticate(
        self, db: Session, *, email: str, password: str
    ) -> Optional[models.User]:
        """用户认证"""
        user = await self.get_by_email(db, email=email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    async def is_active(self, user: models.User) -> bool:
        """检查用户是否激活"""
        return user.is_active

    async def is_superuser(self, user: models.User) -> bool:
        """检查是否是超级用户"""
        return user.is_superuser 