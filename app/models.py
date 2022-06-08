from pydantic import BaseModel, BaseSettings, EmailStr, constr
from os import path
import datetime
from typing import Optional, Union, List


ENV_PATH = path.join(path.dirname(__file__), "..", ".env")


class Settings(BaseSettings):
    MONGO_URI: str

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
    id: str
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


class PostDB(BaseModel):
    title: constr(max_length=50)
    content: constr(max_length=250)
    created: datetime.datetime
    updated: Optional[datetime.datetime] = None
    userID: str
    likes: int = 0
    dislikes: int = 0


class UpdatePostDB(BaseModel):
    title: Optional[constr(max_length=50)] = None
    content: Optional[constr(max_length=250)] = None
