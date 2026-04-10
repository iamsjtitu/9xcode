from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from database import snippets_collection
from dotenv import load_dotenv
from datetime import datetime, timezone
import os
import json

try:
    from emergentintegrations.llm.chat import LlmChat, UserMessage
    HAS_EMERGENT = True
except ImportError:
    HAS_EMERGENT = False

try:
    import litellm
    HAS_LITELLM = True
except ImportError:
    HAS_LITELLM = False

load_dotenv()

router = APIRouter(prefix="/ai-rewrite", tags=["ai-rewrite"])

EMERGENT_KEY = os.environ.get("EMERGENT_LLM_KEY")
OPENAI_KEY = os.environ.get("OPENAI_API_KEY")


def check_ai():
    if OPENAI_KEY and HAS_LITELLM:
        return  # Direct OpenAI mode
    if HAS_EMERGENT and EMERGENT_KEY:
        return  # Emergent mode
    if not HAS_EMERGENT and not HAS_LITELLM:
        raise HTTPException(status_code=501, detail="AI library not installed.")
    raise HTTPException(status_code=500, detail="AI not configured. Add OPENAI_API_KEY or EMERGENT_LLM_KEY to backend/.env")


def clean_json(text):
    text = text.strip()
    if text.startswith("```json"):
        text = text[7:]
    elif text.startswith("```"):
        text = text.split("\n", 1)[1] if "\n" in text else text[3:]
    if text.endswith("```"):
        text = text[:-3]
    return text.strip()


async def _do_ai_call(system_msg, user_msg_text, session_prefix):
    """Single AI call — returns raw text response"""
    if OPENAI_KEY and HAS_LITELLM:
        response = await litellm.acompletion(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_msg},
                {"role": "user", "content": user_msg_text},
            ],
            api_key=OPENAI_KEY,
        )
        return response.choices[0].message.content
    else:
        chat = LlmChat(
            api_key=EMERGENT_KEY,
            session_id=f"{session_prefix}-{hash(user_msg_text[:30])}",
            system_message=system_msg,
        )
        chat.with_model("openai", "gpt-4o-mini")
        return await chat.send_message(UserMessage(text=user_msg_text))


async def call_ai(system_msg, user_msg_text, session_prefix="ai"):
    max_retries = 2
    for attempt in range(max_retries + 1):
        try:
            raw = await _do_ai_call(system_msg, user_msg_text, session_prefix)
            return json.loads(clean_json(raw))
        except json.JSONDecodeError:
            if attempt < max_retries:
                import asyncio
                await asyncio.sleep(1)
                continue
            raise HTTPException(status_code=500, detail="AI returned invalid format after retries. Please try again.")
        except Exception as e:
            error_msg = str(e)
            if any(kw in error_msg.lower() for kw in ["balance", "credit", "budget", "exceeded", "quota", "insufficient_quota"]):
                raise HTTPException(status_code=402, detail="API key balance low. Check your OpenAI/Emergent billing.")
            if "access_denied" in error_msg.lower() or "FREE_USER" in error_msg:
                raise HTTPException(status_code=403, detail="Emergent key external access denied. Add OPENAI_API_KEY to .env for VPS usage.")
            raise HTTPException(status_code=500, detail=f"AI failed: {error_msg}")


def article_to_text(title, description, steps):
    text = f"Title: {title}\nDescription: {description}\n\nSteps:\n"
    for i, s in enumerate(steps):
        text += f"\nStep {i+1}: {s.get('title', '')}\n"
        if s.get('description'):
            text += f"Description: {s['description']}\n"
        if s.get('code'):
            text += f"Code:\n{s['code']}\n"
    return text


# ===== PROMPTS =====

REWRITE_PROMPT = """You are a technical content writer for 9xCodes.com. Rewrite the given article to be UNIQUE and original while keeping technical accuracy.

Rules:
- Rewrite in your own words, don't copy
- Clear step-by-step instructions
- Friendly but professional tone
- Keep all commands/code accurate - do NOT modify working commands
- Make descriptions helpful for beginners

Return ONLY valid JSON:
{"title": "rewritten title", "description": "max 200 chars description", "steps": [{"title": "step title", "description": "explanation", "code": "command", "language": "bash"}]}"""

SEO_PROMPT = """You are an SEO expert for 9xCodes.com, a technical tutorial website. Generate SEO-optimized metadata for the given article.

Rules:
- Title: 50-60 chars, include primary keyword, compelling
- Description: 150-160 chars, include keywords, call to action
- Keywords: 8-12 relevant long-tail keywords
- Tags: 5-8 short tags for categorization
- Focus keyword: The main keyword to rank for

Return ONLY valid JSON:
{"seo_title": "SEO optimized title", "seo_description": "meta description 150-160 chars", "keywords": ["keyword1", "keyword2"], "tags": ["tag1", "tag2"], "focus_keyword": "main keyword"}"""

SUMMARIZE_PROMPT = """You are a content editor for 9xCodes.com. Generate a comprehensive article summary and improved description.

Rules:
- Short description: 150-200 chars, concise and engaging
- Summary: 2-3 sentences covering what the article teaches
- Key takeaways: 3-5 bullet points of what readers will learn
- Difficulty assessment: beginner/intermediate/advanced with reason

Return ONLY valid JSON:
{"description": "150-200 char description", "summary": "2-3 sentence summary", "key_takeaways": ["point1", "point2", "point3"], "difficulty": "beginner", "difficulty_reason": "why this level"}"""

