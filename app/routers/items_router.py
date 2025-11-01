
from fastapi import APIRouter, Depends, HTTPException
from backend.app.db.session import get_session
from backend.app.core.security import get_current_active_user
from sqlmodel import Session, select
from backend.app.models.item_model import Item
from backend.app.schemas.item_schema import Read_item, Create_item, Update_item, Delete_item
from uuid import UUID
from backend.app.models.user_model import User



router = APIRouter(tags=["Items"])

@router.post("/create/", response_model=Read_item)
def create_item(
    item_data: Create_item,
    db: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_user)
):
    db_item = Item(**item_data.dict(), owner_id=current_user.id)
    if not db_item:
        raise HTTPException(status_code=400, detail="Item could not be created")
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return Read_item.from_orm(db_item)



@router.get("/items/", response_model=list[Read_item])
async def read_items(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_session),
):
    items = await db.exec(select(Item).offset(skip).limit(limit)).all()
    if not items:
        raise HTTPException(status_code=404, detail="No items found")
    return items


@router.get("/{item_id}/", response_model=Read_item)
def read_single_item(
    item_id: UUID,
    db: Session = Depends(get_session),
):
    item = db.get(Item, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return Read_item.from_orm(item)


@router.get("/my_items/", response_model=list[Read_item])
async def read_user_items(
    skip: int = 0,
    limit: int = 10,
    db: Session =  Depends(get_session),
    current_user: User = Depends(get_current_active_user),
):
    print(current_user.id)
    print()
    items = await db.exec(select(Item).filter(Item.owner_id == current_user.id).offset(skip).limit(limit)).all()
    print(items)
    if not items:
        raise HTTPException(status_code=404, detail="No items found for this user")
    return items


@router.delete("/delete/{item_id}/", response_model=Delete_item)
def delete_item(
    item_id: UUID,
    db: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_user),
):
    item = db.get(Item, item_id)
    if not item or item.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Item not found")
    db.delete(item)
    db.commit()
    return Delete_item(id=item_id)

@router.put("/update/{item_id}/", response_model=Update_item)
def update_item(
    item_id: UUID,
    item_data: Create_item,
    db: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_user),
):
    item = db.get(Item, item_id)
    if not item or item.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Item not found")
    for key, value in item_data.dict().items():
        setattr(item, key, value)
    db.add(item)
    db.commit()
    db.refresh(item)
    return Update_item.from_orm(item)

