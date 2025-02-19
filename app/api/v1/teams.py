"""
团队管理API模块

提供团队管理相关功能：
1. 团队创建和管理
2. 成员管理
3. 权限控制
4. 团队资源管理
"""

from typing import Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import models, schemas
from app.api import deps
from app.services.team_service import TeamService
from app.utils.logger import logger

router = APIRouter()
team_service = TeamService()

@router.post("/", response_model=schemas.Team)
async def create_team(
    *,
    db: Session = Depends(deps.get_mysql_db),
    team_in: schemas.TeamCreate,
    current_user: models.User = Depends(deps.get_current_user)
) -> Any:
    """创建新团队"""
    try:
        team = await team_service.create_team(
            db=db,
            team_in=team_in,
            owner_id=current_user.id
        )
        return team
    except Exception as e:
        logger.error(f"Create team error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.get("/", response_model=List[schemas.Team])
async def get_teams(
    db: Session = Depends(deps.get_mysql_db),
    current_user: models.User = Depends(deps.get_current_user)
) -> Any:
    """获取用户相关的团队列表"""
    try:
        teams = await team_service.get_user_teams(db=db, user_id=current_user.id)
        return teams
    except Exception as e:
        logger.error(f"Get teams error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.post("/{team_id}/members", response_model=schemas.TeamMember)
async def add_team_member(
    *,
    db: Session = Depends(deps.get_mysql_db),
    team_id: int,
    member_in: schemas.TeamMemberCreate,
    current_user: models.User = Depends(deps.get_current_user)
) -> Any:
    """添加团队成员"""
    if not await team_service.is_team_admin(db, team_id, current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    try:
        member = await team_service.add_member(
            db=db,
            team_id=team_id,
            member_in=member_in
        )
        return member
    except Exception as e:
        logger.error(f"Add team member error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.delete("/{team_id}/members/{user_id}")
async def remove_team_member(
    *,
    db: Session = Depends(deps.get_mysql_db),
    team_id: int,
    user_id: int,
    current_user: models.User = Depends(deps.get_current_user)
) -> Any:
    """移除团队成员"""
    if not await team_service.is_team_admin(db, team_id, current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    try:
        await team_service.remove_member(db=db, team_id=team_id, user_id=user_id)
        return {"msg": "Member removed successfully"}
    except Exception as e:
        logger.error(f"Remove team member error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        ) 