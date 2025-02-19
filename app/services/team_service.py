"""
团队服务模块
"""

from typing import List, Optional
from sqlalchemy.orm import Session
from app import models, schemas

class TeamService:
    """
    TeamService类提供了团队相关操作的异步服务，
    包括创建团队、获取用户团队列表和检查用户是否为团队管理员。
    """

    async def create_team(self, db: Session, team_in: schemas.TeamCreate, owner_id: int) -> models.Team:
        """
        创建一个新的团队并将其添加到数据库中。
        
        参数:
        - db: 数据库会话。
        - team_in: 包含要创建团队的信息的模式。
        - owner_id: 团队所有者的用户ID。
        
        返回:
        创建的Team对象。
        """
        # 使用传入的团队信息和所有者ID创建一个新的Team实例
        team = models.Team(**team_in.dict(), owner_id=owner_id)
        # 将新的团队添加到数据库会话中
        db.add(team)
        # 提交数据库会话以保存新的团队信息
        db.commit()
        # 刷新数据库会话以确保团队对象的最新状态
        db.refresh(team)
        # 返回新创建的团队对象
        return team
    
    async def get_user_teams(self, db: Session, user_id: int) -> List[models.Team]:
        """
        获取指定用户的团队列表。
        
        参数:
        - db: 数据库会话。
        - user_id: 用户的ID。
        
        返回:
        用户的团队列表。
        """
        # 查询数据库中所有属于指定用户的团队
        return db.query(models.Team).filter(models.Team.owner_id == user_id).all()
    
    async def is_team_admin(self, db: Session, team_id: int, user_id: int) -> bool:
        """
        检查用户是否是指定团队的管理员。
        
        参数:
        - db: 数据库会话。
        - team_id: 团队的ID。
        - user_id: 用户的ID。
        
        返回:
        如果用户是团队的管理员则返回True，否则返回False。
        """
        # 查询指定ID的团队信息
        team = db.query(models.Team).filter(models.Team.id == team_id).first()
        # 检查团队是否存在且所有者ID与用户ID匹配
        return team and team.owner_id == user_id