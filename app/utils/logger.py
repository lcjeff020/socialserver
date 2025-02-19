"""
日志工具模块

配置和管理应用日志：
1. 日志格式定义
2. 日志级别控制
3. 日志输出配置
"""

import logging
from app.core.config import settings

def setup_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(settings.LOG_LEVEL)
    return logger

logger = setup_logger("social-media-manager") 