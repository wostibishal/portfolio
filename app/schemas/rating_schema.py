from sqlmodel import SQLModel, Field
from uuid import UUID


class Read_rating(SQLModel):
    item_id: UUID
    average_score: float | None = None

    class Config:
        from_attributes = True

class Create_rating(SQLModel):
    score: int
    item_id: UUID

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