from sqlmodel import SQLModel, Field, Relationship
from uuid import UUID, uuid4
from backend.app.models.product_model import Product

class Category(SQLModel, table=True):
    __table__ = "category"
    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    name: str
    sub_category: str
    product: list["Product"] = Relationship(back_populates="category")