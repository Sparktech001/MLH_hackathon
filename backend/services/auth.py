import jwt
from datetime import datetime, timedelta, timezone
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import bcrypt
from backend.services.supabase_client import supabase

SECRET_KEY = "super-secret-hackathon-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 # 1 day

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def get_password_hash(password: str) -> str:
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

def create_user(email: str, password: str) -> bool:
    # Check if exists
    res = supabase.table("users").select("email").eq("email", email).execute()
    if res.data and len(res.data) > 0:
        return False
        
    try:
        supabase.table("users").insert({
            "email": email, 
            "hashed_password": get_password_hash(password)
        }).execute()
        return True
    except Exception as e:
        print(f"Auth error: {e}")
        return False

def authenticate_user(email: str, password: str) -> bool:
    res = supabase.table("users").select("hashed_password").eq("email", email).execute()
    if res.data and len(res.data) > 0:
        hashed = res.data[0].get("hashed_password")
        if verify_password(password, hashed):
            return True
    return False

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(token: str = Depends(oauth2_scheme)) -> str:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        return email
    except jwt.PyJWTError:
        raise credentials_exception
