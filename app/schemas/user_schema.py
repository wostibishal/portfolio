from pydantic import BaseModel
from uuid import UUID

class userBAse(BaseModel):
    first_name: str
    last_name: str
    email: str
    is_active: bool = True

    class Config:
        from_attributes = True

class UserCreate(userBAse):
    password: str

class UserRead(userBAse):
    id: UUID
   
    class Config:
        from_attributes = True
   


class loginSchema(BaseModel):
    email: str
    password: str
    
    class Config:
        from_attributes = True