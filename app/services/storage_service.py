"""
文件存储服务模块

管理系统中所有文件的存储，功能包括：
1. 媒体文件上传
2. 文件删除
3. 文件访问URL生成
4. 文件元数据管理

使用AWS S3作为存储后端，支持：
- 大文件处理
- 文件访问控制
- 文件生命周期管理
"""

import boto3
from typing import BinaryIO
from app.core.config import settings

class StorageService:
    def __init__(self):
        self.s3 = boto3.client(
            's3',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
        )
        self.bucket = settings.S3_BUCKET
        
    async def upload_file(self, file: BinaryIO, filename: str) -> str:
        """上传文件到S3"""
        try:
            self.s3.upload_fileobj(file, self.bucket, filename)
            return f"https://{self.bucket}.s3.amazonaws.com/{filename}"
        except Exception as e:
            raise Exception(f"Failed to upload file: {str(e)}")
    
    async def delete_file(self, filename: str):
        """从S3删除文件"""
        try:
            self.s3.delete_object(Bucket=self.bucket, Key=filename)
        except Exception as e:
            raise Exception(f"Failed to delete file: {str(e)}") 