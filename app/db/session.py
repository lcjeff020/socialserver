"""
数据库会话模块

管理MySQL和PostgreSQL的数据库连接和会话
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
from app.core.config import settings
from typing import Generator

# 创建数据库引擎
engine = create_engine(
    settings.MYSQL_DATABASE_URI,
    pool_pre_ping=True,
    echo=settings.LOG_LEVEL == "DEBUG"
)

# 创建会话工厂
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# MySQL引擎和会话
mysql_engine = create_engine(
    settings.MYSQL_DATABASE_URI,
    pool_pre_ping=True,
    pool_size=20,
    max_overflow=10
)
MySQLSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=mysql_engine
)

# PostgreSQL引擎和会话
postgres_engine = create_engine(
    settings.POSTGRES_DATABASE_URI,
    pool_pre_ping=True,
    pool_size=20,
    max_overflow=10
)
PostgresSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=postgres_engine
)

# 基础模型类
MySQLBase = declarative_base()
PostgresBase = declarative_base()

# 数据库依赖函数
def get_mysql_db() -> Generator[Session, None, None]:
    """获取MySQL数据库会话"""
    db = MySQLSessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_postgres_db() -> Generator[Session, None, None]:
    """获取PostgreSQL数据库会话"""
    db = PostgresSessionLocal()
    try:
        yield db
    finally:
        db.close() 