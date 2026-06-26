from fastapi import Depends, HTTPException, status
from sqlmodle import Session, select
from backend.app.db.session import get_session
from backend.app.models.user_model import User
from backend.app.util.user.get_current_active_user import get_current_active_user

def get_products(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_session),
) -> List[DisplayProducts]: