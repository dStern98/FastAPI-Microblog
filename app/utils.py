from bson.objectid import ObjectId
from fastapi import HTTPException, status
from passlib.context import CryptContext


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
