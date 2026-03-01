from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from models import CodeSnippet, CodeSnippetCreate
from database import snippets_collection
import re
from datetime import datetime

router = APIRouter(prefix="/snippets", tags=["snippets"])

def create_slug(title: str) -> str:
    """Create URL-friendly slug from title"""
    slug = title.lower()
    slug = re.sub(r'[^a-z0-9]+', '-', slug)
    slug = slug.strip('-')
    return slug

@router.post("", response_model=CodeSnippet)
async def create_snippet(snippet: CodeSnippetCreate):
    """Create a new code snippet"""
    snippet_dict = snippet.dict()
    snippet_dict['slug'] = create_slug(snippet.title)
    snippet_dict['views'] = 0
    snippet_dict['likes'] = 0
    snippet_dict['author'] = 'Admin'
    snippet_dict['createdAt'] = datetime.utcnow()
    snippet_dict['updatedAt'] = datetime.utcnow()
    
    # Convert tags string to list if needed
    if isinstance(snippet_dict.get('tags'), str):
        snippet_dict['tags'] = [tag.strip() for tag in snippet_dict['tags'].split(',') if tag.strip()]
    
    snippet_obj = CodeSnippet(**snippet_dict)
    result = await snippets_collection.insert_one(snippet_obj.dict())
    
    if result.inserted_id:
        return snippet_obj
    raise HTTPException(status_code=500, detail="Failed to create snippet")

@router.get("/popular", response_model=List[CodeSnippet])
async def get_popular_snippets(limit: int = Query(6)):
    """Get most popular snippets by views"""
    cursor = snippets_collection.find().sort([('views', -1)]).limit(limit)
    snippets = await cursor.to_list(length=limit)
    return [CodeSnippet(**s) for s in snippets]

@router.get("", response_model=List[CodeSnippet])
async def get_snippets(
    category: Optional[str] = Query(None),
    os: Optional[str] = Query(None),
    difficulty: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    tag: Optional[str] = Query(None),
    sort: Optional[str] = Query("recent"),
    limit: Optional[int] = Query(100)
):
    """Get all code snippets with optional filters"""
    query = {}
    
    if category:
        query['category'] = category
    if os:
        query['os'] = {'$in': [os]}
    if difficulty:
        query['difficulty'] = difficulty
    if tag:
        # Exact tag match for subcategory filtering
        query['tags'] = {'$in': [tag]}
    if search:
        query['$or'] = [
            {'title': {'$regex': search, '$options': 'i'}},
            {'description': {'$regex': search, '$options': 'i'}},
            {'tags': {'$in': [re.compile(search, re.IGNORECASE)]}}
        ]
    
    # Sort
    sort_by = []
    if sort == "popular":
        sort_by = [('likes', -1)]
    elif sort == "views":
        sort_by = [('views', -1)]
    else:  # recent
        sort_by = [('createdAt', -1)]
    
    cursor = snippets_collection.find(query).sort(sort_by).limit(limit)
    snippets = await cursor.to_list(length=limit)
    
    return [CodeSnippet(**snippet) for snippet in snippets]

@router.get("/{slug}", response_model=CodeSnippet)
async def get_snippet(slug: str):
    """Get a single code snippet by slug"""
    snippet = await snippets_collection.find_one({'slug': slug})
    
    if not snippet:
        raise HTTPException(status_code=404, detail="Snippet not found")
    
    # Increment views
    await snippets_collection.update_one(
        {'slug': slug},
        {'$inc': {'views': 1}}
    )
    snippet['views'] += 1
    
    return CodeSnippet(**snippet)

@router.post("/{slug}/like")
async def like_snippet(slug: str):
    """Like a code snippet"""
    result = await snippets_collection.update_one(
        {'slug': slug},
        {'$inc': {'likes': 1}}
    )
    
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Snippet not found")
    
    snippet = await snippets_collection.find_one({'slug': slug})
    return {'likes': snippet['likes']}

@router.delete("/{slug}")
async def delete_snippet(slug: str):
    """Delete a code snippet"""
    result = await snippets_collection.delete_one({'slug': slug})
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Snippet not found")
    
    return {'message': 'Snippet deleted successfully'}