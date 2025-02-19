"""
社交账号模型模块
"""

from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base_class import Base

class Account(Base):
    """社交媒体账号模型"""
    __tablename__ = "accounts"

    # 定义社交媒体账号的基本属性
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    platform = Column(String(50), nullable=False)  # 平台类型：instagram, tiktok 等
    platform_id = Column(String(255))  # 平台账号ID
    username = Column(String(255))
    access_token = Column(String(1024))
    refresh_token = Column(String(1024))
    token_expires_at = Column(DateTime)
    is_active = Column(Boolean, default=True)
    
    # 审计字段，用于记录账号信息的创建和更新时间
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # 定义关系，关联用户和任务模型
    user = relationship("User", back_populates="accounts")
    tasks = relationship("Task", back_populates="account")

    def __repr__(self):
        """返回社交媒体账号的字符串表示形式"""
        return f"<Account {self.platform}:{self.username}>"