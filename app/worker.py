from typing import Dict, Any
from celery import Celery
from app.core.config import settings
from app.db.session import SessionLocal
from app import models

# 初始化Celery应用，使用Redis作为broker和backend
celery = Celery(
    "worker",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL
)

@celery.task
def execute_social_task(task_id: int) -> Dict[str, Any]:
    """执行社交媒体任务
    
    Args:
        task_id (int): 任务ID
    
    Returns:
        Dict[str, Any]: 任务执行结果，包括状态和可能的错误信息
    """
    db = SessionLocal()
    try:
        # 根据任务ID查询数据库中的任务对象
        task = db.query(models.Task).filter(models.Task.id == task_id).first()
        if not task:
            return {"status": "failed", "error": "Task not found"}
        
        # 更新任务状态为运行中
        task.status = "running"
        db.commit()
        
        # 执行具体任务逻辑
        result = execute_platform_task(task)
        
        # 更新任务状态为已完成
        task.status = "completed"
        db.commit()
        
        return {"status": "success", "result": result}
    
    except Exception as e:
        # 如果执行过程中发生异常，更新任务状态为失败
        task.status = "failed"
        db.commit()
        return {"status": "failed", "error": str(e)}
    
    finally:
        # 关闭数据库会话
        db.close()

def execute_platform_task(task: models.Task) -> Dict[str, Any]:
    """根据平台和任务类型执行具体任务
    
    Args:
        task (models.Task): 任务对象
    
    Returns:
        Dict[str, Any]: 任务执行结果
    
    Raises:
        ValueError: 如果平台不支持，则抛出异常
    """
    # 定义平台和任务处理函数的映射关系
    platform_handlers = {
        "tiktok": execute_tiktok_task,
        "instagram": execute_instagram_task
    }
    
    # 根据任务所属的平台获取对应的处理函数
    handler = platform_handlers.get(task.platform)
    if not handler:
        raise ValueError(f"Unsupported platform: {task.platform}")
    
    # 调用处理函数执行任务并返回结果
    return handler(task)