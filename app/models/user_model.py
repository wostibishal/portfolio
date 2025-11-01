from sqlmodel import Field, SQLModel
from uuid import  uuid4, UUID

class User(SQLModel, table=True):
   __tablename__ = "users"
   id : UUID = Field(default_factory=uuid4, primary_key=True, index=True)
   first_name : str
   last_name : str
   email : str
   is_active : bool = True
   hashed_password : str   
