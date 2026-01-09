from sqlmodel import Field, SQLModel, Relationship
from uuid import UUID, uuid4
from typing import Optional, List, TYPE_CHECKING
from datetime import datetime, timezone
from decimal import Decimal

if TYPE_CHECKING:
    from backend.app.models.order_model import OrderItem
    from backend.app.models.rating_model import Review
    from backend.app.models.user_model import User

class Category(SQLModel, table=True):
    __tablename__ = "categories"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    name: str = Field(index=True)
    slug: str = Field(unique=True) # e.g., "electronics-laptops"
    
    # Relationships
    products: List["Product"] = Relationship(back_populates="category")


class Product(SQLModel, table=True): 

    __tablename__ = "products"

    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    seller_id: UUID = Field(foreign_key="users.id")
    category_id: Optional[UUID] = Field(default=None, foreign_key="categories.id")
    
    title: str
    description: str
    price: Decimal = Field(default=0.0, max_digits=10, decimal_places=2)
    stock_quantity: int = Field(default=0)
    image_url: Optional[str] = None
    
    created_at: datetime = Field(default_factory=lambda:datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda:datetime.now(timezone.utc))

    # Relationships
    seller: "User" = Relationship(back_populates="products")
    category: Optional["Category"] = Relationship(back_populates="products")
    order_items: List["OrderItem"] = Relationship(back_populates="product")
    reviews: List["Review"] = Relationship(back_populates="product")
