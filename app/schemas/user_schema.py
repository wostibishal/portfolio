from sqlmodel import SQLModel
from uuid import UUID

class userBAse(SQLModel):
    first_name: str
    last_name: str
    email: str
    is_active: bool = True

    class Config:
        from_attributes = True

class UserCreate(userBAse):
    password: str

class UserRead(SQLModel):
    id: UUID
   
    class Config:
        from_attributes = True
   


class loginSchema(SQLModel):
    email: str
    password: str
    
    class Config:
        from_attributes = True