FULL_OPTIMIZE_PROMPT = """You are a content and SEO expert for 9xCodes.com. Fully optimize the given article for quality, uniqueness, and SEO.

Rules:
- Rewrite title to be SEO-friendly (50-60 chars) and unique
- Write a compelling meta description (150-160 chars)
- Rewrite each step with unique descriptions (don't copy original)
- Keep all commands/code 100% accurate - NEVER modify working code
- Generate relevant tags and keywords
- Make content beginner-friendly

Return ONLY valid JSON:
{
  "title": "SEO optimized unique title",
  "description": "meta description 150-160 chars",
  "tags": ["tag1", "tag2", "tag3", "tag4", "tag5"],
  "difficulty": "beginner or intermediate or advanced",
  "steps": [{"title": "step title", "description": "unique explanation", "code": "exact original code", "language": "bash"}],
  "seo_keywords": ["keyword1", "keyword2"],
  "summary": "2-3 sentence article summary"
}"""


class RewriteRequest(BaseModel):
    title: str
    description: str
    steps: list


class SEORequest(BaseModel):
    title: str
    description: str
    category: Optional[str] = ""


class SlugRequest(BaseModel):
    slug: str


@router.get("/articles-for-optimize")
async def list_articles_for_optimize(
    page: int = 1,
    limit: int = 50,
    category: str = "",
    filter_status: str = "",
):
    """List articles with their AI optimization status"""
    query = {}
    if category:
        query["category"] = category
    if filter_status == "optimized":
        query["ai_optimized"] = True
    elif filter_status == "pending":
        query["$or"] = [{"ai_optimized": {"$exists": False}}, {"ai_optimized": False}]

    total = await snippets_collection.count_documents(query)
    skip = (page - 1) * limit
    cursor = snippets_collection.find(
        query,
        {"_id": 0, "slug": 1, "title": 1, "category": 1, "ai_optimized": 1, "views": 1, "createdAt": 1}
    ).sort("createdAt", -1).skip(skip).limit(limit)
    articles = await cursor.to_list(length=limit)

    # Get category list for filter
    categories = await snippets_collection.distinct("category")
    optimized_count = await snippets_collection.count_documents({"ai_optimized": True})

    return {
        "articles": articles,
        "total": total,
        "page": page,
        "pages": (total + limit - 1) // limit,
        "categories": sorted([c for c in categories if c]),
        "optimized_count": optimized_count,
        "total_articles": await snippets_collection.count_documents({}),
    }


@router.post("/rewrite")
async def rewrite_article(req: RewriteRequest):
    """Rewrite article content to be unique"""
    check_ai()
    text = article_to_text(req.title, req.description, req.steps)
    result = await call_ai(REWRITE_PROMPT, f"Rewrite this article:\n\n{text}", "rewrite")
    return {"rewritten": result, "original_title": req.title}


@router.post("/seo-optimize")
async def seo_optimize(req: SEORequest):
    """Generate SEO metadata for an article"""
    check_ai()
    text = f"Title: {req.title}\nDescription: {req.description}\nCategory: {req.category}"
    result = await call_ai(SEO_PROMPT, f"Generate SEO metadata for:\n\n{text}", "seo")
    return {"seo": result, "original_title": req.title}


@router.post("/summarize")
async def summarize_article(req: RewriteRequest):
    """Generate article summary and key takeaways"""
    check_ai()
    text = article_to_text(req.title, req.description, req.steps)
    result = await call_ai(SUMMARIZE_PROMPT, f"Summarize this article:\n\n{text}", "summary")
    return {"summary": result, "original_title": req.title}


@router.post("/full-optimize")
async def full_optimize(req: RewriteRequest):
    """Full AI optimization: rewrite + SEO + summary in one call"""
    check_ai()
    text = article_to_text(req.title, req.description, req.steps)
    result = await call_ai(FULL_OPTIMIZE_PROMPT, f"Fully optimize this article:\n\n{text}", "optimize")
    return {"optimized": result, "original_title": req.title}


@router.post("/optimize-existing")
async def optimize_existing_article(req: SlugRequest):
    """Apply full AI optimization to an existing article in the database"""
    check_ai()

    article = await snippets_collection.find_one({"slug": req.slug}, {"_id": 0})
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")

    text = article_to_text(
        article.get("title", ""),
        article.get("description", ""),
        article.get("steps", [])
    )
    result = await call_ai(FULL_OPTIMIZE_PROMPT, f"Fully optimize this article:\n\n{text}", "opt-exist")

    # Update the article in DB
    update_data = {
        "title": result.get("title", article.get("title")),
        "description": result.get("description", article.get("description")),
        "tags": result.get("tags", article.get("tags", [])),
        "difficulty": result.get("difficulty", article.get("difficulty")),
        "updatedAt": datetime.now(timezone.utc),
        "ai_optimized": True,
    }
    if result.get("steps"):
        update_data["steps"] = result["steps"]

    await snippets_collection.update_one({"slug": req.slug}, {"$set": update_data})

    return {
        "message": f"Article '{req.slug}' optimized!",
        "optimized": result,
    }
