# 9xCodes.com - Product Requirements Document

## Original Problem Statement
Build a website named `www.9xcodes.com`, a platform for posting code snippets and server commands.

## Tech Stack
- **Frontend**: React, React Router, TailwindCSS, Shadcn UI, Axios, react-helmet
- **Backend**: FastAPI, Pydantic, Motor, Passlib, BeautifulSoup4, curl_cffi, emergentintegrations, litellm
- **Database**: MongoDB
- **Deployment**: Nginx, PM2, Certbot (SSL), Ubuntu VPS at /var/www/9xcodes

## All Implemented Features

### Core
- Full-stack app live at 9xcodes.com
- Admin panel with dashboard, password change
- 289+ articles, Dark/Light mode toggle
- Social sharing, SEO (sitemap, robots.txt, JSON-LD, RSS feed)
- Google AdSense integration

### Content Quality (NEW - for AdSense approval)
- **Rich Article Structure**: Introduction (200+ words), Prerequisites, Detailed Steps, FAQs, Conclusion, TL;DR Summary
- **FAQ Schema (JSON-LD)**: Google FAQ rich snippets for search results
- **Article Schema (JSON-LD)**: TechArticle structured data
- **"Last Updated" date** display for freshness signals
- **Enhanced About Us page**: Detailed mission, quality standards, stats, CTA sections

### AI Integration (Dual-mode)
- **On Emergent platform**: Uses EMERGENT_LLM_KEY via emergentintegrations
- **On VPS**: Uses direct OPENAI_API_KEY via litellm (GPT-4o-mini)
- **JSON mode enforced** (`response_format: json_object`) for reliable output
- **Retry logic**: 2 retries on JSON parse failures
- **Auto-stop**: After 3 consecutive failures or 402 budget errors
- **Rich JSON extraction**: Handles malformed AI responses

### Admin Features
- Article Scraper with AI Tools (Rewrite, SEO, Summarize, Full Optimize)
- **Bulk AI Optimize** with enhanced prompt generating: intro, prerequisites, FAQs, conclusion, summary, seo_keywords
- Per-Article Analytics, Newsletter, Contributions, Messages
- One-Click VPS Update with manual fallback commands

## DB Schema Updates
- `code_snippets` collection new fields: `introduction`, `prerequisites`, `faqs`, `conclusion`, `summary`, `seo_keywords`
- `FaqSchema`: `{question: str, answer: str}`

## Credentials
- Admin: admin / admin123
- OPENAI_API_KEY in backend/.env (for VPS)
- EMERGENT_LLM_KEY in backend/.env (for Emergent platform)

## Key API Endpoints
- GET /api/snippets/{slug} - Returns full article with new fields
- POST /api/ai-rewrite/optimize-existing - Optimizes with rich content prompt
- POST /api/updater/update & GET /api/updater/status

## Completed (Apr 22, 2026)
- Fixed Emergent key "FREE_USER_EXTERNAL_ACCESS_DENIED" → added direct OpenAI API key support
- Fixed budget error detection, updater log parsing, inline updater race condition
- Upgraded AI prompt for long-form, high-quality content generation
- Added Introduction, Prerequisites, FAQ, Conclusion, Summary, SEO Keywords to articles
- Added JSON-LD structured data (FAQPage + TechArticle schemas)
- Enhanced About Us page for Google credibility
- Added FaqSchema to Pydantic models
- Reset all 289 articles for re-optimization with new prompt

## Future/Backlog
- (P1) Re-optimize all 289 articles via Bulk Optimize on VPS
- (P1) Reapply for Google AdSense after content improvement
- (P2) User comment moderation
