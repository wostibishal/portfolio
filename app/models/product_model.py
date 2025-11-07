from sqlmodel import Field, SQLModel, Relationship
from uuid import UUID, uuid4
from backend.app.models.comment_model import Comment



class Product(SQLModel, table=True):
    __tablename__ = "product"
    id : UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    name : str
    image_url : str | None =None 
    description : str | None = None
    price : float
    quantity : int | None = None
    is_offer : bool | None = None
    owner_id : UUID = Field(foreign_key="retailer.id", nullable=False)
    category_id : UUID = Field(foreign_key="category.id", nullable=False)
    in_stock : bool = True
    comments : list["Comment"] = Relationship(back_populate="product")