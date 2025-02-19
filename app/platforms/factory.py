"""
平台工厂模块

负责创建和管理不同社交平台的实例：
1. 平台实例创建
2. 平台配置管理
3. 平台状态维护
"""

from typing import Dict, Type
from .base import BasePlatform
from .facebook import FacebookPlatform
from .instagram import InstagramPlatform
from .youtube import YoutubePlatform

class PlatformFactory:
    _platforms: Dict[str, Type[BasePlatform]] = {
        "facebook": FacebookPlatform,
        "instagram": InstagramPlatform,
        "youtube": YoutubePlatform
    }

    @classmethod
    def get_platform(cls, platform_name: str) -> BasePlatform:
        """获取平台实例"""
        if platform_name not in cls._platforms:
            raise ValueError(f"Unsupported platform: {platform_name}")
        return cls._platforms[platform_name]() 