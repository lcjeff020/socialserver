from sqlalchemy import Column, Integer, String, DateTime, JSON, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base_class import Base

class Content(Base):
    __tablename__ = "contents"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(String)
    media_urls = Column(JSON)  # 存储媒体文件URL列表
    schedule_time = Column(DateTime)
    status = Column(String)  # draft, scheduled, published, failed
    platforms = Column(JSON)  # 要发布到的平台列表
    analytics = Column(JSON, default={})  # 存储分析数据
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="contents") 