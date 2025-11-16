from sqlmodel import Field, SQLModel, Relationship
from uuid import UUID, uuid4
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from backend.app.models.user_model import Retailer
    from backend.app.models.comment_model import Comment
    from backend.app.models.rating_model import Rating


class Product(SQLModel, table=True):
    __tablename__ = "product"

    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    name: str
    image_url: str | None = None
    description: str | None = None
    price: float
    quantity: int | None = None
    is_offer: bool | None = None
    owner_id: UUID = Field(foreign_key="retailer.id", nullable=False)
    category_id: UUID | None = None
    in_stock: bool = True

    retailer: "Retailer" = Relationship(back_populates="product")
    comments: list["Comment"] = Relationship(back_populates="product")
    ratings: list["Rating"] = Relationship(back_populates="product")
