from pydantic import BaseModel
from datetime import datetime
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class CreatePost(PostBase):
    pass

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    created_at: datetime

class Config:
    orm_mode = True
