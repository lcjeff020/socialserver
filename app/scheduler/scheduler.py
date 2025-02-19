"""
任务调度管理模块

负责管理系统中的所有定时任务，功能包括：
1. 定时内容发布
2. 数据定时采集
3. 报告定时生成
4. 任务状态管理

基于APScheduler实现，支持：
- 持久化任务存储
- 失败任务重试
- 动态任务管理
"""

from datetime import datetime
from typing import Dict, Any
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from app.core.config import settings

class TaskScheduler:
    """任务调度器
    
    负责管理所有定时任务：
    - 创建定时发布任务
    - 管理任务执行
    - 处理任务状态更新
    
    使用 APScheduler 实现，支持持久化到数据库
    """
    
    def __init__(self):
        """初始化调度器
        - 配置任务存储
        - 设置执行器
        - 初始化调度器
        """
        jobstores = {
            'default': SQLAlchemyJobStore(url=settings.SQLALCHEMY_DATABASE_URI)
        }
        self.scheduler = AsyncIOScheduler(jobstores=jobstores)
        
    def start(self):
        self.scheduler.start()
        
    def schedule_post(self, post_data: Dict[str, Any], schedule_time: datetime):
        """安排社交媒体发布任务"""
        job = self.scheduler.add_job(
            'app.worker.publish_post',
            'date',
            run_date=schedule_time,
            kwargs={'post_data': post_data},
            id=f"post_{post_data['id']}"
        )
        return job.id
    
    def cancel_scheduled_post(self, job_id: str):
        """取消已安排的发布任务"""
        self.scheduler.remove_job(job_id) 