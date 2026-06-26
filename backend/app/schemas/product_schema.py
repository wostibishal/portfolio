from uuid import UUID
from sqlmodel import SQLModel
from typing import Optional
from decimal import Decimal

# ------------------------------create schema------------------------------------------------------

class product(SQLModel):
    id: Optional[UUID]
    image_url : Optional[str] = None
    name: str
    description: str | None = None
    

class Read_product(product):
    
    price: float
    category : str


class Create_product(Read_product):
    
    is_offer: bool | None = None
    quantity: int | None = None
    in_stock: bool = True

    class Config:
        from_attributes=True


#----------------------------- output schema ----------------------------------------------------------

class Update_product(Create_product):
    

class Delete_product(SQLModel):
    id: UUID
    message: str = "product deleted successfully"

    class Config:
        from_attributes=True

class DisplayProducts(SQLModel):
    title : str 
    description : str
    price : Decimal
