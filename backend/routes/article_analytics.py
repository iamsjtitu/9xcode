from fastapi import APIRouter, HTTPException
from database import snippets_collection
from bson import ObjectId
from datetime import datetime, timezone, timedelta

router = APIRouter(prefix="/article-analytics", tags=["article-analytics"])


@router.get("/top-articles")
async def get_top_articles(limit: int = 20, sort_by: str = "views"):
    """Get top performing articles sorted by views or likes"""
    sort_field = "views" if sort_by == "views" else "likes"
    cursor = snippets_collection.find(
        {},
        {"_id": 0, "id": 1, "title": 1, "slug": 1, "category": 1, "views": 1, "likes": 1, "createdAt": 1, "tags": 1}
    ).sort(sort_field, -1).limit(limit)
    articles = await cursor.to_list(length=limit)
    return articles


@router.get("/category-stats")
async def get_category_stats():
    """Get aggregated stats per category"""
    pipeline = [
        {"$group": {
            "_id": "$category",
            "count": {"$sum": 1},
            "total_views": {"$sum": "$views"},
            "total_likes": {"$sum": "$likes"},
            "avg_views": {"$avg": "$views"},
            "avg_likes": {"$avg": "$likes"},
        }},
        {"$sort": {"total_views": -1}},
    ]
    results = await snippets_collection.aggregate(pipeline).to_list(length=50)
    return [
        {
            "category": r["_id"] or "uncategorized",
            "count": r["count"],
            "total_views": r["total_views"],
            "total_likes": r["total_likes"],
            "avg_views": round(r["avg_views"], 1),
            "avg_likes": round(r["avg_likes"], 1),
        }
        for r in results
    ]


@router.get("/article/{slug}")
async def get_article_analytics(slug: str):
    """Get detailed analytics for a single article"""
    article = await snippets_collection.find_one(
        {"slug": slug},
        {"_id": 0, "id": 1, "title": 1, "slug": 1, "category": 1, "views": 1, "likes": 1, "tags": 1, "createdAt": 1, "difficulty": 1, "os": 1, "steps": 1}
    )
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")

    steps_count = len(article.get("steps", []))
    code_lines = sum(len(s.get("code", "").split("\n")) for s in article.get("steps", []))

    return {
        **article,
        "steps_count": steps_count,
        "total_code_lines": code_lines,
        "engagement_rate": round((article.get("likes", 0) / max(article.get("views", 1), 1)) * 100, 2),
    }


@router.get("/overview")
async def get_analytics_overview():
    """Get overall analytics overview"""
    total = await snippets_collection.count_documents({})

    pipeline_totals = [
        {"$group": {
            "_id": None,
            "total_views": {"$sum": "$views"},
            "total_likes": {"$sum": "$likes"},
        }}
    ]
    totals = await snippets_collection.aggregate(pipeline_totals).to_list(length=1)
    total_views = totals[0]["total_views"] if totals else 0
    total_likes = totals[0]["total_likes"] if totals else 0

    # Top 5 by views
    top_viewed = await snippets_collection.find(
        {}, {"_id": 0, "title": 1, "slug": 1, "views": 1, "category": 1}
    ).sort("views", -1).limit(5).to_list(length=5)

    # Top 5 by likes
    top_liked = await snippets_collection.find(
        {}, {"_id": 0, "title": 1, "slug": 1, "likes": 1, "category": 1}
    ).sort("likes", -1).limit(5).to_list(length=5)

    # Articles with 0 views
    zero_views = await snippets_collection.count_documents({"views": 0})

    return {
        "total_articles": total,
        "total_views": total_views,
        "total_likes": total_likes,
        "avg_views": round(total_views / max(total, 1), 1),
        "avg_likes": round(total_likes / max(total, 1), 1),
        "zero_view_articles": zero_views,
        "top_viewed": top_viewed,
        "top_liked": top_liked,
    }
