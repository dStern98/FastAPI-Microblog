from pydantic import BaseModel, BaseSettings, EmailStr, constr
from os import path
import datetime
from typing import Optional, Union, List
from enum import Enum

ENV_PATH = path.join(path.dirname(__file__), "..", ".env")


class Settings(BaseSettings):
    MONGO_URI: str
    SECRET: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    DATABASE_NAME: str

    class Config:
        env_file = ENV_PATH


"""
Pydantic Models for Creating, Updating, Reading Users
"""


class CreateUser(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    username: constr(min_length=5, max_length=50)
    password: constr(min_length=5, max_length=50)


class UpdateUser(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[constr(min_length=5, max_length=50)] = None
    password: Optional[constr(min_length=5, max_length=50)] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None


class ReadUser(BaseModel):
    userID: str
    first_name: str
    last_name: str
    email: EmailStr
    username: constr(min_length=5, max_length=50)
    created_at: datetime.datetime


class ReadUsers(BaseModel):
    Users: Union[ReadUser, List[ReadUser]]


"""
Pydantic Models for CRUD on Posts
"""


class CreatePost(BaseModel):
    title: constr(max_length=50)
    content: constr(max_length=250)


class PostDB(CreatePost):
    created_at: datetime.datetime
    updated_at: Optional[datetime.datetime] = None
    userID: str
    likes: int = 0
    dislikes: int = 0


class UpdatePostDB(BaseModel):
    title: Optional[constr(max_length=50)] = None
    content: Optional[constr(max_length=250)] = None


"""
Create a Likes/Dislikes Collection
"""


class LikeType(str, Enum):
    like = "like"
    dislike = "dislike"


class Action(BaseModel):
    action: LikeType


class LikeDislike(BaseModel):
    userID: str
    postID: str
    action: LikeType


"""
Auth related Models
"""


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    userID: str
