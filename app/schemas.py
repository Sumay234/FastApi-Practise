from pydantic import BaseModel
from  . import models


class PostBase(BaseModel):
    title  : str
    content : str
    published : bool = True

class PostCreate(PostBase):
    pass

class PostResponse(BaseModel):
    pass

class Post(BaseModel):
    id = int
    title: str
    content: str
    published: bool

    class Config:
        orm_mode = True
