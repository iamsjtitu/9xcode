from fastapi import APIRouter, HTTPException, Depends, Header
from auth import LoginRequest, Token, authenticate_user, create_access_token, verify_token
from datetime import timedelta

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login", response_model=Token)
async def login(credentials: LoginRequest):
    """Admin login endpoint"""
    if not authenticate_user(credentials.username, credentials.password):
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password"
        )
    
    access_token = create_access_token(
        data={"sub": credentials.username},
        expires_delta=timedelta(minutes=1440)
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/verify")
async def verify(authorization: str = Header(None)):
    """Verify authentication token"""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authorization header")
    
    token = authorization.split(" ")[1]
    payload = verify_token(token)
    
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    
    return {"valid": True, "username": payload.get("sub")}

def get_current_user(authorization: str = Header(None)):
    """Dependency to check if user is authenticated"""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    token = authorization.split(" ")[1]
    payload = verify_token(token)
    
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    
    return payload.get("sub")