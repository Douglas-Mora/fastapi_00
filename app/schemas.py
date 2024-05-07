from pydantic import BaseModel

class Post(BaseModel):
    "This is the schema that defines the post model"
    title: str
    content: str
    published: bool = False

class PostCreate(BaseModel):
    pass


