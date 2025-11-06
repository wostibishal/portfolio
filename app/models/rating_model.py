from sqlmodel import SQLModel, Field
from uuid import uuid4, UUID
from datetime import datetime

class Rating(SQLModel, table=True):
    __tablename__ = "ratings"
    id : UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    score : int
    costuemr_id : UUID = Field(foreign_key="costumer.id", nullable=False)
    item_id : UUID = Field(foreign_key="items.id", nullable=False)
    created_at: str = Field(default=datetime.now())
