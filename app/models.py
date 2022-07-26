from pydantic import BaseModel, BaseSettings, EmailStr, constr
from os import path
import datetime
from typing import Optional, Union, List
from enum import Enum

ENV_PATH = path.join(path.dirname(__file__), "..", ".env")
UVICORN_PREFIX = "uvicorn_"


class Settings(BaseSettings):

    # Mongo settings
    mongodb_host: str
    mongodb_port: Optional[int] = None
    mongodb_user: str
    mongodb_password: str
    mongodb_database: Optional[str] = None
    mongodb_driver: str
    mongodb_params: Optional[dict] = None
    mongodb_useAtlas: bool

    # Uvicorn settings
    uvicorn_host: str
    uvicorn_port: int
    uvicorn_reload: bool

    # Auth Related
    auth_secret_key: str
    auth_algorithm: str
    auth_token_expiration_minutes: int

    class Config:
        env_file = ENV_PATH

    # Access all of the Uvicorn .env vars
    def get_uvicorn_settings(self) -> dict:
        return {attr.replace(UVICORN_PREFIX, ''): getattr(self, attr)
                for attr in dir(self) if attr.startswith(UVICORN_PREFIX)}


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
The below two models would be used when the front-end needs to know
if a logged in user has liked/disliked a set of posts in their feed
"""


class postGetAction(BaseModel):
    postIDs: List[str]


"""
Auth related Models
"""


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    userID: str
