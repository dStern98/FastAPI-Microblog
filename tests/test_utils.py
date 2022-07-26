from pydantic import BaseModel
from typing import Optional
from app.utils import build_mongo_URI

"""
Test the function that builds the MongoURI. One for an atlas URI, one for a local URI
"""

atlas_kwargs = {
    "mongodb_host": "someurl",
    "mongodb_driver": "mongodb+srv",
    "mongodb_user": "someuser",
    "mongodb_password": "somepassword",
    "mongodb_database": "somedatabase",
    "mongodb_params": {"retryWrites": "true", "w": "majority"},
    "mongodb_useAtlas": True
}

local_kwargs = {
    "mongodb_host": "localhost",
    "mongodb_driver": "mongodb",
    "mongodb_user": "david",
    "mongodb_password": "somepassword",
    "mongodb_database": "somedatabase",
    "mongodb_params": {"serverSelectionTimeoutMS": "2000"},
    "mongodb_port": 27017,
    "mongodb_useAtlas": False
}

localURI = f"mongodb://david:somepassword@localhost:27017/?serverSelectionTimeoutMS=2000"
atlasMongoURI = f'mongodb+srv://someuser:somepassword@someurl/somedatabase?retryWrites=true&w=majority'


class FakeSettings(BaseModel):
    # Mongo settings
    mongodb_host: str
    mongodb_port: Optional[int] = None
    mongodb_user: str
    mongodb_password: str
    mongodb_database: Optional[str] = None
    mongodb_driver: str
    mongodb_params: Optional[dict] = None
    mongodb_useAtlas: bool


def test_local_URI():
    assert build_mongo_URI(FakeSettings(**local_kwargs)) == localURI


def test_atlas_URI():
    assert build_mongo_URI(FakeSettings(**atlas_kwargs)) == atlasMongoURI
