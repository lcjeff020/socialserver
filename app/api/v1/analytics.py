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
from app.schemas.common import ResponseModel

router = APIRouter()
analytics_service = AnalyticsService()

@router.get("/content/{content_id}", response_model=ResponseModel[schemas.ContentAnalytics])
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
        return ResponseModel(
            code=200,
            msg="获取成功",
            data=analytics
        )
    except Exception as e:
        logger.error(f"获取内容分析数据错误: {str(e)}")
        return ResponseModel(
            code=201,
            msg="获取内容分析数据失败",
            data={"error": f"{str(e)}"}
        )

@router.get("/account/{account_id}", response_model=ResponseModel[schemas.AccountAnalytics])
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
        return ResponseModel(
            code=200,
            msg="获取成功",
            data=analytics
        )
    except Exception as e:
        logger.error(f"获取账号分析数据错误: {str(e)}")
        return ResponseModel(
            code=201,
            msg="获取账号分析数据失败",
            data={"error": f"{str(e)}"}
        )

@router.get("/trends", response_model=ResponseModel[schemas.TrendsAnalysis])
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
        return ResponseModel(
            code=200,
            msg="获取成功",
            data=trends
        )
    except Exception as e:
        logger.error(f"获取趋势分析数据错误: {str(e)}")
        return ResponseModel(
            code=201,
            msg="获取趋势分析数据失败",
            data={"error": f"{str(e)}"}
        )

@router.get("/performance-report", response_model=ResponseModel[schemas.PerformanceReport])
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
        return ResponseModel(
            code=200,
            msg="获取成功",
            data=report
        )
    except Exception as e:
        logger.error(f"获取性能报告错误: {str(e)}")
        return ResponseModel(
            code=201,
            msg="获取性能报告失败",
            data={"error": f"{str(e)}"}
        )

@router.get("/summary", response_model=ResponseModel[schemas.AnalyticsSummary])
async def get_summary(
    db: Session = Depends(deps.get_mysql_db),
    current_user = Depends(deps.get_current_user)
) -> Any:
    """获取分析摘要"""
    try:
        summary = await analytics_service.get_summary(db, user_id=current_user.id)
        return ResponseModel(
            code=200,
            msg="获取成功",
            data=summary
        )
    except Exception as e:
        logger.error(f"获取分析摘要错误: {str(e)}")
        return ResponseModel(
            code=201,
            msg="获取分析摘要失败",
            data={"error": f"{str(e)}"}
        ) 