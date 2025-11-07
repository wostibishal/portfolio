from sqlmodel import SQLModel, Field, Relationship
from uuid import uuid4, UUID
from datetime import datetime
from backend.app.models.product_model import Product

class Comment(SQLModel, table=True):
    __tablename__ = "comments"
    id : UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    content: str
    owner_id: UUID = Field(foreign_key="costumer.id", nullable=False)
    product_id: UUID = Field(foreign_key="products.id", nullable=False)
    created_at: str = Field(default= datetime.now())
    updated_at: str | None = None
    is_visible: bool = True