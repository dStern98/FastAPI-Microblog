from fastapi import APIRouter, Depends
from .connectDB import inject_mongo_client, SETTINGS
from ..models import Action
from ..controllers.voting_logic import VotingLogic
from ..oauth2 import get_current_user


router = APIRouter(prefix="/vote", tags=["Vote"])


@router.post("/")
async def like_post(postID: str, action_type: Action, current_user=Depends(get_current_user), client=Depends(inject_mongo_client)):
    posts_collection = client[SETTINGS.DATABASE_NAME]["posts"]
    votes_collection = client[SETTINGS.DATABASE_NAME]["votes"]

    # Refactored the Voting Logic into it own file
    response = await VotingLogic(votes_collection=votes_collection, posts_collection=posts_collection,
                                 postID=postID, action=action_type.action, userID=current_user.userID).ApplyVotingLogic()

    return response
