from fastapi import APIRouter, Depends, HTTPException
from app.utils.database import db
from app.models import User
from app.utils.jwt import verify_access_token
from app.routes.auth import get_current_user

router = APIRouter()

@router.get("/profile")
async def get_user_profile(current_user: dict = Depends(get_current_user)):
    return {"user_id": current_user["user_id"], "user_name": current_user["user_name"], "email": current_user["user_email"]}

@router.get("/user/{user_email}")
async def get_user(user_email: str, current_user: User = Depends(get_current_user)):
    user = await User.find_one({"user_email": user_email})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.get("/")
async def get_users(token: str = Depends(verify_access_token)):
    if not token:
        return {"message": "Unauthorized"}
    users = list(db["users"].find({}, {"_id": 0, "password": 0}))
    return {"users": users}
