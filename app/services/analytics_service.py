"""
数据分析服务模块

提供全面的数据分析功能，包括：
1. 账号数据分析（粉丝增长、互动率等）
2. 内容表现分析（播放量、点赞量等）
3. 最佳发布时间分析
4. 竞品数据分析
5. 趋势报告生成

支持多平台数据整合，提供统一的分析接口
"""

from typing import Dict, Any, List
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app import models
from app.core.config import settings

class AnalyticsService:
    """数据分析服务
    
    提供各类数据分析功能：
    - 账号数据分析
    - 内容表现分析
    - 互动率计算
    - 最佳发布时间分析
    """
    
    async def get_account_analytics(
        self,
        db: Session,
        account_id: int,
        start_date: datetime,
        end_date: datetime
    ) -> Dict[str, Any]:
        """获取账号分析数据
        
        参数:
            db: 数据库会话
            account_id: 账号ID
            start_date: 开始日期
            end_date: 结束日期
            
        返回:
            包含各类统计数据的字典
        """
        account = db.query(models.Account).filter_by(id=account_id).first()
        if not account:
            raise ValueError("Account not found")
            
        # 获取发布统计
        posts = db.query(models.Content).filter(
            models.Content.account_id == account_id,
            models.Content.created_at.between(start_date, end_date)
        ).all()
        
        # 统计数据
        stats = {
            "total_posts": len(posts),
            "engagement_rate": self._calculate_engagement_rate(posts),
            "followers_growth": self._get_followers_growth(account, start_date, end_date),
            "best_posting_times": self._analyze_best_posting_times(posts)
        }
        
        return stats
    
    def _calculate_engagement_rate(self, posts: List[models.Content]) -> float:
        """计算互动率"""
        if not posts:
            return 0.0
            
        total_engagement = sum(
            post.analytics.get("likes", 0) + 
            post.analytics.get("comments", 0) + 
            post.analytics.get("shares", 0) 
            for post in posts
        )
        return total_engagement / len(posts)

    async def get_content_analytics(
        self,
        mysql_db: Session,  # 用于基础数据
        postgres_db: Session,  # 用于分析数据
        content_id: int
    ) -> Dict[str, Any]:
        """获取内容分析数据"""
        # 从MySQL获取基础内容信息
        content = mysql_db.query(models.Content).filter_by(id=content_id).first()
        if not content:
            raise ValueError("Content not found")
            
        # 从PostgreSQL获取分析数据
        analytics = postgres_db.query(models.ContentAnalytics)\
            .filter_by(content_id=content_id)\
            .order_by(models.ContentAnalytics.created_at.desc())\
            .first()
            
        return {
            "content": {
                "id": content.id,
                "title": content.title,
                "platform": content.platform
            },
            "analytics": analytics.metrics if analytics else {}
        }

    async def store_analytics(
        self,
        postgres_db: Session,
        content_id: int,
        platform: str,
        metrics: Dict[str, Any]
    ):
        """存储分析数据"""
        analytics = models.ContentAnalytics(
            content_id=content_id,
            platform=platform,
            metrics=metrics,
            created_at=datetime.utcnow()
        )
        postgres_db.add(analytics)
        postgres_db.commit() 