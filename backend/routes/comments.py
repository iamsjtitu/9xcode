from fastapi import APIRouter, HTTPException
from typing import List
from models import Comment, CommentCreate
from database import comments_collection

router = APIRouter(prefix="/comments", tags=["comments"])

@router.post("", response_model=Comment)
async def create_comment(comment: CommentCreate):
    """Create a new comment"""
    comment_obj = Comment(**comment.dict())
    result = await comments_collection.insert_one(comment_obj.dict())
    
    if result.inserted_id:
        return comment_obj
    raise HTTPException(status_code=500, detail="Failed to create comment")

@router.get("/{snippet_id}", response_model=List[Comment])
async def get_comments(snippet_id: str):
    """Get all comments for a snippet"""
    cursor = comments_collection.find({'snippetId': snippet_id}).sort('createdAt', -1)
    comments = await cursor.to_list(length=1000)
    return [Comment(**comment) for comment in comments]