"""
内容管理服务模块

处理所有与内容相关的操作，包括：
1. 内容创建和编辑
2. 媒体文件上传
3. 内容定时发布
4. 多平台内容同步
5. 内容版本管理

集成了文件存储服务，支持多种媒体格式
"""

from typing import List, Dict, Any
from fastapi import HTTPException, UploadFile
from sqlalchemy.orm import Session
from app import models, schemas
from app.services.storage_service import StorageService
from app.cache.redis import RedisCache
from app.utils.logger import logger
from app.tasks.content import publish_content
from app.platforms.factory import PlatformFactory

class ContentService:
    def __init__(self):
        self.storage = StorageService()
        self.cache = RedisCache()
    
    async def create_content(
        self,
        db: Session,
        content_data: schemas.ContentCreate,
        media_files: List[UploadFile],
        user: models.User
    ) -> models.Content:
        try:
            # 上传媒体文件
            media_urls = []
            for file in media_files:
                url = await self.storage.upload_file(
                    file.file,
                    f"user_{user.id}/{file.filename}"
                )
                media_urls.append(url)
            
            # 创建内容记录
            content = models.Content(
                title=content_data.title,
                content=content_data.content,
                media_urls=media_urls,
                schedule_time=content_data.schedule_time,
                platforms=content_data.platforms,
                status="draft",
                user_id=user.id
            )
            
            db.add(content)
            db.commit()
            db.refresh(content)
            
            # 如果需要立即发布
            if content_data.publish_now:
                publish_content.delay(content.id)
                
            return content
            
        except Exception as e:
            logger.error(f"Failed to create content: {str(e)}")
            raise 

    async def publish_post(self, db: Session, post_id: int) -> Dict[str, Any]:
        """发布内容到多个平台"""
        post = await self.get_post(db, post_id)
        if not post:
            raise ValueError("Post not found")

        results = []
        for platform_name in post.platforms:
            try:
                # 获取平台实例
                platform = PlatformFactory.get_platform(platform_name)
                
                # 发布内容
                result = await platform.post_content({
                    "title": post.title,
                    "content": post.content,
                    "media_urls": post.media_urls,
                    "tags": post.tags,
                    "config": post.config.get(platform_name, {})
                })
                
                results.append(result)
                
                # 更新发布状态
                post.status = "published"
                post.analytics[platform_name] = result
                db.commit()
                
            except Exception as e:
                logger.error(f"Failed to publish to {platform_name}: {str(e)}")
                post.status = "failed"
                db.commit()
                raise
        
        return {
            "status": "success",
            "results": results
        } 