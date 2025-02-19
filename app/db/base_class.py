"""
数据库基础类模块
"""

from sqlalchemy.ext.declarative import declarative_base, declared_attr

class CustomBase:
    # 生成表名
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()
    
    # 通用的列
    id: int

# 创建基础模型类
Base = declarative_base(cls=CustomBase) 