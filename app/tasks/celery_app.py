"""
Celery应用配置模块

负责配置和初始化Celery应用，包括：
1. 任务队列配置
2. 任务路由设置
3. 错误处理
4. 任务重试策略
"""

from celery import Celery
from app.core.config import settings

celery = Celery(
    "social-media-manager",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL
)

# 任务路由配置
celery.conf.task_routes = {
    'app.tasks.content.*': {'queue': 'content'},
    'app.tasks.analytics.*': {'queue': 'analytics'}
}

# 任务重试设置
celery.conf.task_acks_late = True
celery.conf.task_reject_on_worker_lost = True 