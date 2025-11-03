from sqlmodel import Field, SQLModel
from uuid import UUID, uuid4


class Item(SQLModel, table=True):
    __tablename__ = "items"
    id : UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    name : str
    image_url : str | None =None 
    description : str | None = None
    price : float
    quantity : int | None = None
    is_offer : bool | None = None
    owner_id : UUID = Field(foreign_key="users.id", nullable=False)
    in_stock : bool = True

class Rating(SQLModel, table=True):
    __tablename__ = "ratings"
    id : UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    score : int
    reviewer_id : UUID = Field(foreign_key="users.id", nullable=False)
    item_id : UUID = Field(foreign_key="items.id", nullable=False)

class Comment(SQLModel, table=True):
    __tablename__ = "comments"
    id : UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    content: str
    author_id: UUID = Field(foreign_key="users.id", nullable=False)
    item_id: UUID = Field(foreign_key="items.id", nullable=False)
    created_at: str = Field(default_factory=lambda: __import__('datetime').datetime.utcnow().isoformat())
    updated_at: str | None = None
    is_visible: bool = True
    