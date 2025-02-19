"""
内容处理任务模块

处理与内容相关的异步任务：
1. 内容发布
2. 内容同步
3. 媒体处理
"""

from typing import Dict, Any
from app.tasks.celery_app import celery
from app.db.session import SessionLocal
from app import models

@celery.task(bind=True, max_retries=3)
def publish_content(self, content_id: int) -> Dict[str, Any]:
    """发布内容到社交平台"""
    db = SessionLocal()
    try:
        content = db.query(models.Content).filter_by(id=content_id).first()
        if not content:
            return {"status": "failed", "error": "Content not found"}
            
        # 更新状态
        content.status = "publishing"
        db.commit()
        
        # 执行发布
        result = execute_platform_publish(content)
        
        # 更新结果
        content.status = "published"
        db.commit()
        
        return {"status": "success", "result": result}
        
    except Exception as e:
        self.retry(exc=e, countdown=60)  # 1分钟后重试
        
    finally:
        db.close() 