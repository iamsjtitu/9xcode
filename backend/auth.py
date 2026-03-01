from pydantic import BaseModel
from typing import Optional
import jwt
from datetime import datetime, timedelta
import os
from passlib.context import CryptContext
from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT settings
SECRET_KEY = os.getenv("JWT_SECRET", "your-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1440  # 24 hours

# Default admin credentials
ADMIN_USERNAME = "admin"
DEFAULT_PASSWORD_HASH = pwd_context.hash("admin123")

# Security
security = HTTPBearer()

class LoginRequest(BaseModel):
    username: str
    password: str

class ChangePasswordRequest(BaseModel):
    current_password: str
    new_password: str

class Token(BaseModel):
    access_token: str
    token_type: str

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str) -> Optional[dict]:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Dependency to get current authenticated user"""
    token = credentials.credentials
    payload = verify_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return payload

async def get_admin_password_hash(db):
    """Get admin password hash from database or return default"""
    admin_doc = await db.admin_settings.find_one({"type": "credentials"})
    if admin_doc and admin_doc.get("password_hash"):
        return admin_doc["password_hash"]
    return DEFAULT_PASSWORD_HASH

async def update_admin_password(db, new_password_hash: str):
    """Update admin password in database"""
    await db.admin_settings.update_one(
        {"type": "credentials"},
        {"$set": {"password_hash": new_password_hash, "updated_at": datetime.utcnow()}},
        upsert=True
    )
