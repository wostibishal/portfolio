from fastapi import Depends, HTTPException, status
from backend.app.models.user_model import User
from backend.app.util.user.get_current_user import get_current_user

async def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:
    if getattr(current_user, "is_active", True) is False:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Inactive user"
        )    
    return current_user
