from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from backend.app.schemas.comment_schema import Read_comment
from backend.app.db.session import get_session
from backend.app.core.security import get_current_active_user
from backend.app.models.user_model import User 
from backend.app.models.product_model import product, Comment
from backend.app.services.crud_service import product_crud 
from backend.app.services.crud_service import comment_crud
from uuid import UUID



router = APIRouter(tags=["Comments"])

@router.post("/comment/{product_id}", response_model=Read_comment)
def create_post(
    product_id: UUID,
    post_data: Read_comment,
    db: Session = Depends(get_session),
    current_user : User = Depends(get_current_active_user),
):
     product = product_crud.get_product(db, product_id)
     if not product:
          raise HTTPException(status_code=404, detail= "no product found")
     db_comment = Comment(**post_data.dict(), product_id = product_id, owner_id=current_user.id)
     if not db_comment:
          raise HTTPException(status_code=404, detail = "comment can't be created")
     comment = comment_crud.create(db, db_comment)
     return comment