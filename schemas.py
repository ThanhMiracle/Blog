from pydantic import BaseModel
from typing import List
class BlogBase(BaseModel):
    title: str
    body: str
    # class Config():
    #     from_attributes = True

class Blog(BlogBase):
    class Config():
        from_attributes = True

class User(BaseModel):
    name: str
    email:str
    password: str

class ShowUser(BaseModel):
    ID: int
    name: str
    email: str
    blog: List[Blog] = []
    class Config():
        from_attributes = True

class ShowCreator(BaseModel):
    name: str
    email: str
    class Config():
        from_attributes = True
class ShowBlog(BaseModel):
    ID: int
    title: str
    body: str
    creator : ShowCreator
    class Config():
        from_attributes = True
