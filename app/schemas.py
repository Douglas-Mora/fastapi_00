from pydantic import BaseModel, EmailStr
from datetime import datetime

class PostBase(BaseModel):
    "This is the schema that defines the post model"
    title: str
    content: str
    published: bool = False

class PostCreate(PostBase):
    pass

class PostResponse(BaseModel): #Cambié PostCreate a BaseModel, no he probado
    "Fields 'title', 'content', and 'published' are inherited from PostBase class above."
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True
        

# ------------- USERS
class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    email: EmailStr
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True