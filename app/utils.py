from bson.objectid import ObjectId
from fastapi import HTTPException, status


# verify valid BSON ObjectID
def verify_object_ID(id: str):
    try:
        id = ObjectId(id)
        return id
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"{id} is not a valid ObjectID")
