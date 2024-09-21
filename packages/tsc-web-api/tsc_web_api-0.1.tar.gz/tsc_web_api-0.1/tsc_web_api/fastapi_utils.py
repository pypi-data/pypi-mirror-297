from fastapi import status, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials


def get_bearer_validator(tokens: list[str]):
    """获取简单验证 Bearer Token 的依赖
    路由加入 dependencies=[Depends(get_bearer_validator(tokens))] 使用
    
    Args:
        tokens (list[str]): 允许的 token 列表
    
    Returns:
        Callable[..., None]: 依赖
    """
    def bearer_validator(credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())):
        token = credentials.credentials
        if token not in tokens:
            raise HTTPException(status.HTTP_403_FORBIDDEN, detail="Invalid or expired token")
    return bearer_validator
