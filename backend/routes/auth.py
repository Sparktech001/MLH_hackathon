from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from backend.services.auth import create_user, authenticate_user, create_access_token
from pydantic import BaseModel

router = APIRouter(prefix="/auth", tags=["auth"])

class UserCreate(BaseModel):
    email: str
    password: str

@router.post("/register")
async def register(user: UserCreate):
    success = create_user(user.email, user.password)
    if not success:
        raise HTTPException(status_code=400, detail="Email already registered")
    return {"message": "User registered successfully"}

@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    OAuth2 compatible token login, gets username (email) and password from form data.
    """
    if authenticate_user(form_data.username, form_data.password):
        access_token = create_access_token(data={"sub": form_data.username})
        return {"access_token": access_token, "token_type": "bearer"}
        
    raise HTTPException(status_code=400, detail="Incorrect email or password")

from backend.services.auth import get_current_user, get_user_profile, update_welcome_seen, add_user_xp

@router.get("/profile")
async def get_profile(current_user: str = Depends(get_current_user)):
    return get_user_profile(current_user)

@router.post("/welcome-seen")
async def welcome_seen(current_user: str = Depends(get_current_user)):
    update_welcome_seen(current_user)
    return {"message": "Welcome seen updated"}

class XPUpdate(BaseModel):
    xp_amount: int

@router.post("/add-xp")
async def add_xp(xp_update: XPUpdate, current_user: str = Depends(get_current_user)):
    new_xp = add_user_xp(current_user, xp_update.xp_amount)
    return {"xp": new_xp}
