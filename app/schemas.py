from pydantic import BaseModel, ConfigDict, EmailStr
from datetime import datetime

class PostBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    title: str
    content: str
    published: bool | None = True

    
class PostCreate(PostBase):
    pass

class PostResponse(PostBase):
    id: int
    created_at: datetime


class UserBase(BaseModel):
    email: EmailStr
    

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    created_at: datetime

class UserLogin(UserCreate):
    pass
