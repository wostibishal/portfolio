from uuid import UUID
from sqlmodel import  SQLModel


class Read_item(SQLModel):
    id: UUID
    name: str
    description: str | None = None
    price: float
    is_offer: bool | None = None

    class Config:
        from_attributes=True

class Create_item(SQLModel):
    name: str
    description: str | None = None
    price: float
    is_offer: bool | None = None
    quantity: int | None = None
    in_stock: bool = True

    class Config:
        from_attributes=True


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