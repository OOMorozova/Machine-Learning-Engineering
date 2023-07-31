import datetime
from typing import Optional

from pydantic import BaseModel, Field


class UserGet(BaseModel):
    id: int
    age: int
    city: str
    country: str
    exp_group: int
    gender: int
    os: str
    source: str

    class Config:
        orm_mode = True


class PostGet(BaseModel):
    id: int
    text: str
    topic: str

    class Config:
        orm_mode = True


class FeedGet(BaseModel):
    post_id: int
    post: PostGet
    action: str
    user_id: int
    user: UserGet
    time: datetime.datetime

    class Config:
        orm_mode = True
