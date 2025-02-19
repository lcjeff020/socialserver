"""
分析数据模型 (PostgreSQL)
"""

from sqlalchemy import Column, Integer, String, DateTime, JSON, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from app.db.session import PostgresBase

class ContentAnalytics(PostgresBase):
    __tablename__ = "content_analytics"
    
    id = Column(Integer, primary_key=True, index=True)
    content_id = Column(Integer)  # 关联到MySQL的content表
    platform = Column(String)
    metrics = Column(JSONB)  # 使用PostgreSQL的JSONB类型存储指标
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

class AccountAnalytics(PostgresBase):
    __tablename__ = "account_analytics"
    
    id = Column(Integer, primary_key=True, index=True)
    account_id = Column(Integer)  # 关联到MySQL的account表
    platform = Column(String)
    metrics = Column(JSONB)
    period = Column(String)  # daily, weekly, monthly
    date = Column(DateTime)

class EngagementMetrics(PostgresBase):
    __tablename__ = "engagement_metrics"
    
    id = Column(Integer, primary_key=True, index=True)
    content_id = Column(Integer)
    platform = Column(String)
    engagement_type = Column(String)  # like, comment, share
    count = Column(Integer)
    date = Column(DateTime) 