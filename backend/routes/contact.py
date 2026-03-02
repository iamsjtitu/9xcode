from fastapi import APIRouter, HTTPException
from database import db
from pydantic import BaseModel
from datetime import datetime, timezone

router = APIRouter(prefix="/contact", tags=["contact"])

contact_collection = db.contact_messages

class ContactMessage(BaseModel):
    name: str
    email: str
    subject: str
    message: str

@router.post("")
async def submit_contact(msg: ContactMessage):
    if not msg.name or not msg.email or not msg.message:
        raise HTTPException(status_code=400, detail="All fields are required")
    await contact_collection.insert_one({
        'name': msg.name,
        'email': msg.email,
        'subject': msg.subject,
        'message': msg.message,
        'createdAt': datetime.now(timezone.utc).isoformat(),
    })
    return {"message": "Message sent successfully!"}
