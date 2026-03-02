from fastapi import APIRouter, HTTPException, Query
from database import db
from pydantic import BaseModel
from datetime import datetime, timezone
import uuid

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
        'id': str(uuid.uuid4()),
        'name': msg.name,
        'email': msg.email,
        'subject': msg.subject,
        'message': msg.message,
        'createdAt': datetime.now(timezone.utc).isoformat(),
    })
    return {"message": "Message sent successfully!"}

@router.get("/messages")
async def list_messages(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    search: str = Query(None),
):
    query = {}
    if search:
        query['$or'] = [
            {'name': {'$regex': search, '$options': 'i'}},
            {'email': {'$regex': search, '$options': 'i'}},
            {'subject': {'$regex': search, '$options': 'i'}},
        ]
    total = await contact_collection.count_documents(query)
    skip = (page - 1) * limit
    cursor = contact_collection.find(query, {'_id': 0}).sort('createdAt', -1).skip(skip).limit(limit)
    msgs = await cursor.to_list(length=limit)
    return {"messages": msgs, "total": total, "page": page, "pages": max(1, (total + limit - 1) // limit)}

@router.delete("/messages/{message_id}")
async def delete_message(message_id: str):
    result = await contact_collection.delete_one({'id': message_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Message not found")
    return {"message": "Message deleted"}
