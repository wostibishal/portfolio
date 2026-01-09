from sqlmodel import Field, SQLModel, Relationship
from uuid import UUID, uuid4
from decimal import Decimal
from datetime import datetime, timezone
from backend.app.core.enum import OrderStatus
from typing import List, TYPE_CHECKING
if TYPE_CHECKING:
    from backend.app.models.user_model import User
    from backend.app.models.product_model import Product


class Order(SQLModel, table=True):
    __tablename__ = "orders"

    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    user_id: UUID = Field(foreign_key="users.id")
    
    status: OrderStatus = Field(default=OrderStatus.PENDING)
    total_amount: Decimal = Field(default=0.0, max_digits=10, decimal_places=2)
    shipping_address: str
    
    created_at: datetime = Field(default_factory=lambda:datetime.now(timezone.utc))

    # Relationships
    user: "User" = Relationship(back_populates="orders")
    items: List["OrderItem"] = Relationship(back_populates="order")

class OrderItem(SQLModel, table=True):
    __tablename__ = "order_items"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    order_id: UUID = Field(foreign_key="orders.id")
    product_id: UUID = Field(foreign_key="products.id")
    
    quantity: int
    price_at_purchase: Decimal = Field(max_digits=10, decimal_places=2)

    order: "Order" = Relationship(back_populates="items")
    product: "Product" = Relationship(back_populates="order_items")
