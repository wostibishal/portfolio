from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from backend.app.schemas.comment_schema import Read_comment
from backend.app.db.session import get_session
from backend.app.core.security import get_current_active_user
from backend.app.models.user_model import User 
from backend.app.models.item_model import Item, Comment
from backend.app.services.crud_service import item_crud 
from backend.app.services.crud_service import comment_crud
from uuid import UUID



router = APIRouter(tags=["Comments"])

@router.post("/comment/{item_id}", response_model=Read_comment)
def create_post(
    item_id: UUID,
    post_data: Read_comment,
    db: Session = Depends(get_session),
    current_user : User = Depends(get_current_active_user),
):
     item = item_crud.get_item(db, item_id)
     if not item:
          raise HTTPException(status_code=404, detail= "no item found")
     db_comment = Comment(**post_data.dict(), item_id = item_id, owner_id=current_user.id)
     if not db_comment:
          raise HTTPException(status_code=404, detail = "comment can't be created")
     comment = comment_crud.create(db, db_comment)
     return comment