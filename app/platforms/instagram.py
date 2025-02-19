"""
Instagram平台实现模块

实现Instagram平台的具体功能：
1. 图片/视频上传
2. Story发布
3. 数据分析
"""

from typing import Dict, Any, List
import httpx
from .base import BasePlatform
from app.core.config import settings
from app.utils.logger import logger

class InstagramPlatform(BasePlatform):
    def __init__(self):
        self.api_key = settings.INSTAGRAM_APP_ID
        self.api_secret = settings.INSTAGRAM_APP_SECRET
        self.base_url = "https://graph.instagram.com/v12.0"

    async def post_content(self, content: Dict[str, Any]) -> Dict[str, Any]:
        """发布内容到Instagram"""
        try:
            # 1. 创建媒体容器
            container_id = await self._create_container(content)
            
            # 2. 发布媒体
            result = await self._publish_container(container_id, content)
            
            return {
                "platform": "instagram",
                "status": "success",
                "post_id": result["id"],
                "url": f"https://instagram.com/p/{result['shortcode']}"
            }
        except Exception as e:
            logger.error(f"Instagram post error: {str(e)}")
            raise

    async def _create_container(self, content: Dict[str, Any]) -> str:
        """创建媒体容器"""
        media_type = self._determine_media_type(content["media_urls"])
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/media",
                headers=self._get_headers(),
                json={
                    "media_type": media_type,
                    "image_url": content["media_urls"][0] if media_type == "IMAGE" else None,
                    "video_url": content["media_urls"][0] if media_type == "VIDEO" else None,
                    "caption": f"{content['title']}\n\n{content['content']}"
                }
            )
            return response.json()["id"]

    async def _publish_container(self, container_id: str, content: Dict[str, Any]) -> Dict[str, Any]:
        """发布媒体容器"""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/media/publish",
                headers=self._get_headers(),
                json={
                    "creation_id": container_id
                }
            )
            return response.json()

    def _determine_media_type(self, media_urls: List[str]) -> str:
        """确定媒体类型"""
        # 简单根据文件扩展名判断
        if media_urls[0].endswith((".mp4", ".mov")):
            return "VIDEO"
        return "IMAGE"

    async def get_analytics(self, post_id: str) -> Dict[str, Any]:
        """获取帖子分析数据"""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/{post_id}/insights",
                headers=self._get_headers(),
                params={"metric": "engagement,impressions,reach"}
            )
            return response.json()

    def _get_headers(self) -> Dict[str, str]:
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        } 