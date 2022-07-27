from ..models import Settings
import motor.motor_asyncio
from fastapi import APIRouter, HTTPException, status
from ..utils import mongoURI

settings = Settings()
router = APIRouter()

mongoClient = {"mongo_client": None}


# On Startup, Connect to the Database
@router.on_event("startup")
async def connect_DB():
    mongoClient["mongo_client"] = motor.motor_asyncio.AsyncIOMotorClient(
        mongoURI)
    print("Connected to DB...")


async def inject_mongo_client():
    if not mongoClient["mongo_client"]:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Startup script failed to run.")
    return mongoClient["mongo_client"]


@router.get("/")
def health_check():
    return {"Message": "Hello World!!!!!"}
