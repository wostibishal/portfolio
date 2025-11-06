from datetime import datetime
from sqlmodel import SQLModel
from uuid import UUID

class userBAse(SQLModel):
    first_name: str
    last_name: str
    email: str
    role: str


class UserCreate(userBAse):
    password: str
    is_active: bool = True
    created_at: str = datetime.now()


class UserRead(userBAse):
    id: UUID
   
    class Config:
        from_attributes = True
   


