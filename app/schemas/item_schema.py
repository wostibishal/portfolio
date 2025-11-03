from uuid import UUID
from sqlmodel import SQLModel


# ------------------------------create schema------------------------------------------------------

class Read_item(SQLModel):
    id: UUID
    image : str
    name: str
    description: str | None = None
    price: float
    is_offer: bool | None = None

    class Config:
        from_attributes=True

class Create_item(SQLModel):
    image: str
    name: str
    description: str | None = None
    price: float
    is_offer: bool | None = None
    quantity: int | None = None
    in_stock: bool = True

    class Config:
        from_attributes=True


#----------------------------- output schema ----------------------------------------------------------

class Update_item(SQLModel):
    id : UUID
    message: str = "Item updated successfully"
    class Config:
        from_attributes=True

class Delete_item(SQLModel):
    id: UUID
    message: str = "Item deleted successfully"

    class Config:
        from_attributes=True