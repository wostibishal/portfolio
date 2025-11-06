
from fastapi import APIRouter, Depends, HTTPException
from backend.app.db.session import get_session
from backend.app.core.security import get_current_active_user
from backend.app.services import Role_required
from sqlmodel import Session
from backend.app.schemas.item_schema import Read_item, Create_item, Update_item, Delete_item
from uuid import UUID
from backend.app.models.user_model import User
from backend.app.models.item_model import Item
from backend.app.services.crud_service import item_crud



router = APIRouter(tags=["Items"])

@router.post("/create/", response_model=Read_item)
@role_required(["admin","retailer"])
def create_item(
    item_data: Create_item,
    db: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_user)
    
):
    db_item = Item(**item_data.dict(), owner_id=current_user.id)
    if not db_item:
        raise HTTPException(status_code=400, detail="Item could not be created")
    item = item_crud.create(db , db_item)
    return item 

@router.get("/items/", response_model=list[Read_item])
async def read_items(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_session),
):
    items = item_crud.get_all(db, skip, limit)
    if not items:
        raise HTTPException(status_code=404, detail="No items found")
    return items

@router.get("/my_items/", response_model=list[Read_item])
@role_required(["admin","retailer"])
async def read_my_items(
    skip: int = 0,
    limit: int = 10,
    db: Session =  Depends(get_session),
    current_user: User = Depends(get_current_active_user),
):
    items = item_crud.get_by_user(db, current_user.id, skip, limit)
    if not items:
        raise HTTPException(status_code=404, detail="No items found for this user")
    return items

@router.get("/retailer_items", response_model=list[Read_item])
async def read_retailer_items(
    skip: int = 0,
    limit:int = 10,
    db: Session = Depends(get_session),
):
    user = 


@router.get("/{item_id}/", response_model=Read_item)
def read_single_item(
    item_id: UUID,
    db: Session = Depends(get_session),
):
    item = item_crud.get(db, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item 

@router.delete("/delete/{item_id}/", response_model=Delete_item)
@role_required(["admin","retailer"])
def delete_item(
    item_id: UUID,
    db: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_user),
):
    item = item_crud.get_single(db, item_id)
    if not item or item.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Item not found")
    item_crud.delete(db,item)
    return Delete_item(id=item_id)

@router.put("/update/{item_id}/", response_model=Update_item)
@role_required(["admin","retailer"])
def update_item(
    item_id: UUID,
    item_data: Create_item,
    db: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_user),
):
    item = item_crud.get_single(db, item_id)
    if not item or item.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Item not found")
    
    item_crud.update(db, item, item_data)
    return Update_item(id= item_id)

