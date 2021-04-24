from typing import List
import datetime as _dt
import pydantic as _pydantic


class _PostBase(_pydantic.BaseModel):
    title: str
    content: str


class PostCreate(_PostBase):
    pass


class Post(_PostBase):
    id: int
    owner_id: int
    date_created: _dt.datetime
    date_last_updated: _dt.datetime

    class Config:
        orm_mode = True


class _UserBase(_pydantic.BaseModel):
    email: str


class UserCreate(_UserBase):
    password: str


class User(_UserBase):
    id: int
    is_active: bool
    posts: List[Post] = []

    class Config:
        orm_mode = True