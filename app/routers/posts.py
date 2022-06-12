from fastapi import APIRouter, HTTPException, status, Depends
from ..models import CreatePost, PostDB, UpdatePostDB
from .connectDB import inject_mongo_client
import datetime
from ..utils import verify_object_ID
from typing import Optional
from ..oauth2 import get_current_user
import pymongo

router = APIRouter(prefix="/posts", tags=["Posts"])


@router.post("/", status_code=status.HTTP_201_CREATED)
async def post_post(post: CreatePost, current_user=Depends(get_current_user), client=Depends(inject_mongo_client)):
    posts_collection = client["MicroBlog"]["posts"]
    post_dict = post.dict()

    post_dict["created_at"] = datetime.datetime.utcnow()
    post_dict["userID"] = current_user.userID

    # Gurantee the integrity of the posted document by passing it to Pydantic
    post_dict = PostDB(**post_dict)

    await posts_collection.insert_one(post_dict.dict())
    return {"Message": "Successfully inserted the document."}


@router.get('/all/')
async def get_all_posts(client=Depends(inject_mongo_client)):
    posts_collection = client["MicroBlog"]["posts"]
    all_posts = await posts_collection.find({}).to_list(length=100)
    for post in all_posts:
        post["postID"] = str(post["_id"])
        del post["_id"]
    return all_posts


@router.delete("/{postID}/")
async def delete_post(postID: str, current_user=Depends(get_current_user), client=Depends(inject_mongo_client)):
    posts_collection = client["MicroBlog"]["posts"]
    postID_BSON = verify_object_ID(postID)

    # First, you must check if the user owns the associated post, otherwise reject request
    post_to_be_deleted = await posts_collection.find_one({"_id": postID_BSON})

    if not post_to_be_deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No such document.")
    if post_to_be_deleted["userID"] != current_user.userID:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"You cannot delete someone else's post.")

    # If they own the post, then delete it
    delete_response = await posts_collection.find_one_and_delete({"_id": postID_BSON})

    delete_response["postID"] = str(delete_response["_id"])
    del delete_response["_id"]
    return {"Message": "Successfully deleted the following document.",
            "Document": delete_response}


@router.patch("/{postID}/")
async def update_post(postID: str, update_to_post: UpdatePostDB, current_user=Depends(get_current_user), client=Depends(inject_mongo_client)):
    posts_collection = client["MicroBlog"]["posts"]
    postID_BSON = verify_object_ID(postID)

    # Pydantic will default any missing keys to a value of None, parse those out
    update_to_post = {key: value for key,
                      value in update_to_post.dict().items() if value}
    update_to_post["updated_at"] = datetime.datetime.utcnow()

    # Check first if the user owns the associated post
    post_to_be_updated = await posts_collection.find_one({"_id": postID_BSON})

    if not post_to_be_updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No such document.")
    if post_to_be_updated["userID"] != current_user.userID:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"You cannot delete someone else's post.")

    # If they do own the post, then delete the document
    old_post_before_update = await posts_collection.find_one_and_update({"_id": postID_BSON}, {"$set": update_to_post})

    old_post_before_update["postID"] = str(old_post_before_update["_id"])
    del old_post_before_update["_id"]

    return {"Message": "Successfully updated the following document.",
            "Document": old_post_before_update}


# Build the Actual Search Endpoint for Front-end
@router.get("/")
async def get_some_posts(title: Optional[str] = None, userID: Optional[str] = None,
                         skip: Optional[int] = 0, client=Depends(inject_mongo_client)):
    posts_collection = client["MicroBlog"]["posts"]
    query_dictionary = {}

    if title:
        query_dictionary["title"] = {
            "$regex": f"[a-z0-9]*{title}[a-z0-9]*", "$options": "i"}
    if userID:
        query_dictionary["userID"] = userID

    queried_posts = await posts_collection.find(query_dictionary).skip(skip).sort(
        "created", pymongo.DESCENDING).to_list(length=100)

    for post in queried_posts:
        post["postID"] = str(post["_id"])
        del post["_id"]
    return {"Posts": queried_posts}
