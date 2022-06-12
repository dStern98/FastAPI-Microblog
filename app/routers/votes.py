from fastapi import APIRouter, Depends
from .connectDB import inject_mongo_client
from ..models import Action
from ..controllers.voting_logic import VotingLogic
from ..auth import get_current_user


router = APIRouter(prefix="/vote", tags=["Vote"])


@router.post("/")
async def like_post(postID: str, action_type: Action, current_user=Depends(get_current_user), client=Depends(inject_mongo_client)):
    posts_collection = client["MicroBlog"]["posts"]
    votes_collection = client["MicroBlog"]["votes"]

    # Refactored the Voting Logic into it own file, as it became lengthy
    response = await VotingLogic(votes_collection=votes_collection, posts_collection=posts_collection,
                                 postID=postID, action=action_type.action, userID=current_user.userID).ApplyVotingLogic()

    return response
