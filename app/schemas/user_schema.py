from datetime import datetime
from sqlmodel import SQLModel
from uuid import UUID
from backend.app.services import Role

class userBAse(SQLModel):
    first_name: str
    last_name: str
    email: str


class UserCreate(userBAse):
    password: str
    is_active: bool = True
    created_at: str = datetime.now()


class UserRead(userBAse):
    id: UUID
    role: Role
   
    class Config:
        from_attributes = True
   


