from sqlmodel import Field, SQLModel, Relationship
from uuid import uuid4, UUID
from datetime import datetime, timezone
from backend.app.core.enum import Role
from typing import  Optional, List


from backend.app.models.product_model import Product
from backend.app.models.rating_model import Review
from backend.app.models.order_model import Order



class User(SQLModel, table=True):
    __tablename__ = "users"

    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    email: str = Field(unique=True, index=True)
    hashed_password: str
    first_name: str
    last_name: str
    
    role: Role = Field(default=Role.COSTUMER)
    is_active: bool = True
    created_at: datetime = Field(default_factory=lambda:datetime.now(timezone.utc))

    # Relationships
    retailer_profile: Optional["RetailerProfile"] = Relationship(
        back_populates="user", 
        sa_relationship_kwargs={"uselist": False}
    )
    orders: List["Order"] = Relationship(back_populates="user")
    products: List["Product"] = Relationship(back_populates="seller")
    reviews: List["Review"] = Relationship(back_populates="user")

class RetailerProfile(SQLModel, table=True):
    __tablename__ = "retailer_profiles"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="users.id", unique=True)
    
    brand_name: str
    strike_count: int = Field(default=0)
    is_verified: bool = Field(default=False)

    user: "User" = Relationship(back_populates="retailer_profile")