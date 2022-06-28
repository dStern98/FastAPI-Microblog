from fastapi import HTTPException, status
from ..utils import verify_object_ID
from ..models import LikeDislike
from typing import Dict
import asyncio


class VotingLogic:
    def __init__(self, posts_collection, votes_collection, postID: str, userID: str, action: str):
        self.posts_collection = posts_collection
        self.votes_collection = votes_collection
        self.postID = postID
        self.userID = userID
        self.action = action
        self.action_map = {"like": "likes", "dislike": "dislikes"}

    async def __verify_post(self):
        # Check if the post exists
        post_object_id = verify_object_ID(self.postID)
        self.post_object_id = post_object_id
        post_to_like: dict = await self.posts_collection.find_one({"_id": post_object_id})
        if not post_to_like:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="No such document.")
        self.post_to_like = post_to_like

    async def __check_post_vote_status(self):
        # check if the person has already liked the page
        try:
            already_voted: dict = await self.votes_collection.find_one({"userID": self.userID, "postID": self.postID})
            self.already_voted = already_voted.get("action")
        except Exception:
            self.already_voted = None

    async def __action(self):
        if self.already_voted == self.action:
            await asyncio.gather(
                self.votes_collection.delete_one(
                    {"userID": self.userID, "postID": self.postID, "action": self.already_voted}),
                self.posts_collection.update_one({"_id": self.post_object_id},
                                                 {"$set": {self.action_map[self.action]:
                                                           self.post_to_like[self.action_map[self.action]] - 1}})
            )

        elif self.already_voted != self.action and self.already_voted is not None:
            await asyncio.gather(
                self.votes_collection.update_one({"userID": self.userID,
                                                  "postID": self.postID}, {"$set": {"action": self.action}}),
                self.posts_collection.update_one({"_id": self.post_object_id},
                                                 {"$set": {self.action_map[self.action]:
                                                           self.post_to_like[self.action_map[self.action]] + 1,
                                                           self.action_map[self.already_voted]:
                                                           self.post_to_like[self.action_map[self.already_voted]] - 1}})
            )
        else:
            new_vote_entry = {"userID": self.userID,
                              "postID": self.postID, "action": self.action}
            await asyncio.gather(
                self.votes_collection.insert_one(
                    LikeDislike(**new_vote_entry).dict()),
                self.posts_collection.update_one({"_id": self.post_object_id},
                                                 {"$set": {self.action_map[self.action]:
                                                           self.post_to_like[self.action_map[self.action]] + 1}})

            )

    async def ApplyVotingLogic(self) -> Dict:
        await self.__verify_post()
        await self.__check_post_vote_status()
        await self.__action()
        return {"Message": "Successfully voted."}
