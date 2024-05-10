from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class PostBase(BaseModel):
    "This is the schema that defines the post model"
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass

class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    # owner : UserOut
    
    class Config:
        from_attributes = True
    
    
#class PostOut(BaseModel):
#    Post: Post
#    votes: int

#class PostResponse(PostBase): #Cambié PostCreate a BaseModel, no he probado
#    "Fields 'title', 'content', and 'published' are inherited from PostBase class above."
#    id: int
#    created_at: datetime
       
#    class Config:
#        from_attributes = True
        

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
        

class UserLogin(BaseModel):
    email: EmailStr
    password: str
    
    
class Token(BaseModel):
    access_token: str
    token_type: str
    
    
class TokenData(BaseModel):
    id: Optional[str]=None
    
