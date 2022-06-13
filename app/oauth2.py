from fastapi.security import OAuth2PasswordBearer
from fastapi import HTTPException, status, Depends
from .routers.connectDB import SETTINGS, inject_mongo_client
import datetime
from jose import JWTError, jwt
from .models import TokenData, ReadUser
from .utils import verify_object_ID


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY = SETTINGS.SECRET
ALGORITHM = SETTINGS.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = SETTINGS.ACCESS_TOKEN_EXPIRE_MINUTES

"""
Create JWT Tokens, Verify JWT Tokens, get_current_user to be used for all guarded routes
"""


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.datetime.utcnow(
    ) + datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        userID: str = payload.get("userID")
        return TokenData(userID=userID)

    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid credentials.", headers={"WWW-Authenticate": "Bearer"})


async def get_current_user(token: str = Depends(oauth2_scheme), client=Depends(inject_mongo_client)):
    users_collection = client[SETTINGS.DATABASE_NAME]["users"]

    token_model = verify_access_token(token)
    try:
        token_id = verify_object_ID(token_model.userID)
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid credentials.", headers={"WWW-Authenticate": "Bearer"})
    current_user = await users_collection.find_one({"_id": token_id})
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials.")
    current_user = {key: value for key,
                    value in current_user.items() if key != "_id"}
    current_user["userID"] = str(token_id)
    return ReadUser(**current_user)
