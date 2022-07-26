from bson.objectid import ObjectId
from fastapi import HTTPException, status
from passlib.context import CryptContext
from .models import Settings

# verify valid BSON ObjectID


def verify_object_ID(id: str) -> ObjectId:
    try:
        return ObjectId(id)
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"{id} is not a valid ObjectID")


"""
Authentication related Utils
"""

# Create the Passlib Context for Hashing and Verifying Passwords
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


def hash_password(password: str):
    return pwd_context.hash(password)


# Write a function to build a correct MongoURI from the env vars

def build_mongo_URI(pydantic_settings: Settings) -> str:
    URI = f"{pydantic_settings.mongodb_driver}://{pydantic_settings.mongodb_user}:{pydantic_settings.mongodb_password}@{pydantic_settings.mongodb_host}"
    if pydantic_settings.mongodb_port:
        URI = f"{URI}:{pydantic_settings.mongodb_port}"
    if pydantic_settings.mongodb_database and pydantic_settings.mongodb_useAtlas:
        URI = f"{URI}/{pydantic_settings.mongodb_database}"
    else:
        URI = f"{URI}/"
    if pydantic_settings.mongodb_params:
        query_params_string = "?"
        for key, value in pydantic_settings.mongodb_params.items():
            query_params_string = f"{query_params_string}{key}={value}&"
        URI = f"{URI}{query_params_string.rstrip('&')}"
    return URI


mongoURI = build_mongo_URI(Settings())
