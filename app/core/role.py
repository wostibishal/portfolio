from functools import wraps
from typing import List
from fastapi import Depends, HTTPException, status
from backend.app.core.security import get_current_active_user

def role_required(allowed_roles: List[str]):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, current_user=Depends(get_current_active_user), **kwargs):
            if current_user.role not in allowed_roles:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Access denied. Requires roles: {allowed_roles}"
                )
            return await func(*args, **kwargs)
        return wrapper
    return decorator
