"""
基础数据模型 (MySQL)
"""

from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.db.session import MySQLBase

class User(MySQLBase):
    __tablename__ = "users"
    # ... 用户模型定义 ...

class Content(MySQLBase):
    __tablename__ = "contents"
    # ... 内容模型定义 ...

class Account(MySQLBase):
    __tablename__ = "accounts"
    # ... 账号模型定义 ... 