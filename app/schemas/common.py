"""
通用响应模型
"""

from typing import Generic, TypeVar, Optional, Union, Dict, Any
from pydantic import BaseModel

DataT = TypeVar('DataT')

class ResponseModel(BaseModel, Generic[DataT]):
    """统一响应模型
    
    支持两种数据格式：
    1. 成功响应：直接返回数据对象
    2. 错误响应：返回包含错误信息的字典
    """
    code: int = 200
    msg: str = "操作成功"
    data: Union[DataT, Dict[str, Any], str] = {} 