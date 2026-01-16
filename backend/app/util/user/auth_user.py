
from sqlmodel import Session
from typing import Optional
from backend.app.models.user_model import User
from backend.app.util.user.get_user import get_user
from backend.app.util.user.verify_password import verify_password


def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
    user = get_user(db, email=email )
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user