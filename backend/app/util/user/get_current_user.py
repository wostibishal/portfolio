from fastapi import Depends, HTTPException, status
from sqlmodel import Session
import jwt
from jwt.exceptions import InvalidTokenError
from backend.app.core.config import SECRET_KEY, ALGORITHM, oauth2_scheme
from backend.app.models.user_model import User
from backend.app.db.session import get_session
from typing import Optional
from backend.app.util.user.get_user import get_user

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_session),
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: Optional[str] = payload.get("email")
        if email is None:
            raise credentials_exception
    except InvalidTokenError:
        raise credentials_exception
    user = get_user(db, email=email)
    if user is None:
        raise credentials_exception
    return user
