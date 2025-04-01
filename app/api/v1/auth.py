"""
认证相关的API路由
"""

from datetime import timedelta
from typing import Any
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app import schemas, models
from app.api import deps
from app.core import security
from app.core.config import settings
from app.services.user_service import UserService
from app.schemas.common import ResponseModel
import logging

logger = logging.getLogger(__name__)
router = APIRouter()
user_service = UserService()

@router.post("/register", response_model=ResponseModel[schemas.User])
async def register(
    *,
    db: Session = Depends(deps.get_mysql_db),
    user_in: schemas.UserCreate,
) -> Any:
    """用户注册"""
    try:
        # 根据邮箱查询用户
        user = await user_service.get_by_email(db, email=user_in.email)
        # 如果用户存在，返回已注册的提示
        if user:
            return ResponseModel(
                code=201,
                msg="该邮箱已被注册",
                data={"error": "该邮箱已被注册"}
            )
        # 如果用户不存在，创建新用户
        user = await user_service.create(db, obj_in=user_in)
        # 返回注册成功的提示
        return ResponseModel(
            code=200,
            msg="注册成功",
            data=user
        )
    except Exception as e:
        # 记录错误日志
        logger.error(f"注册错误: {str(e)}")
        # 返回注册过程中发生错误的提示
        return ResponseModel(
            code=201,
            msg="注册过程中发生错误",
            data={"error": f"注册错误: {str(e)}"}
        )

@router.post("/login", response_model=ResponseModel[schemas.Token])
async def login(
    db: Session = Depends(deps.get_mysql_db),
    form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """用户登录"""
    try:
        # 根据用户名和密码进行用户认证
        user = await user_service.authenticate(
            db, email=form_data.username, password=form_data.password
        )
        # 如果用户不存在或密码错误
        if not user:
            return ResponseModel(
                code=201,
                msg="邮箱或密码错误",
                data={"error": "邮箱或密码错误"}
            )
        # 如果用户已被禁用
        elif not user.is_active:
            return ResponseModel(
                code=201,
                msg="该用户已被禁用",
                data={"error": "该用户已被禁用"}
            )

        # 设置access_token的过期时间
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        # 生成access_token
        access_token = security.create_access_token(
            user.id, expires_delta=access_token_expires
        )
        # 返回登录成功的信息
        return ResponseModel(
            code=200,
            msg="登录成功",
            data={
                "access_token": access_token,
                "token_type": "bearer"
            }
        )
    except Exception as e:
        logger.error(f"登录错误: {str(e)}")
        return ResponseModel(
            code=201,
            msg="登录失败",
            data={"error": f"{str(e)}"}
        )

@router.post("/password-recovery/{email}", response_model=ResponseModel[dict])
async def recover_password(email: str, db: Session = Depends(deps.get_mysql_db)) -> Any:
    """密码重置"""
    # 根据邮箱获取用户信息
    user = await user_service.get_by_email(db, email=email)
    # 如果没有找到对应的用户，返回未找到该邮箱对应的用户
    if not user:
        return ResponseModel(
            code=201,
            msg="未找到该邮箱对应的用户",
            data={}
        )
    # TODO: 发送密码重置邮件
    # 返回密码重置邮件已发送
    return ResponseModel(
        code=200,
        msg="密码重置邮件已发送",
        data={"email": email}
    ) 