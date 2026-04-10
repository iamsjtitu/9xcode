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
- 289+ articles, Dark/Light mode toggle (GitHub-style professional design)
- Social sharing, SEO (sitemap, robots.txt, JSON-LD, RSS feed)
- Google AdSense integration

### Reader Features
- Most Popular, Related Articles, Bookmarks, Copy Code, Search Autocomplete
- Table of Contents, Reading time, Homepage Pagination

### Public Pages
- Home (/), About (/about), Contact (/contact), Contribute (/contribute)
- Privacy Policy (/privacy-policy), Terms of Service (/terms-of-service), Disclaimer (/disclaimer)

### Admin Features
- Newsletter (/admin/subscribers), Bulk Articles (/admin/articles)
- Contributions (/admin/contributions), Messages (/admin/messages)
- Article Scraper (/admin/scraper) - curl_cffi for Cloudflare bypass
- AI Tools in Scraper: Full Optimize, Rewrite, SEO Optimize, Summarize
- **Bulk AI Optimize** (/admin/bulk-optimize):
  - Select articles individually or all at once
  - Category & status (Pending/Optimized) filters
  - Real-time progress bar with start/stop control
  - Per-article status tracking (processing/done/failed)
  - Auto-stops on LLM balance errors (402) or after 3 consecutive failures
  - Shows descriptive error banner with fix instructions
  - Pagination (50 per page)
- Per-Article Analytics (/admin/per-article-analytics)
- One-Click VPS Update (update_script.sh) with manual fallback commands

### AI Integration (Dual-mode)
- **On Emergent platform**: Uses EMERGENT_LLM_KEY via emergentintegrations
- **On VPS**: Uses direct OPENAI_API_KEY via litellm (GPT-4o-mini)
- Automatic fallback: prefers OPENAI_API_KEY if set, otherwise uses EMERGENT_LLM_KEY

### SEO
- Dynamic sitemap.xml, robots.txt, RSS feed, meta tags, JSON-LD, ads.txt

## Credentials
- Admin: admin / admin123
- OPENAI_API_KEY in backend/.env (for VPS AI features)

## VPS Info
- Path: /var/www/9xcodes, Venv: backend/venv

## Key API Endpoints
- GET /api/ai-rewrite/articles-for-optimize
- POST /api/ai-rewrite/optimize-existing (returns 402 on budget errors, 403 on access denied)
- POST /api/ai-rewrite/rewrite, /seo-optimize, /summarize, /full-optimize
- POST /api/scraper/from-url, /save, /discover
- POST /api/updater/update & GET /api/updater/status

## Bug Fixes (Apr 9, 2026)
- Fixed Emergent key "FREE_USER_EXTERNAL_ACCESS_DENIED" on VPS → added direct OpenAI API key support
- Fixed budget/balance error detection (catches "budget", "exceeded", "quota", "insufficient_quota")
- Fixed updater log parsing - searches ALL lines for RESULT
- Fixed inline updater race condition - writes RESULT before PM2 restart
- Added auto-stop in BulkOptimize after 3 consecutive failures
- Added error banner + manual update commands fallback in AdminPanel
- Increased updater retry count from 10 to 15

## Future/Backlog (P2)
- User comment moderation
- Bulk Optimize all 294 articles for AdSense approval
- Guide user to reapply for Google AdSense
