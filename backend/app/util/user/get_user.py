from sqlmodel import Session, select
from typing import Optional
from backend.app.models.user_model import User 


def get_user(db: Session, email: str) -> Optional[User]:
    statement = select(User).where(User.email == email)
    user = db.exec(statement).first()
    return user