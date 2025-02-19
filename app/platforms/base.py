"""
社交平台抽象基类模块

定义了所有社交平台的标准接口，包括：
1. 内容发布接口
2. 数据分析接口
3. 定时发布接口

所有具体的社交平台实现（如TikTok、Instagram等）都必须继承此基类
并实现这些标准接口，确保不同平台的一致性操作
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List

class BasePlatform(ABC):
    """社交平台基类
    
    定义了所有社交平台必须实现的基本接口：
    - 内容发布
    - 数据分析
    - 定时发布
    
    所有具体的平台实现都必须继承此类并实现这些方法
    """
    
    @abstractmethod
    async def post_content(self, content: Dict[str, Any]) -> Dict[str, Any]:
        """发布内容到平台"""
        pass
    
    @abstractmethod
    async def get_analytics(self, post_id: str) -> Dict[str, Any]:
        """获取帖子分析数据"""
        pass
    
    @abstractmethod
    async def schedule_post(self, content: Dict[str, Any], schedule_time: str) -> Dict[str, Any]:
        """安排定时发布"""
        pass 