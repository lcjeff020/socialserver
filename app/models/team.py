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

from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base_class import Base

class Team(Base):
    """团队模型"""
    __tablename__ = "teams"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(String(1000))
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    is_active = Column(Boolean, default=True)
    config = Column(JSON)

    # 审计字段
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # 关系
    owner = relationship("User", back_populates="teams")
    members = relationship("TeamMember", back_populates="team")

    def __repr__(self):
        return f"<Team {self.name}>"


class TeamMember(Base):
    """团队成员模型"""
    __tablename__ = "team_members"

    id = Column(Integer, primary_key=True, index=True)
    team_id = Column(Integer, ForeignKey("teams.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    role = Column(String(50), default="member")
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # 关系
    team = relationship("Team", back_populates="members")
    user = relationship("User") 