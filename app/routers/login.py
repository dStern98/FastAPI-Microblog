from http.client import HTTPException
from fastapi import APIRouter, Depends, HTTPException, status
from ..utils import verify_password
from .connectDB import inject_mongo_client
from ..auth import create_access_token
from fastapi.security import OAuth2PasswordRequestForm
from ..models import Token

router = APIRouter(tags=["Authentication"])


@router.post("/login/", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), client=Depends(inject_mongo_client)):
    users_collection = client["MicroBlog"]["users"]
    user = await users_collection.find_one({"username": form_data.username})

    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials.")

    if not verify_password(form_data.password, user["password"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials.")

    access_token = create_access_token({"userID": str(user["_id"])})

    return {"access_token": access_token, "token_type": "bearer"}
