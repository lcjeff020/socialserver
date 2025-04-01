"""
分析相关的数据模型
"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel

class ContentAnalytics(BaseModel):
    """内容分析数据"""
    content_id: int
    views: int = 0
    likes: int = 0
    comments: int = 0
    shares: int = 0
    engagement_rate: float = 0.0
    updated_at: datetime

class AccountAnalytics(BaseModel):
    """账号分析数据"""
    account_id: int
    followers: int = 0
    following: int = 0
    posts: int = 0
    engagement_rate: float = 0.0
    period_start: datetime
    period_end: datetime

class TrendsAnalysis(BaseModel):
    """趋势分析数据"""
    platform: Optional[str] = None
    period: str
    data_points: List[Dict]
    trends: Dict

class PerformanceReport(BaseModel):
    """性能报告"""
    total_posts: int = 0
    total_engagement: int = 0
    best_performing_posts: List[Dict]
    worst_performing_posts: List[Dict]
    performance_by_time: Dict
    recommendations: List[str]

class AnalyticsSummary(BaseModel):
    """分析摘要"""
    total_accounts: int = 0
    total_posts: int = 0
    total_engagement: int = 0
    average_engagement_rate: float = 0.0
    platform_distribution: Dict
    content_performance: Dict 