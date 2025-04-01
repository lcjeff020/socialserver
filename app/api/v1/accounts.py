"""
账号管理API模块

提供社交媒体账号管理功能：
1. 账号添加和认证
2. 账号信息更新
3. 账号列表获取
4. 账号数据统计
"""

from typing import Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import models, schemas
from app.api import deps
from app.services.account_service import AccountService
from app.utils.logger import logger
from app.schemas.common import ResponseModel

router = APIRouter()
account_service = AccountService()

@router.post("/", response_model=ResponseModel[schemas.Account])
async def create_account(
    *,
    db: Session = Depends(deps.get_mysql_db),
    account_in: schemas.AccountCreate,
    current_user: models.User = Depends(deps.get_current_user)
) -> Any:
    """
    添加新的社交媒体账号
    """
    try:
        # 检查是否已存在相同平台账号
        existing_account = await account_service.get_account_by_platform(
            db=db,
            user_id=current_user.id,
            platform=account_in.platform,
            platform_id=account_in.platform_id
        )
        if existing_account:
            return ResponseModel(
                code=201,
                msg="该平台账号已存在",
                data={}
            )

        account = await account_service.create_account(
            db=db,
            account_in=account_in,
            user_id=current_user.id
        )
        return ResponseModel(
            code=200,
            msg="创建成功",
            data=account
        )

    except Exception as e:
        logger.error(f"创建账号错误: {str(e)}")
        return ResponseModel(
            code=201,
            msg="创建账号失败",
            data={"error": f"{str(e)}"}
        )

@router.get("/", response_model=ResponseModel[List[schemas.Account]])
async def get_accounts(
    db: Session = Depends(deps.get_mysql_db),
    skip: int = 0,
    limit: int = 100,
    platform: Optional[str] = None,
    current_user: models.User = Depends(deps.get_current_user)
) -> Any:
    """
    获取用户的社交媒体账号列表
    """
    try:
        accounts = await account_service.get_user_accounts(
            db=db,
            user_id=current_user.id,
            skip=skip,
            limit=limit,
            platform=platform
        )
        return ResponseModel(
            code=200,
            msg="获取成功",
            data=accounts
        )
    except Exception as e:
        logger.error(f"获取账号列表错误: {str(e)}")
        return ResponseModel(
            code=201,
            msg="获取账号列表失败",
            data={"error": f"{str(e)}"}
        )

@router.get("/{account_id}", response_model=schemas.Account)
async def get_account(
    *,
    db: Session = Depends(deps.get_mysql_db),
    account_id: int,
    current_user: models.User = Depends(deps.get_current_user)
) -> Any:
    """
    获取特定账号的详细信息
    """
    account = await account_service.get_account(db=db, account_id=account_id)
    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Account not found"
        )
    if account.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    return account

@router.put("/{account_id}", response_model=schemas.Account)
async def update_account(
    *,
    db: Session = Depends(deps.get_mysql_db),
    account_id: int,
    account_in: schemas.AccountUpdate,
    current_user: models.User = Depends(deps.get_current_user)
) -> Any:
    """
    更新账号信息
    """
    account = await account_service.get_account(db=db, account_id=account_id)
    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Account not found"
        )
    if account.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    try:
        account = await account_service.update_account(
            db=db,
            account=account,
            account_in=account_in
        )
        return account
    except Exception as e:
        logger.error(f"Update account error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.delete("/{account_id}", response_model=ResponseModel[dict])
async def delete_account(
    *,
    db: Session = Depends(deps.get_mysql_db),
    account_id: int,
    current_user: models.User = Depends(deps.get_current_user)
) -> Any:
    """
    删除账号
    """
    try:
        account = await account_service.get_account(db=db, account_id=account_id)
        if not account or account.user_id != current_user.id:
            return ResponseModel(
                code=201,
                msg="账号不存在或无权限",
                data={}
            )
        
        await account_service.delete_account(db=db, account_id=account_id)
        return ResponseModel(
            code=200,
            msg="删除成功",
            data={"account_id": account_id}
        )
    except Exception as e:
        logger.error(f"删除账号错误: {str(e)}")
        return ResponseModel(
            code=201,
            msg="删除账号失败",
            data={"error": f"{str(e)}"}
        )

@router.post("/{account_id}/refresh-token")
async def refresh_account_token(
    *,
    db: Session = Depends(deps.get_mysql_db),
    account_id: int,
    current_user: models.User = Depends(deps.get_current_user)
) -> Any:
    """
    刷新账号的访问令牌
    """
    account = await account_service.get_account(db=db, account_id=account_id)
    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Account not found"
        )
    if account.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    try:
        result = await account_service.refresh_token(db=db, account=account)
        return result
    except Exception as e:
        logger.error(f"Refresh token error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        ) 