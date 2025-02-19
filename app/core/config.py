"""
配置管理模块

本模块负责管理整个应用的配置信息，包括：
1. 项目基础配置（名称、版本等）
2. 安全相关配置（密钥、Token等）
3. 数据库连接配置
4. 第三方服务配置（AWS、Redis等）
5. 社交平台API配置

使用 Pydantic 进行配置验证，确保所有配置项的类型正确性
"""

from typing import List, Union
from pydantic_settings import BaseSettings
from pydantic import AnyHttpUrl, validator
import logging

class Settings(BaseSettings):
    """全局配置类
    
    包含了应用程序所需的所有配置项：
    - 基础设置（项目名称、API版本等）
    - 安全设置（密钥、token过期时间等）
    - 数据库设置
    - 存储设置（S3配置）
    - 社交平台设置（各平台的密钥）
    """
    # 基础设置
    PROJECT_NAME: str = "Social Media Manager"
    API_V1_STR: str = "/api/v1"
    
    # 安全设置
    SECRET_KEY: str = "your-secret-key-here"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8天
    
    # BACKEND_CORS_ORIGINS is a comma-separated list of origins
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        return v

    # MySQL配置 (用于基础数据)
    MYSQL_HOST: str = "localhost"
    MYSQL_PORT: int = 3306
    MYSQL_USER: str = "root"
    MYSQL_PASSWORD: str = "123456"
    MYSQL_DB: str = "socialdb"
    
    # PostgreSQL配置 (用于分析数据)
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = ""
    POSTGRES_DB: str = "social_media_analytics"

    @property
    def MYSQL_DATABASE_URI(self) -> str:
        """MySQL连接URI"""
        return f"mysql+pymysql://{self.MYSQL_USER}:{self.MYSQL_PASSWORD}@{self.MYSQL_HOST}:{self.MYSQL_PORT}/{self.MYSQL_DB}"

    @property
    def POSTGRES_DATABASE_URI(self) -> str:
        """PostgreSQL连接URI"""
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    # S3 配置
    AWS_ACCESS_KEY_ID: str = ""
    AWS_SECRET_ACCESS_KEY: str = ""
    S3_BUCKET: str = ""
    
    # Redis 配置
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # 社交媒体平台配置
    TIKTOK_APP_KEY: str = ""
    TIKTOK_APP_SECRET: str = ""
    INSTAGRAM_APP_ID: str = ""
    INSTAGRAM_APP_SECRET: str = ""
    
    # 时区设置
    TIMEZONE: str = "Asia/Shanghai"
    
    # Facebook配置
    FACEBOOK_APP_ID: str = ""
    FACEBOOK_APP_SECRET: str = ""
    FACEBOOK_PAGE_ID: str = ""
    
    # YouTube配置
    YOUTUBE_CLIENT_SECRETS_FILE: str = "client_secrets.json"
    
    # 添加日志配置
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    LOG_FILE: str = "app.log"
    
    @validator("LOG_LEVEL", pre=True)
    def validate_log_level(cls, v: str) -> str:
        """验证日志级别"""
        valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        v = v.upper()
        if v not in valid_levels:
            return "INFO"
        return v

    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings() 