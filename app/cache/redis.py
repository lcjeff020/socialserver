"""
Redis缓存配置模块

管理Redis连接和缓存操作：
1. 连接池管理
2. 键值操作封装
3. 缓存策略配置
"""

from redis import Redis
from app.core.config import settings

redis_client = Redis.from_url(settings.REDIS_URL)

class RedisCache:
    @staticmethod
    async def get(key: str) -> str:
        return redis_client.get(key)
        
    @staticmethod
    async def set(key: str, value: str, expire: int = None):
        redis_client.set(key, value, ex=expire) 