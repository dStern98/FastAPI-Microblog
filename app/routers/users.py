from fastapi import APIRouter, HTTPException, status, Depends
from ..models import CreateUser, UpdateUser, ReadUsers
from .connectDB import inject_mongo_client
import datetime
from ..utils import verify_object_ID
from typing import Optional


router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(new_user: CreateUser, client=Depends(inject_mongo_client)):
    users_collection = client["MicroBlog"]["users"]
    new_user = new_user.dict()
    new_user["created_at"] = datetime.datetime.utcnow()
    await users_collection.insert_one(new_user)
    return {
        "Message": "Successfully created new user",
        "email": new_user["email"],
        "Name": f"{new_user['first_name']} {new_user['last_name']}"
    }


@router.delete("/{userID}")
async def delete_user(userID: str, client=Depends(inject_mongo_client)):
    users_collection = client["MicroBlog"]["users"]
    object_id = verify_object_ID(userID)

    user = await users_collection.find_one_and_delete({"_id": object_id})

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No User with given userID.")

    return {"Message": f"Successfully deleted document with UserID {userID}"}


@router.patch("/{userID}")
async def update_user(userID: str, updated_user: UpdateUser, client=Depends(inject_mongo_client)):
    users_collection = client["MicroBlog"]["users"]
    object_id = verify_object_ID(userID)

    updated_user_dict = {key: value for key,
                         value in updated_user.dict().items() if value}

    updated_user = await users_collection.find_one_and_update({"_id": object_id}, {"$set": updated_user_dict})

    if not updated_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No User with given userID.")

    return {"Message": "Successfully updated the document."}


@router.get("/", response_model=ReadUsers)
async def search_users(username_search: Optional[str] = None, skip: Optional[int] = 0, client=Depends(inject_mongo_client)):
    users_collection = client["MicroBlog"]["users"]
    query_dictionary = {}
    if username_search:
        query_dictionary["username"] = {
            "$regex": f"[A-Za-z]*{username_search}[A-Za-z]*", "$options": "i"}

    users = await users_collection.find(query_dictionary).skip(skip).to_list(length=100)
    for user in users:
        user["id"] = str(user["_id"])
    return {"Users": users}


@router.get("/{userID}", response_model=ReadUsers)
async def get_user(userID: str, client=Depends(inject_mongo_client)):
    users_collection = client["MicroBlog"]["users"]
    object_id = verify_object_ID(userID)

    user = await users_collection.find_one({"_id": object_id})

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No User with given userID.")

    user["id"] = str(user["_id"])
    return {"Users": user}
