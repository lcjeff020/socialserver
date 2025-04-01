"""
团队相关的API路由
"""

from typing import Any, List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app import schemas
from app.api import deps
from app.services.team_service import TeamService
from app.schemas.common import ResponseModel
import logging

logger = logging.getLogger(__name__)
router = APIRouter()
team_service = TeamService()

@router.get("/", response_model=ResponseModel[List[schemas.Team]])
async def list_teams(
    db: Session = Depends(deps.get_mysql_db),
    current_user = Depends(deps.get_current_user)
) -> Any:
    """获取用户的团队列表"""
    try:
        teams = await team_service.get_user_teams(db, user_id=current_user.id)
        return ResponseModel(
            code=200,
            msg="获取成功",
            data=teams
        )
    except Exception as e:
        logger.error(f"获取团队列表错误: {str(e)}")
        return ResponseModel(
            code=201,
            msg="获取团队列表失败",
            data={"error": f"{str(e)}"}
        )

@router.post("/", response_model=ResponseModel[schemas.Team])
async def create_team(
    *,
    db: Session = Depends(deps.get_mysql_db),
    team_in: schemas.TeamCreate,
    current_user = Depends(deps.get_current_user)
) -> Any:
    """创建新团队"""
    try:
        team = await team_service.create_team(db, team_in=team_in, owner_id=current_user.id)
        return ResponseModel(
            code=200,
            msg="创建成功",
            data=team
        )
    except Exception as e:
        logger.error(f"创建团队错误: {str(e)}")
        return ResponseModel(
            code=201,
            msg="创建团队失败",
            data={"error": f"{str(e)}"}
        )

@router.get("/{team_id}", response_model=ResponseModel[schemas.Team])
async def get_team(
    *,
    db: Session = Depends(deps.get_mysql_db),
    team_id: int,
    current_user = Depends(deps.get_current_user)
) -> Any:
    """获取团队详情"""
    try:
        team = await team_service.get_team(db, team_id=team_id)
        if not team or team.owner_id != current_user.id:
            return ResponseModel(
                code=201,
                msg="团队不存在或无权限",
                data={}
            )
        return ResponseModel(
            code=200,
            msg="获取成功",
            data=team
        )
    except Exception as e:
        logger.error(f"获取团队详情错误: {str(e)}")
        return ResponseModel(
            code=201,
            msg="获取团队详情失败",
            data={"error": f"{str(e)}"}
        )

@router.put("/{team_id}", response_model=ResponseModel[schemas.Team])
async def update_team(
    *,
    db: Session = Depends(deps.get_mysql_db),
    team_id: int,
    team_in: schemas.TeamUpdate,
    current_user = Depends(deps.get_current_user)
) -> Any:
    """更新团队信息"""
    try:
        team = await team_service.get_team(db, team_id=team_id)
        if not team or team.owner_id != current_user.id:
            return ResponseModel(
                code=201,
                msg="团队不存在或无权限",
                data="团队不存在或无权限修改"
            )
        team = await team_service.update_team(db, team=team, team_in=team_in)
        return ResponseModel(
            code=200,
            msg="更新成功",
            data=team
        )
    except Exception as e:
        logger.error(f"更新团队错误: {str(e)}")
        return ResponseModel(
            code=201,
            msg="更新团队失败",
            data={"error": f"{str(e)}"}
        )

@router.delete("/{team_id}", response_model=ResponseModel[dict])
async def delete_team(
    *,
    db: Session = Depends(deps.get_mysql_db),
    team_id: int,
    current_user = Depends(deps.get_current_user)
) -> Any:
    """删除团队"""
    try:
        team = await team_service.get_team(db, team_id=team_id)
        if not team or team.owner_id != current_user.id:
            return ResponseModel(
                code=201,
                msg="团队不存在或无权限",
                data={}
            )
        await team_service.delete_team(db, team_id=team_id)
        return ResponseModel(
            code=200,
            msg="删除成功",
            data={"team_id": team_id}
        )
    except Exception as e:
        logger.error(f"删除团队错误: {str(e)}")
        return ResponseModel(
            code=201,
            msg="删除团队失败",
            data={"error": f"{str(e)}"}
        ) 