from pydantic import BaseModel, EmailStr
from uuid import UUID
from typing import Optional
from datetime import datetime
from backend.app.core.enum import Role

class UserCreateBase(BaseModel):
    email: EmailStr
    password: str
    first_name: str
    last_name: str

class RetailerRegister(UserCreateBase):
    brand_name: str
    
class DisplayUser(BaseModel):
    id : UUID
    first_name: str
    last_name: str
    email : EmailStr

    class Config:
        from_attributes = True

class DisplayRetailer(DisplayUser):
    brand_name : Optional[str] = None

    class Config:
        from_attributes = True

class SuperDisplayUser(DisplayRetailer):
    role : Optional[Role]
    is_active : bool
    created_at : datetime
    strike_count: Optional[int] = None
    is_verified : Optional[bool] = None

    class Config:
        from_attributes = True



class ReadUser(BaseModel):
    email : EmailStr

    class Config:
        from_attributes = True

class UpdateUser(BaseModel):
    first_name: str
    last_name: str
    email : str
    password: str


class UpdateRetailer(UpdateUser):
    brand_name : Optional[str] = None

    class Config:
        from_attributes = True 
        

class SuperUpdate(UpdateRetailer):
    strike_count: Optional[int] = None 
    is_verified : Optional[bool] = None
    is_active : Optional[bool] 

    class Config:
        from_attributes = True 

class DeleteUser(BaseModel):
    email: EmailStr

    class Config:
        from_attributes = True 

class UpdatePassword(BaseModel):
   
    current_password: str
    password : str
    password2: str

    class Config:
        from_attributes = True