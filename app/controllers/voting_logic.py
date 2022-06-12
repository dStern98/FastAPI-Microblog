from fastapi import HTTPException, status
from ..utils import verify_object_ID
from ..models import LikeDislike
from typing import Dict


class VotingLogic:
    def __init__(self, posts_collection, votes_collection, postID: str, userID: str, action: str):
        self.posts_collection = posts_collection
        self.votes_collection = votes_collection
        self.postID = postID
        self.userID = userID
        self.action = action

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
            already_voted: dict = await self.votes_collection.find_one({"userID": "fakeUserID", "postID": self.postID})
            self.already_voted = already_voted.get("action")
        except Exception:
            self.already_voted = None

    async def __action_like(self):
        # If they have already liked the page, then unlike the page
        if self.already_voted == "like":
            await self.votes_collection.delete_one({"userID": "fakeUserID", "postID": self.postID, "action": "like"})
            await self.posts_collection.update_one({"_id": self.post_object_id},
                                                   {"$set": {"likes": self.post_to_like["likes"] - 1}})
        elif self.already_voted == "dislike":
            await self.votes_collection.update_one({"userID": "fakeUserID",
                                                    "postID": self.postID}, {"$set": {"action": "like"}})
            await self.posts_collection.update_one({"_id": self.post_object_id},
                                                   {"$set": {"likes": self.post_to_like["likes"] + 1,
                                                             "dislikes": self.post_to_like["dislikes"] - 1}})
        else:
            new_vote_entry = {"userID": "fakeUserID",
                              "postID": self.postID, "action": "like"}
            await self.votes_collection.insert_one(LikeDislike(**new_vote_entry).dict())
            await self.posts_collection.update_one({"_id": self.post_object_id},
                                                   {"$set": {"likes": self.post_to_like["likes"] + 1}})

        return {"Message": "Successfully liked"}

    async def __action_dislike(self):
        if self.already_voted == "dislike":
            await self.votes_collection.delete_one({"userID": "fakeUserID", "postID": self.postID, "action": "dislike"})
            await self.posts_collection.update_one({"_id": self.post_object_id},
                                                   {"$set": {"dislikes": self.post_to_like["dislikes"] - 1}})
        elif self.already_voted == "like":
            await self.votes_collection.update_one({"userID": "fakeUserID",
                                                    "postID": self.postID}, {"$set": {"action": "dislike"}})
            await self.posts_collection.update_one({"_id": self.post_object_id},
                                                   {"$set": {"likes": self.post_to_like["likes"] - 1,
                                                             "dislikes": self.post_to_like["dislikes"] + 1}})
        else:
            new_vote_entry = {"userID": "fakeUserID",
                              "postID": self.postID, "action": "dislike"}
            await self.votes_collection.insert_one(LikeDislike(**new_vote_entry).dict())
            await self.posts_collection.update_one({"_id": self.post_object_id},
                                                   {"$set": {"dislikes": self.post_to_like["dislikes"] + 1}})

        return {"Message": "Successfully disliked"}

    async def ApplyVotingLogic(self) -> Dict:
        await self.__verify_post()
        await self.__check_post_vote_status()
        if self.action == "like":
            response = await self.__action_like()
        else:
            response = await self.__action_dislike()

        return response
