
from fastapi import APIRouter, Depends, HTTPException
from backend.app.db.session import get_session
from backend.app.core.security import get_current_active_user
from backend.app.services.user_services import role_required
from sqlmodel import Session, select
from backend.app.schemas.product_schema import Read_product, Create_product, Update_product, Delete_product
from uuid import UUID
from backend.app.models.user_model import User, Retailer
from backend.app.models.product_model import product
from backend.app.services.crud_service import product_crud




router = APIRouter(tags=["products"])

@router.post("/create/", response_model=Read_product)
@role_required(["admin","retailer"])
def create_product(
    product_data: Create_product,
    db: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_user)
    
):
    db_product = product(**product_data.dict(), owner_id=current_user.id)
    if not db_product:
        raise HTTPException(status_code=400, detail="product could not be created")
    product = product_crud.create(db , db_product)
    return product 


@router.get("/products/", response_model=list[Read_product])
async def read_products(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_session),
):
    products = product_crud.get_all(db, skip, limit)
    if not products:
        raise HTTPException(status_code=404, detail="No products found")
    return products


@router.get("/my_products/", response_model=list[Read_product])
@role_required(["admin","retailer"])
async def read_my_products(
    skip: int = 0,
    limit: int = 10,
    db: Session =  Depends(get_session),
    current_user: User = Depends(get_current_active_user),
):
    products = product_crud.get_by_user(db, current_user.id, skip, limit)
    if not products:
        raise HTTPException(status_code=404, detail="No products found for this user")
    return products


@router.get("/retailer_products/{retailer_id}", response_model=list[Read_product])
async def read_retailer_products(
    retailer_id : UUID,
    skip: int = 0,
    limit:int = 10,
    db: Session = Depends(get_session),
):
    user = select(Retailer).where(Retailer.id == retailer_id)
    products = product_crud.get_by_user(db, user.id, skip, limit)
    if not products:
        raise HTTPException(status_code=404, detail="No products found from the user")
    return products


@router.get("/{product_id}/", response_model=Read_product)
def read_single_product(
    product_id: UUID,
    db: Session = Depends(get_session),
):
    product = product_crud.get(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="product not found")
    return product 


@router.delete("/delete/{product_id}/", response_model=Delete_product)
@role_required(["admin","retailer"])
def delete_product(
    product_id: UUID,
    db: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_user),
):
    product = product_crud.get_single(db, product_id)
    if not product or product.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="product not found")
    product_crud.delete(db,product)
    return Delete_product(id=product_id)


@router.put("/update/{product_id}/", response_model=Update_product)
@role_required(["admin","retailer"])
def update_product(
    product_id: UUID,
    product_data: Create_product,
    db: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_user),
):
    product = product_crud.get_single(db, product_id)
    if not product or product.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="product not found")
    
    product_crud.update(db, product, product_data)
    return Update_product(id= product_id)

