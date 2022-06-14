import pytest
import pymongo
from fastapi.testclient import TestClient
from app.main import app
from app.routers.connectDB import SETTINGS
from app.models import CreateUser
import datetime
from app.oauth2 import create_access_token
from app.utils import hash_password
"""
For the purpose of settings up or tearing down the databases, there is no need to use Motor
"""
pymongo_client = pymongo.MongoClient(SETTINGS.MONGO_URI)


@pytest.fixture
def test_client():
    with TestClient(app) as client:
        yield client


@pytest.fixture
def clear_collections():
    database = pymongo_client[SETTINGS.DATABASE_NAME]
    collections = ["users", "posts", "votes"]
    for collection in collections:
        try:
            database[collection].delete_many({})
        except Exception:
            pass


@pytest.fixture
def get_users():
    users_data = [{
        "email": "Tevye@gmail.com",
        "username": "TevyeTheMilkman",
        "password": "password123",
        "first_name": "Shalom",
        "last_name": "Aleichem"},
        {
        "email": "jonsnow@gmail.com",
        "username": "KingInTheNorth",
        "password": "password321",
        "first_name": "Jon",
        "last_name": "Snow"}
    ]
    return users_data


@pytest.fixture
def get_posts():
    posts_data = [
        {
            "title": "Pizza is the best",
            "content": "The best food in the world is pizza!"
        },
        {
            "title": "IPAs are the best type of beer!",
            "content": "Despite what some critics think, Hazy IPAs are the pinnacle of beer making!"
        }]
    return posts_data


@pytest.fixture
def login_user1():
    users_collection = pymongo_client[SETTINGS.DATABASE_NAME]['users']
    users_data1 = {
        "email": "Tevye@gmail.com",
        "username": "TevyeTheMilkman",
        "password": "password123",
        "first_name": "Shalom",
        "last_name": "Aleichem"

    }
    user1_data = CreateUser(**users_data1).dict()
    user1_data["created_at"] = datetime.datetime.utcnow()
    user1_data["password"] = hash_password(user1_data["password"])
    users_collection.insert_one(user1_data)
    # Now you must get the _id for that post
    user1_post = users_collection.find_one(
        {"username": user1_data["username"]})
    return create_access_token({"userID": str(user1_post["_id"])})


@pytest.fixture
def login_user2():
    users_collection = pymongo_client[SETTINGS.DATABASE_NAME]['users']
    users_data2 = {
        "email": "jonsnow@gmail.com",
        "username": "KingInTheNorth",
        "password": "password321",
        "first_name": "Jon",
        "last_name": "Snow"

    }
    user2_data = CreateUser(**users_data2).dict()
    user2_data["created_at"] = datetime.datetime.utcnow()
    user2_data["password"] = hash_password(user2_data["password"])
    users_collection.insert_one(user2_data)
   # Now you must get the _id for that post
    user2_post = users_collection.find_one(
        {"username": user2_data["username"]})
    return create_access_token({"userID": str(user2_post["_id"])})
