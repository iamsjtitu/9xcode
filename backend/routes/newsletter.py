from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import StreamingResponse
from database import subscribers_collection
from datetime import datetime, timezone
from pydantic import BaseModel, EmailStr
import io, csv

router = APIRouter(prefix="/newsletter", tags=["newsletter"])

class SubscribeRequest(BaseModel):
    email: str

@router.post("/subscribe")
async def subscribe(req: SubscribeRequest):
    email = req.email.strip().lower()
    if not email or '@' not in email:
        raise HTTPException(status_code=400, detail="Invalid email address")
    existing = await subscribers_collection.find_one({'email': email})
    if existing:
        raise HTTPException(status_code=409, detail="Already subscribed")
    await subscribers_collection.insert_one({
        'email': email,
        'subscribedAt': datetime.now(timezone.utc).isoformat(),
    })
    return {"message": "Successfully subscribed!", "email": email}

@router.get("/subscribers")
async def list_subscribers(
    page: int = Query(1, ge=1),
    limit: int = Query(50, ge=1, le=200),
    search: str = Query(None),
):
    query = {}
    if search:
        query['email'] = {'$regex': search, '$options': 'i'}
    total = await subscribers_collection.count_documents(query)
    skip = (page - 1) * limit
    cursor = subscribers_collection.find(query, {'_id': 0}).sort('subscribedAt', -1).skip(skip).limit(limit)
    subs = await cursor.to_list(length=limit)
    return {"subscribers": subs, "total": total, "page": page, "pages": (total + limit - 1) // limit}

@router.get("/subscribers/export")
async def export_subscribers_csv():
    cursor = subscribers_collection.find({}, {'_id': 0}).sort('subscribedAt', -1)
    subs = await cursor.to_list(length=100000)
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['Email', 'Subscribed At'])
    for s in subs:
        writer.writerow([s['email'], s.get('subscribedAt', '')])
    output.seek(0)
    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=subscribers.csv"}
    )

@router.delete("/subscribers/{email}")
async def delete_subscriber(email: str):
    result = await subscribers_collection.delete_one({'email': email.lower()})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Subscriber not found")
    return {"message": "Subscriber removed"}

@router.get("/subscribers/count")
async def subscriber_count():
    total = await subscribers_collection.count_documents({})
    return {"count": total}
