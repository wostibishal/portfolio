from sqlmodel import SQLModel, Field, Relationship
from uuid import uuid4, UUID
from datetime import datetime
from backend.app.models.product_model import Product

class Rating(SQLModel, table=True):
    __tablename__ = "rating"
    id : UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    score : int
    costuemr_id : UUID = Field(foreign_key="costumer.id", nullable=False)
    product_id : UUID = Field(foreign_key="product.id", nullable=False)
    created_at: str = Field(default=datetime.now())
    product : Product = Relationship(back_populates="rating")