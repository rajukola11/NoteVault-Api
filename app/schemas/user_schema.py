from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class UserCreate(BaseModel):
    email:str
    password:str
    role:Optional[str]='user'

class UserRead(BaseModel):
    id:int
    email:str
    role:str
    is_active:bool
    created_at:datetime
    
    class Config:
        orm_mode=True
