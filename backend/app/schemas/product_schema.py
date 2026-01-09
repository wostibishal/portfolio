from uuid import UUID
from sqlmodel import SQLModel
from typing import Optional

# ------------------------------create schema------------------------------------------------------

class product(SQLModel):
    id: UUID
    image_url : Optional[str] = None
    name: str
    description: str | None = None
    

class Read_product(SQLModel):
    
    price: float
    category : str


    class Config:
        from_attributes=True


class Create_product(SQLModel):
    
    is_offer: bool | None = None
    quantity: int | None = None
    in_stock: bool = True

    class Config:
        from_attributes=True


#----------------------------- output schema ----------------------------------------------------------

class Update_product(SQLModel):
   

    class Config:
        from_attributes=True

class Delete_product(SQLModel):
    id: UUID
    message: str = "product deleted successfully"

    class Config:
        from_attributes=True