from sqlmodel import Field, SQLModel
from uuid import  uuid4, UUID
from enum import Enum
from pydantic import EmailStr
from datetime import datetime


class Role(str, Enum):
   SUPER = 'super'
   COSTUMER = 'costumer'
   RETAILER = 'retailer'


class User(SQLModel):
   id : UUID = Field(default_factory=uuid4, primary_key=True, index=True)
   first_name : str
   last_name : str
   email : EmailStr
   hashed_password : str 
   created_at: str = Field(default=datetime.now())
   

class Retailer(User, table = True):
   __tablename__ = "retailer"
   brand: str
   role : Role =Field(default= Role.RETAILER)
   is_active : bool = False
   had_strike : bool = False
   strike : int = Field(default= 0)


class Costumer(User, table= True):
   __tablename__ = "costumer"
   role : Role =Field(default= Role.COSTUMER)
   is_active : bool = True
   
class Super(User, table= True):
   __tablename__ = "Super"
   role : Role = Field(default= Role.SUPER)