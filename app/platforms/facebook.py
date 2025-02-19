"""
Facebook平台实现模块

实现Facebook平台的具体功能：
1. 文本/图片/视频发布
2. 页面管理
3. 数据分析
4. 互动管理
"""

from typing import Dict, Any, List
import httpx
from .base import BasePlatform
from app.core.config import settings
from app.utils.logger import logger

class FacebookPlatform(BasePlatform):
    def __init__(self):
        self.api_key = settings.FACEBOOK_APP_ID
        self.api_secret = settings.FACEBOOK_APP_SECRET
        self.base_url = "https://graph.facebook.com/v17.0"
        self.page_id = settings.FACEBOOK_PAGE_ID

    async def post_content(self, content: Dict[str, Any]) -> Dict[str, Any]:
        """发布内容到Facebook"""
        try:
            if content.get("media_urls"):
                # 包含媒体的帖子
                post_id = await self._create_media_post(content)
            else:
                # 纯文本帖子
                post_id = await self._create_text_post(content)

            return {
                "platform": "facebook",
                "status": "success",
                "post_id": post_id,
                "url": f"https://facebook.com/{post_id}"
            }
        except Exception as e:
            logger.error(f"Facebook post error: {str(e)}")
            raise

    async def _create_media_post(self, content: Dict[str, Any]) -> str:
        """创建包含媒体的帖子"""
        media_type = self._determine_media_type(content["media_urls"][0])
        
        async with httpx.AsyncClient() as client:
            # 1. 上传媒体
            media_response = await client.post(
                f"{self.base_url}/{self.page_id}/photos" if media_type == "photo" else f"{self.base_url}/{self.page_id}/videos",
                headers=self._get_headers(),
                data={
                    "url": content["media_urls"][0],
                    "caption": f"{content['title']}\n\n{content['content']}"
                }
            )
            return media_response.json()["id"]

    async def _create_text_post(self, content: Dict[str, Any]) -> str:
        """创建纯文本帖子"""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/{self.page_id}/feed",
                headers=self._get_headers(),
                data={
                    "message": f"{content['title']}\n\n{content['content']}"
                }
            )
            return response.json()["id"]

    def _determine_media_type(self, media_url: str) -> str:
        """确定媒体类型"""
        if media_url.endswith((".mp4", ".mov")):
            return "video"
        return "photo"

    async def get_analytics(self, post_id: str) -> Dict[str, Any]:
        """获取帖子分析数据"""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/{post_id}/insights",
                headers=self._get_headers(),
                params={
                    "metric": "post_impressions,post_engagements,post_reactions_by_type_total"
                }
            )
            return response.json()

    def _get_headers(self) -> Dict[str, str]:
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        } 