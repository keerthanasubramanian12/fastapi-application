from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from app.utils.hashing import hash_password, verify_password
from app.utils.jwt import create_access_token, create_refresh_token, verify_access_token
from app.utils.database import db
from datetime import datetime
from uuid import uuid4
from app.utils.jwt import verify_access_token
from app.models import User 

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

@router.post("/register")
async def register_user(user_name: str, user_email: str, mobile_number: str, password: str):
    if db["users"].find_one({"user_email": user_email}):
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = hash_password(password)
    user = {
        "user_id": str(uuid4()),
        "user_name": user_name,
        "user_email": user_email,
        "mobile_number": mobile_number,
        "password": hashed_password,
        "created_on": datetime.utcnow(),
        "last_update": datetime.utcnow(),
    }
    db["users"].insert_one(user)
    return {"message": "User registered successfully"}

@router.post("/login")
async def login(user_email: str = None, mobile_number: str = None, password: str = None):
    if user_email:
        user = db["users"].find_one({"user_email": user_email})
    elif mobile_number:
        user = db["users"].find_one({"mobile_number": mobile_number})
    else:
        raise HTTPException(status_code=400, detail="Email or Mobile Number is required")
    
    if not user or not verify_password(password, user["password"]):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    
    access_token = create_access_token({"user_id": user["user_id"]})
    refresh_token = create_refresh_token({"user_id": user["user_id"]})
    return {"access_token": access_token, "refresh_token": refresh_token}

@router.post("/logout")
async def logout(token: str = Depends(oauth2_scheme)):
    return {"message": "Logged out successfully"}

def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    payload = verify_access_token(token)
    if not payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")
    
    user_id = payload.get("user_id")
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    
    user = db["users"].find_one({"user_id": user_id})
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    
    return user
