"""
TikTok平台集成模块

实现了与TikTok平台的具体交互，包括：
1. 内容发布功能
2. 数据统计获取
3. 评论互动管理
4. 账号数据分析

使用TikTok官方API，处理认证、请求和响应
支持异步操作，使用httpx进行HTTP请求
"""

import json
from typing import Dict, Any, List
import httpx
from .base import BasePlatform
from app.core.config import settings
from app.utils.logger import logger

class TiktokPlatform(BasePlatform):
    """TikTok平台实现类
    
    实现了与TikTok平台的具体交互：
    - 通过API发布内容
    - 获取数据分析
    - 处理授权认证
    """
    
    def __init__(self):
        """初始化TikTok平台
        - 设置API密钥
        - 配置基础URL
        - 初始化HTTP客户端
        """
        self.api_key = settings.TIKTOK_APP_KEY
        self.api_secret = settings.TIKTOK_APP_SECRET
        self.base_url = "https://open.tiktokapis.com/v2"
        self.upload_url = f"{self.base_url}/video/upload/"
        self.publish_url = f"{self.base_url}/video/publish/"
        
    async def post_content(self, content: Dict[str, Any]) -> Dict[str, Any]:
        """发布内容到TikTok"""
        try:
            # 1. 上传视频
            video_id = await self._upload_video(content["media_urls"][0])
            
            # 2. 发布视频
            result = await self._publish_video(video_id, content)
            
            return {
                "platform": "tiktok",
                "status": "success",
                "post_id": result["video_id"],
                "url": result["share_url"]
            }
        except Exception as e:
            logger.error(f"TikTok post error: {str(e)}")
            raise
            
    async def _upload_video(self, video_url: str) -> str:
        """上传视频到TikTok"""
        async with httpx.AsyncClient() as client:
            # 1. 获取上传URL
            init_response = await client.post(
                self.upload_url,
                headers=self._get_headers(),
                json={"source": "FILE"}
            )
            upload_info = init_response.json()

            # 2. 上传视频文件
            with open(video_url, "rb") as video_file:
                upload_response = await client.put(
                    upload_info["upload_url"],
                    content=video_file,
                    headers={"Content-Type": "video/mp4"}
                )

            return upload_info["video_id"]

    async def _publish_video(self, video_id: str, content: Dict[str, Any]) -> Dict[str, Any]:
        """发布视频"""
        publish_data = {
            "video_id": video_id,
            "title": content["title"],
            "description": content["content"],
            "privacy_level": "PUBLIC",
            "disable_comment": False,
            "disable_duet": False,
            "disable_stitch": False,
            "tags": content.get("tags", [])
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(
                self.publish_url,
                headers=self._get_headers(),
                json=publish_data
            )
            return response.json()

    async def get_analytics(self, post_id: str) -> Dict[str, Any]:
        """获取帖子分析数据"""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/videos/{post_id}/analytics",
                headers=self._get_headers()
            )
            return response.json()
    
    def _get_headers(self) -> Dict[str, str]:
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        } 