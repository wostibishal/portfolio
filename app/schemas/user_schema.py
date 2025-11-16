from datetime import datetime
from sqlmodel import SQLModel, Field
from uuid import UUID
from backend.app.core.role import Role

class userBase(SQLModel):
    first_name: str
    last_name: str
    email: str
    is_active: bool 
    created_at: str 


class CreateUser(userBase):
    password: str
   
 
class CreateUserRetailer(CreateUser):
    brand : str

class UserRead(userBase):
    id: UUID
    role: Role
   
    class Config:
        from_attributes = True
   
class UpdateUser(CreateUserRetailer):
    is_active: bool = False
    had_strike: bool = False
    strike: int = Field(default= 0)
    brand: str = Field(default= None)

    class Config:
        form_attributes = True

class deleteUser(SQLModel):
    id : UUID
