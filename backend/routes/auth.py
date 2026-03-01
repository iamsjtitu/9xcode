from fastapi import APIRouter, HTTPException, Depends, Header
from auth import (
    LoginRequest, Token, ChangePasswordRequest, 
    create_access_token, verify_token, verify_password, 
    hash_password, get_admin_password_hash, update_admin_password,
    get_current_user, ADMIN_USERNAME
)
from database import get_db
from datetime import timedelta

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login", response_model=Token)
async def login(credentials: LoginRequest):
    """Admin login endpoint"""
    db = await get_db()
    
    # Get password hash from database
    stored_hash = await get_admin_password_hash(db)
    
    # Verify credentials
    if credentials.username != ADMIN_USERNAME or not verify_password(credentials.password, stored_hash):
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password"
        )
    
    access_token = create_access_token(
        data={"sub": credentials.username},
        expires_delta=timedelta(minutes=1440)
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/change-password")
async def change_password(
    request: ChangePasswordRequest,
    current_user: dict = Depends(get_current_user)
):
    """Change admin password"""
    db = await get_db()
    
    # Get current password hash
    stored_hash = await get_admin_password_hash(db)
    
    # Verify current password
    if not verify_password(request.current_password, stored_hash):
        raise HTTPException(
            status_code=400,
            detail="Current password is incorrect"
        )
    
    # Validate new password
    if len(request.new_password) < 6:
        raise HTTPException(
            status_code=400,
            detail="New password must be at least 6 characters"
        )
    
    # Hash and save new password
    new_hash = hash_password(request.new_password)
    await update_admin_password(db, new_hash)
    
    return {"message": "Password changed successfully"}

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
