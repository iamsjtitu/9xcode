from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
import os
import json

try:
    from emergentintegrations.llm.chat import LlmChat, UserMessage
    HAS_LLM = True
except ImportError:
    HAS_LLM = False

load_dotenv()

router = APIRouter(prefix="/ai-rewrite", tags=["ai-rewrite"])

EMERGENT_KEY = os.environ.get("EMERGENT_LLM_KEY")

SYSTEM_PROMPT = """You are a technical content writer for 9xCodes.com, a platform for Linux server commands and code tutorials. 

Your job is to REWRITE the given article content in the 9xCodes style:
- Clear, concise step-by-step instructions
- Each step should have a descriptive title and explanation
- Code blocks should be clean and well-formatted
- Use a friendly but professional tone
- Make the content unique and original while keeping technical accuracy
- Improve descriptions to be more helpful for beginners
- Keep all commands and code accurate - do NOT modify working commands

Return your response as valid JSON with this structure:
{
  "title": "rewritten title",
  "description": "rewritten description (max 200 chars)",
  "steps": [
    {"title": "step title", "description": "step explanation", "code": "the code/command", "language": "bash"}
  ]
}

IMPORTANT: Return ONLY valid JSON, no markdown, no backticks, no extra text."""


class RewriteRequest(BaseModel):
    title: str
    description: str
    steps: list


@router.post("/rewrite")
async def rewrite_article(req: RewriteRequest):
    """Rewrite article content using AI in 9xCodes style"""
    if not HAS_LLM:
        raise HTTPException(status_code=501, detail="AI library not installed. Run: pip install emergentintegrations --extra-index-url https://d33sy5i8bnduwe.cloudfront.net/simple/")
    if not EMERGENT_KEY:
        raise HTTPException(status_code=500, detail="AI service not configured. Add EMERGENT_LLM_KEY to backend/.env")

    article_text = f"Title: {req.title}\nDescription: {req.description}\n\nSteps:\n"
    for i, step in enumerate(req.steps):
        article_text += f"\nStep {i+1}: {step.get('title', '')}\n"
        article_text += f"Description: {step.get('description', '')}\n"
        article_text += f"Code: {step.get('code', '')}\n"

    try:
        chat = LlmChat(
            api_key=EMERGENT_KEY,
            session_id=f"rewrite-{req.title[:20]}",
            system_message=SYSTEM_PROMPT,
        )
        chat.with_model("openai", "gpt-4o-mini")

        user_msg = UserMessage(text=f"Rewrite this article in 9xCodes style:\n\n{article_text}")
        response = await chat.send_message(user_msg)

        # Parse JSON response
        response_text = response.strip()
        # Remove markdown code blocks if present
        if response_text.startswith("```"):
            response_text = response_text.split("\n", 1)[1] if "\n" in response_text else response_text[3:]
        if response_text.endswith("```"):
            response_text = response_text[:-3]
        response_text = response_text.strip()

        rewritten = json.loads(response_text)

        return {
            "rewritten": rewritten,
            "original_title": req.title,
        }
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="AI returned invalid format. Please try again.")
    except Exception as e:
        error_msg = str(e)
        if "balance" in error_msg.lower() or "credit" in error_msg.lower():
            raise HTTPException(status_code=402, detail="LLM key balance low. Go to Profile -> Universal Key -> Add Balance.")
        raise HTTPException(status_code=500, detail=f"AI rewrite failed: {error_msg}")
