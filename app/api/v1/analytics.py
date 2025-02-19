"""
数据分析API模块

提供数据分析相关功能：
1. 内容数据分析
2. 账号数据分析
3. 趋势分析
4. 性能报告
"""

from typing import Any, Dict, List, Optional
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import models, schemas
from app.api import deps
from app.services.analytics_service import AnalyticsService
from app.utils.logger import logger

router = APIRouter()
analytics_service = AnalyticsService()

@router.get("/content/{content_id}")
async def get_content_analytics(
    *,
    mysql_db: Session = Depends(deps.get_mysql_db),
    postgres_db: Session = Depends(deps.get_postgres_db),
    content_id: int,
    current_user: models.User = Depends(deps.get_current_user)
) -> Any:
    """获取内容分析数据"""
    try:
        analytics = await analytics_service.get_content_analytics(
            mysql_db=mysql_db,
            postgres_db=postgres_db,
            content_id=content_id
        )
        return analytics
    except Exception as e:
        logger.error(f"Get content analytics error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.get("/account/{account_id}")
async def get_account_analytics(
    *,
    mysql_db: Session = Depends(deps.get_mysql_db),
    postgres_db: Session = Depends(deps.get_postgres_db),
    account_id: int,
    start_date: datetime,
    end_date: datetime,
    current_user: models.User = Depends(deps.get_current_user)
) -> Any:
    """获取账号分析数据"""
    try:
        analytics = await analytics_service.get_account_analytics(
            mysql_db=mysql_db,
            postgres_db=postgres_db,
            account_id=account_id,
            start_date=start_date,
            end_date=end_date
        )
        return analytics
    except Exception as e:
        logger.error(f"Get account analytics error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.get("/trends")
async def get_trends_analysis(
    *,
    postgres_db: Session = Depends(deps.get_postgres_db),
    platform: Optional[str] = None,
    period: str = "7d",
    current_user: models.User = Depends(deps.get_current_user)
) -> Any:
    """获取趋势分析数据"""
    try:
        trends = await analytics_service.get_trends(
            db=postgres_db,
            user_id=current_user.id,
            platform=platform,
            period=period
        )
        return trends
    except Exception as e:
        logger.error(f"Get trends analysis error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.get("/performance-report")
async def get_performance_report(
    *,
    mysql_db: Session = Depends(deps.get_mysql_db),
    postgres_db: Session = Depends(deps.get_postgres_db),
    start_date: datetime,
    end_date: datetime,
    current_user: models.User = Depends(deps.get_current_user)
) -> Any:
    """获取性能报告"""
    try:
        report = await analytics_service.generate_performance_report(
            mysql_db=mysql_db,
            postgres_db=postgres_db,
            user_id=current_user.id,
            start_date=start_date,
            end_date=end_date
        )
        return report
    except Exception as e:
        logger.error(f"Get performance report error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        ) 