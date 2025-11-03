from uuid import UUID
from sqlmodel import  SQLModel


class Read_comment(SQLModel):
    id: UUID
    author_id: UUID
    content: str

    class Config:
        from_attributes=True

class Create_comment(SQLModel):
    content: str
    item_id: UUID

    class Config:
        from_attributes=True

class Update_comment(SQLModel):
    content: str | None = None
    is_visible: bool | None = None

    class Config:
        from_attributes=True

class Delete_comment(SQLModel):
    id: UUID

    class Config:
        from_attributes=True