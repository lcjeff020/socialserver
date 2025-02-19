"""
团队管理数据模型

定义团队相关的数据结构，包括：
1. 团队基本信息
2. 团队成员关系
3. 成员权限管理
4. 团队资源关联

使用SQLAlchemy ORM，支持：
- 多对多关系（用户-团队）
- 权限角色管理
- 团队资源隔离
"""

from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from app.db.base_class import Base

team_members = Table(
    "team_members",
    Base.metadata,
    Column("team_id", Integer, ForeignKey("teams.id")),
    Column("user_id", Integer, ForeignKey("users.id")),
    Column("role", String)  # admin, editor, viewer
)

class Team(Base):
    __tablename__ = "teams"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, nullable=True)
    
    members = relationship("User", secondary=team_members, backref="teams")
    accounts = relationship("Account", back_populates="team") 