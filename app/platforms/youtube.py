"""
YouTube平台实现模块

实现YouTube平台的具体功能：
1. 视频上传
2. 视频管理
3. 数据分析
4. 评论管理
"""

from typing import Dict, Any, List
import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from .base import BasePlatform
from app.core.config import settings
from app.utils.logger import logger

class YoutubePlatform(BasePlatform):
    def __init__(self):
        self.credentials = self._get_credentials()
        self.youtube = build('youtube', 'v3', credentials=self.credentials)

    async def post_content(self, content: Dict[str, Any]) -> Dict[str, Any]:
        """上传视频到YouTube"""
        try:
            if not content.get("media_urls"):
                raise ValueError("Video file is required for YouTube")

            video_path = content["media_urls"][0]
            
            # 设置视频元数据
            body = {
                'snippet': {
                    'title': content['title'],
                    'description': content['content'],
                    'tags': content.get('tags', []),
                    'categoryId': '22'  # 默认分类
                },
                'status': {
                    'privacyStatus': 'public',
                    'selfDeclaredMadeForKids': False
                }
            }

            # 创建媒体文件对象
            media = MediaFileUpload(
                video_path,
                mimetype='video/*',
                resumable=True
            )

            # 执行上传
            request = self.youtube.videos().insert(
                part=','.join(body.keys()),
                body=body,
                media_body=media
            )
            
            response = request.execute()

            return {
                "platform": "youtube",
                "status": "success",
                "post_id": response['id'],
                "url": f"https://youtube.com/watch?v={response['id']}"
            }

        except Exception as e:
            logger.error(f"YouTube upload error: {str(e)}")
            raise

    async def get_analytics(self, post_id: str) -> Dict[str, Any]:
        """获取视频分析数据"""
        try:
            request = self.youtube.videos().list(
                part="statistics",
                id=post_id
            )
            response = request.execute()

            if not response['items']:
                raise ValueError("Video not found")

            stats = response['items'][0]['statistics']
            return {
                "views": stats.get('viewCount', 0),
                "likes": stats.get('likeCount', 0),
                "comments": stats.get('commentCount', 0)
            }

        except Exception as e:
            logger.error(f"YouTube analytics error: {str(e)}")
            raise

    def _get_credentials(self) -> Credentials:
        """获取YouTube API凭证"""
        SCOPES = ['https://www.googleapis.com/auth/youtube.upload',
                 'https://www.googleapis.com/auth/youtube.readonly']
        
        flow = InstalledAppFlow.from_client_secrets_file(
            settings.YOUTUBE_CLIENT_SECRETS_FILE,
            SCOPES
        )
        return flow.run_local_server(port=0) 