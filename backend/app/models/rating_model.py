from sqlmodel import SQLModel, Field, Relationship
from uuid import uuid4, UUID
from datetime import datetime, timezone
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from backend.app.models.product_model import Product
    from backend.app.models.user_model import User


class Review(SQLModel, table=True):
   
    __tablename__ = "reviews"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="users.id")
    product_id: UUID = Field(foreign_key="products.id")
    
    rating: int = Field(ge=1, le=5) # 1 to 5 stars
    comment: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda:datetime.now(timezone.utc))

    user: "User" = Relationship(back_populates="reviews")
    product: "Product" = Relationship(back_populates="reviews")