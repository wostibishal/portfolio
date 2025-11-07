from sqlmodel import SQLModel
from uuid import UUID


class Read_rating(SQLModel):
    product_id: UUID 
    average_score: float | None = None

    class Config:
        from_attributes = True

class Create_rating(SQLModel):
    score: int
    product_id: UUID

    class Config:
        from_attributes = True

class Update_rating(SQLModel):
    score: int | None = None

    class Config:
        from_attributes = True

class Delete_rating(SQLModel):
    id: UUID

    class Config:
        from_attributes = True