from sqlmodel import Field, SQLModel
from uuid import UUID, uuid4


class Item(SQLModel, table=True):
    __tablename__ = "items"
    id : UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    name : str
    description : str | None = None
    price : float
    quantity : int | None = None
    is_offer : bool | None = None
    owner_id : UUID = Field(foreign_key="users.id", nullable=False)
    in_stock : bool = True