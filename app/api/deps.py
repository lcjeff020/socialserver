"""
API依赖模块
"""

from fastapi import Depends
from sqlalchemy.orm import Session
from app.db.session import get_mysql_db, get_postgres_db

async def get_analytics_dbs(
    mysql_db: Session = Depends(get_mysql_db),
    postgres_db: Session = Depends(get_postgres_db)
):
    """获取两个数据库的会话"""
    return mysql_db, postgres_db 