from fastapi import APIRouter
from app.api.v1 import auth, accounts, posts, teams, devices, analytics

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["认证"])
api_router.include_router(accounts.router, prefix="/accounts", tags=["账号管理"])
api_router.include_router(posts.router, prefix="/posts", tags=["内容发布"])
api_router.include_router(teams.router, prefix="/teams", tags=["团队管理"])
api_router.include_router(devices.router, prefix="/devices", tags=["设备管理"])
api_router.include_router(analytics.router, prefix="/analytics", tags=["数据分析"]) 