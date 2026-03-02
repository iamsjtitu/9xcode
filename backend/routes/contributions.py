from fastapi import APIRouter, HTTPException, Query
from database import db
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime, timezone
import uuid, re

router = APIRouter(prefix="/contributions", tags=["contributions"])

contributions_collection = db.contributions

def create_slug(title):
    s = re.sub(r'[^a-z0-9]+', '-', title.lower())
    return s.strip('-')

class ContributionSubmit(BaseModel):
    contributorName: str
    contributorEmail: str
    title: str
    description: str
    category: str
    difficulty: str = "beginner"
    os: List[str] = []
    tags: List[str] = []
    steps: List[dict] = []

@router.post("/submit")
async def submit_contribution(req: ContributionSubmit):
    if not req.title or not req.description or not req.category or not req.steps:
        raise HTTPException(status_code=400, detail="Missing required fields")
    if not req.contributorName or not req.contributorEmail:
        raise HTTPException(status_code=400, detail="Contributor name and email required")
    
    contribution = {
        'id': str(uuid.uuid4()),
        'contributorName': req.contributorName,
        'contributorEmail': req.contributorEmail,
        'title': req.title,
        'slug': create_slug(req.title),
        'description': req.description,
        'category': req.category,
        'difficulty': req.difficulty,
        'os': req.os,
        'tags': req.tags,
        'steps': req.steps,
        'status': 'pending',
        'submittedAt': datetime.now(timezone.utc).isoformat(),
    }
    await contributions_collection.insert_one(contribution)
    return {"message": "Article submitted for review!", "id": contribution['id']}

@router.get("")
async def list_contributions(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=50),
    status: str = Query("pending"),
):
    query = {'status': status}
    total = await contributions_collection.count_documents(query)
    skip = (page - 1) * limit
    cursor = contributions_collection.find(query, {'_id': 0}).sort('submittedAt', -1).skip(skip).limit(limit)
    items = await cursor.to_list(length=limit)
    return {"contributions": items, "total": total, "page": page, "pages": (total + limit - 1) // limit}

@router.post("/{contribution_id}/approve")
async def approve_contribution(contribution_id: str):
    contrib = await contributions_collection.find_one({'id': contribution_id})
    if not contrib:
        raise HTTPException(status_code=404, detail="Contribution not found")
    
    # Create the article in snippets collection
    from database import snippets_collection
    article = {
        'id': str(uuid.uuid4()),
        'title': contrib['title'],
        'slug': contrib['slug'],
        'description': contrib['description'],
        'category': contrib['category'],
        'difficulty': contrib['difficulty'],
        'os': contrib.get('os', []),
        'tags': contrib.get('tags', []),
        'steps': contrib.get('steps', []),
        'author': contrib['contributorName'],
        'views': 0,
        'likes': 0,
        'createdAt': datetime.now(timezone.utc).isoformat(),
        'updatedAt': datetime.now(timezone.utc).isoformat(),
        'postInstallation': None,
    }
    
    existing = await snippets_collection.find_one({'slug': article['slug']})
    if existing:
        article['slug'] = f"{article['slug']}-{str(uuid.uuid4())[:6]}"
    
    await snippets_collection.insert_one(article)
    await contributions_collection.update_one({'id': contribution_id}, {'$set': {'status': 'approved'}})
    return {"message": "Contribution approved and published!"}

@router.post("/{contribution_id}/reject")
async def reject_contribution(contribution_id: str):
    result = await contributions_collection.update_one(
        {'id': contribution_id},
        {'$set': {'status': 'rejected'}}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Contribution not found")
    return {"message": "Contribution rejected"}

@router.get("/pending-count")
async def pending_count():
    count = await contributions_collection.count_documents({'status': 'pending'})
    return {"count": count}
