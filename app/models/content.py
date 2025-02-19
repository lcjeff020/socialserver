"""
内容模型模块
"""

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base_class import Base

class Content(Base):
    """内容模型"""
    __tablename__ = "contents"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    account_id = Column(Integer, ForeignKey("accounts.id"), nullable=False)
    title = Column(String(255), nullable=False)
    content = Column(String(4000))
    content_type = Column(String(50))  # text, image, video
    platform = Column(String(50))
    status = Column(String(50), default="draft")
    scheduled_time = Column(DateTime(timezone=True))
    published_at = Column(DateTime(timezone=True))
    meta_data = Column(JSON)

    # 审计字段
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # 关系
    user = relationship("User", back_populates="contents")
    account = relationship("Account", back_populates="contents")

    def __repr__(self):
        return f"<Content {self.title}>" 