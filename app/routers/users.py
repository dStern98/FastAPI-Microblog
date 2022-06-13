from fastapi import APIRouter, HTTPException, status, Depends
from ..models import CreateUser, UpdateUser, ReadUsers
from .connectDB import inject_mongo_client, SETTINGS
import datetime
from ..utils import verify_object_ID, hash_password
from typing import Optional
from ..oauth2 import get_current_user

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(new_user: CreateUser, client=Depends(inject_mongo_client)):
    users_collection = client[SETTINGS.DATABASE_NAME]["users"]

    # First, check if someone already has taken the submitted username
    username_already_exists = await users_collection.find_one({"username": new_user.username})

    if username_already_exists:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"The requested username {new_user.username} already exists.")

    new_user.password = hash_password(new_user.password)
    new_user = new_user.dict()
    new_user["created_at"] = datetime.datetime.utcnow()
    await users_collection.insert_one(new_user)
    return {
        "Message": "Successfully created new user",
        "email": new_user["email"],
        "Name": f"{new_user['first_name']} {new_user['last_name']}",
        "username": new_user["username"]
    }


@router.delete("/")
async def delete_user(current_user=Depends(get_current_user), client=Depends(inject_mongo_client)):
    users_collection = client[SETTINGS.DATABASE_NAME]["users"]
    object_id = verify_object_ID(current_user.userID)
    user = await users_collection.delete_one({"_id": object_id})
    return {"Message": f"Successfully deleted document with UserID {current_user.userID}"}


@router.patch("/")
async def update_user(updated_user: UpdateUser, current_user=Depends(get_current_user), client=Depends(inject_mongo_client)):
    users_collection = client[SETTINGS.DATABASE_NAME]["users"]
    object_id = verify_object_ID(current_user.userID)

    updated_user_dict = {key: value for key,
                         value in updated_user.dict().items() if value}

    updated_user = await users_collection.find_one_and_update({"_id": object_id}, {"$set": updated_user_dict})

    if not updated_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No User with given userID.")

    return {"Message": "Successfully updated the document."}


@router.get("/search/", response_model=ReadUsers)
async def search_users(username_search: Optional[str] = None, skip: Optional[int] = 0, length: Optional[int] = 25,
                       client=Depends(inject_mongo_client)):
    users_collection = client[SETTINGS.DATABASE_NAME]["users"]
    query_dictionary = {}
    if username_search:
        query_dictionary["username"] = {
            "$regex": f"[a-z0-9]*{username_search}[a-z0-9]*", "$options": "i"}

    users = await users_collection.find(query_dictionary).skip(skip).to_list(length=length)
    for user in users:
        user["userID"] = str(user["_id"])
    return {"Users": users}


@router.get("/", response_model=ReadUsers)
async def get_user(current_user=Depends(get_current_user)):
    return {"Users": current_user.dict()}
