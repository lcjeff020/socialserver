from typing import Dict, Any
from celery import Celery
from app.core.config import settings
from app.db.session import SessionLocal
from app import models

celery = Celery(
    "worker",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL
)

@celery.task
def execute_social_task(task_id: int):
    """执行社交媒体任务"""
    db = SessionLocal()
    try:
        task = db.query(models.Task).filter(models.Task.id == task_id).first()
        if not task:
            return {"status": "failed", "error": "Task not found"}
        
        # 更新任务状态
        task.status = "running"
        db.commit()
        
        # 执行具体任务逻辑
        result = execute_platform_task(task)
        
        # 更新任务状态
        task.status = "completed"
        db.commit()
        
        return {"status": "success", "result": result}
    
    except Exception as e:
        task.status = "failed"
        db.commit()
        return {"status": "failed", "error": str(e)}
    
    finally:
        db.close()

def execute_platform_task(task: models.Task) -> Dict[str, Any]:
    """根据平台和任务类型执行具体任务"""
    platform_handlers = {
        "tiktok": execute_tiktok_task,
        "instagram": execute_instagram_task
    }
    
    handler = platform_handlers.get(task.platform)
    if not handler:
        raise ValueError(f"Unsupported platform: {task.platform}")
    
    return handler(task) 