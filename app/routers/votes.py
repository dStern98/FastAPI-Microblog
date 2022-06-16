from fastapi import APIRouter, Depends
from .connectDB import inject_mongo_client, SETTINGS
from ..models import Action, postGetAction
from ..controllers.voting_logic import VotingLogic
from ..oauth2 import get_current_user
from typing import Optional

router = APIRouter(prefix="/vote", tags=["Vote"])
"""
The "/" endpoint allows you to like/dislike a post
The "/userVotes" endpoint allows an authenticated user to get their liked/disliked posts
The "/postVotes" endpoint allows anyone to access the likes/dislikes users list for a post
"""


@router.post("/")
async def like_post(postID: str, action_type: Action, current_user=Depends(get_current_user), client=Depends(inject_mongo_client)):
    posts_collection = client[SETTINGS.DATABASE_NAME]["posts"]
    votes_collection = client[SETTINGS.DATABASE_NAME]["votes"]

    # Refactored the Voting Logic into it own file
    response = await VotingLogic(votes_collection=votes_collection, posts_collection=posts_collection,
                                 postID=postID, action=action_type.action, userID=current_user.userID).ApplyVotingLogic()

    return response


@router.post("/userVotes/")
async def check_if_user_voted(list_of_posts: postGetAction, current_user=Depends(get_current_user),
                              client=Depends(inject_mongo_client)):
    votes_collection = client[SETTINGS.DATABASE_NAME]["votes"]
    user_vote_actions = await votes_collection.find({"userID": current_user.userID,
                                                    "postID": {"$in": list_of_posts.dict()["postIDs"]}}).to_list(length=100)
    for document in user_vote_actions:
        del document["_id"]
    return {"User_Votes": user_vote_actions}


@router.post("/postVotes/")
async def find_post_votes(postID: str, skip: Optional[int] = 0, client=Depends(inject_mongo_client)):
    votes_collection = client[SETTINGS.DATABASE_NAME]["votes"]
    post_votes = await votes_collection.find({"postID": postID}).skip(skip).to_list(length=100)
    for document in post_votes:
        del document["_id"]
    return {"Post_Votes": post_votes}
