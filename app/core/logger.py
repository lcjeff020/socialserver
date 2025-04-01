"""
日志配置模块
"""

import os
import logging
from logging.handlers import TimedRotatingFileHandler
from datetime import datetime

# 创建logs目录
LOG_DIR = "logs"
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

# 生成日志文件名
def get_log_filename():
    return os.path.join(LOG_DIR, f"app_{datetime.now().strftime('%Y-%m-%d')}.log")

# 配置日志
def setup_logger():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # 控制台处理器
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(console_format)
    
    # 文件处理器 (每天轮换)
    file_handler = TimedRotatingFileHandler(
        filename=get_log_filename(),
        when='midnight',
        interval=1,
        backupCount=30,
        encoding='utf-8'
    )
    file_handler.setLevel(logging.INFO)
    file_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(file_format)

    # 添加处理器
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger 