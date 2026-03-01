from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import StreamingResponse
from database import snippets_collection
from typing import List, Optional
from pydantic import BaseModel
import io, csv, json

router = APIRouter(prefix="/articles", tags=["articles"])

class BulkDeleteRequest(BaseModel):
    slugs: List[str]

class BulkCategoryRequest(BaseModel):
    slugs: List[str]
    category: str

@router.post("/bulk-delete")
async def bulk_delete(req: BulkDeleteRequest):
    if not req.slugs:
        raise HTTPException(status_code=400, detail="No articles selected")
    result = await snippets_collection.delete_many({'slug': {'$in': req.slugs}})
    return {"deleted": result.deleted_count, "message": f"{result.deleted_count} articles deleted"}

@router.post("/bulk-category")
async def bulk_update_category(req: BulkCategoryRequest):
    if not req.slugs:
        raise HTTPException(status_code=400, detail="No articles selected")
    result = await snippets_collection.update_many(
        {'slug': {'$in': req.slugs}},
        {'$set': {'category': req.category}}
    )
    return {"modified": result.modified_count, "message": f"{result.modified_count} articles updated"}

@router.get("/export")
async def export_articles(format: str = Query("csv")):
    cursor = snippets_collection.find({}, {'_id': 0}).sort('createdAt', -1)
    articles = await cursor.to_list(length=100000)
    if format == "json":
        for a in articles:
            if 'createdAt' in a:
                a['createdAt'] = str(a['createdAt'])
            if 'updatedAt' in a:
                a['updatedAt'] = str(a['updatedAt'])
        content = json.dumps(articles, indent=2)
        return StreamingResponse(
            iter([content]),
            media_type="application/json",
            headers={"Content-Disposition": "attachment; filename=articles.json"}
        )
    # CSV
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['Title', 'Slug', 'Category', 'Difficulty', 'OS', 'Tags', 'Views', 'Likes', 'Author', 'Created At'])
    for a in articles:
        writer.writerow([
            a.get('title', ''),
            a.get('slug', ''),
            a.get('category', ''),
            a.get('difficulty', ''),
            ', '.join(a.get('os', [])),
            ', '.join(a.get('tags', [])),
            a.get('views', 0),
            a.get('likes', 0),
            a.get('author', ''),
            str(a.get('createdAt', '')),
        ])
    output.seek(0)
    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=articles.csv"}
    )

@router.get("/list")
async def list_articles_admin(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    category: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
):
    query = {}
    if category:
        query['category'] = category
    if search:
        query['$or'] = [
            {'title': {'$regex': search, '$options': 'i'}},
            {'description': {'$regex': search, '$options': 'i'}},
        ]
    total = await snippets_collection.count_documents(query)
    skip = (page - 1) * limit
    cursor = snippets_collection.find(query, {'_id': 0, 'steps': 0}).sort('createdAt', -1).skip(skip).limit(limit)
    articles = await cursor.to_list(length=limit)
    return {
        "articles": articles,
        "total": total,
        "page": page,
        "pages": (total + limit - 1) // limit,
    }
