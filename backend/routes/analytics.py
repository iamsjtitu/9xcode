from fastapi import APIRouter, Depends, HTTPException
from database import get_db
from auth import get_current_user
from datetime import datetime, timezone, timedelta
from typing import Optional

router = APIRouter(prefix="/analytics", tags=["analytics"])

@router.get("/dashboard")
async def get_dashboard_stats(current_user: dict = Depends(get_current_user)):
    """Get analytics dashboard data for admin"""
    db = await get_db()
    
    # Total articles
    total_articles = await db.code_snippets.count_documents({})
    
    # Total views (sum of all article views)
    pipeline = [
        {"$group": {"_id": None, "total_views": {"$sum": "$views"}}}
    ]
    views_result = await db.code_snippets.aggregate(pipeline).to_list(1)
    total_views = views_result[0]["total_views"] if views_result else 0
    
    # Total likes
    likes_pipeline = [
        {"$group": {"_id": None, "total_likes": {"$sum": "$likes"}}}
    ]
    likes_result = await db.code_snippets.aggregate(likes_pipeline).to_list(1)
    total_likes = likes_result[0]["total_likes"] if likes_result else 0
    
    # Total comments
    total_comments = await db.comments.count_documents({})
    
    # Articles by category
    category_pipeline = [
        {"$group": {"_id": "$category", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}}
    ]
    categories = await db.code_snippets.aggregate(category_pipeline).to_list(20)
    
    # Top 10 most viewed articles
    top_articles = await db.code_snippets.find(
        {},
        {"_id": 0, "title": 1, "slug": 1, "views": 1, "likes": 1, "category": 1}
    ).sort("views", -1).limit(10).to_list(10)
    
    # Articles by difficulty
    difficulty_pipeline = [
        {"$group": {"_id": "$difficulty", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}}
    ]
    difficulties = await db.code_snippets.aggregate(difficulty_pipeline).to_list(10)
    
    # Recent articles (last 7 days)
    week_ago = datetime.now(timezone.utc) - timedelta(days=7)
    recent_count = await db.code_snippets.count_documents({
        "createdAt": {"$gte": week_ago}
    })
    
    # Top tags
    tags_pipeline = [
        {"$unwind": "$tags"},
        {"$group": {"_id": "$tags", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 15}
    ]
    top_tags = await db.code_snippets.aggregate(tags_pipeline).to_list(15)
    
    return {
        "overview": {
            "total_articles": total_articles,
            "total_views": total_views,
            "total_likes": total_likes,
            "total_comments": total_comments,
            "articles_this_week": recent_count
        },
        "categories": [{"name": c["_id"], "count": c["count"]} for c in categories],
        "difficulties": [{"name": d["_id"], "count": d["count"]} for d in difficulties],
        "top_articles": top_articles,
        "top_tags": [{"name": t["_id"], "count": t["count"]} for t in top_tags]
    }

@router.get("/traffic")
async def get_traffic_data(
    days: int = 30,
    current_user: dict = Depends(get_current_user)
):
    """Get traffic data over time"""
    db = await get_db()
    
    start_date = datetime.now(timezone.utc) - timedelta(days=days)
    
    # Articles created per day
    pipeline = [
        {"$match": {"createdAt": {"$gte": start_date}}},
        {
            "$group": {
                "_id": {
                    "$dateToString": {"format": "%Y-%m-%d", "date": "$createdAt"}
                },
                "count": {"$sum": 1},
                "views": {"$sum": "$views"}
            }
        },
        {"$sort": {"_id": 1}}
    ]
    
    daily_data = await db.code_snippets.aggregate(pipeline).to_list(days)
    
    return {
        "period": f"Last {days} days",
        "daily_stats": daily_data
    }
