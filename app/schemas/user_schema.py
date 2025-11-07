from datetime import datetime
from sqlmodel import SQLModel, Field
from uuid import UUID
from backend.app.services.user_services import Role

class userBase(SQLModel):
    first_name: str
    last_name: str
    email: str


class UserCreate(userBase):
    password: str
    is_active: bool = True
    created_at: str = datetime.now()


class UserRead(userBase):
    id: UUID
    role: Role
   
    class Config:
        from_attributes = True
   


class UpdateUser(UserCreate):
    is_active: bool = False
    had_strike: bool = False
    strike: int = Field(default= 0)
    brand: str = Field(default= None)

    class Config:
        form_attributes = True