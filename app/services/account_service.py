"""
账号服务模块
"""

from typing import List, Optional
from sqlalchemy.orm import Session
from app import models, schemas

class AccountService:
    async def get_account(self, db: Session, account_id: int) -> Optional[models.Account]:
        return db.query(models.Account).filter(models.Account.id == account_id).first()
    
    async def get_account_by_platform(
        self, 
        db: Session, 
        user_id: int,
        platform: str,
        platform_id: str
    ) -> Optional[models.Account]:
        return db.query(models.Account).filter(
            models.Account.user_id == user_id,
            models.Account.platform == platform,
            models.Account.platform_id == platform_id
        ).first()
    
    async def get_user_accounts(
        self, 
        db: Session, 
        user_id: int,
        skip: int = 0,
        limit: int = 100,
        platform: Optional[str] = None
    ) -> List[models.Account]:
        query = db.query(models.Account).filter(models.Account.user_id == user_id)
        if platform:
            query = query.filter(models.Account.platform == platform)
        return query.offset(skip).limit(limit).all() 