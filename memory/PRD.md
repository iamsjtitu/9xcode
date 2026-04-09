# 9xCodes.com - Product Requirements Document

## Original Problem Statement
Build a website named `www.9xcodes.com`, a platform for posting code snippets and server commands.

## Tech Stack
- **Frontend**: React, React Router, TailwindCSS, Shadcn UI, Axios, react-helmet
- **Backend**: FastAPI, Pydantic, Motor, Passlib, BeautifulSoup4, curl_cffi, emergentintegrations
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
  - Overall optimization progress stats
- Per-Article Analytics (/admin/per-article-analytics)
- One-Click VPS Update (update_script.sh) with manual fallback commands

### SEO
- Dynamic sitemap.xml, robots.txt, RSS feed, meta tags, JSON-LD, ads.txt

## Credentials
- Admin: admin / admin123

## VPS Info
- Path: /var/www/9xcodes, Venv: backend/venv
- New packages: curl_cffi, cloudscraper, emergentintegrations

## Key API Endpoints
- GET /api/ai-rewrite/articles-for-optimize - List articles with AI opt status
- POST /api/ai-rewrite/optimize-existing - Optimize single article by slug (returns 402 on budget errors)
- POST /api/ai-rewrite/rewrite, /seo-optimize, /summarize, /full-optimize
- POST /api/scraper/from-url, /save, /discover
- POST /api/updater/update - Trigger VPS update
- GET /api/updater/status - Get update status with logs

## Bug Fixes (Apr 9, 2026)
- Fixed budget/balance error detection in call_ai() - now catches "budget", "exceeded", "quota" keywords
- Fixed updater log parsing - searches ALL lines for RESULT, not just last line
- Fixed inline updater race condition - writes RESULT before PM2 restart
- Added auto-stop in BulkOptimize after 3 consecutive failures
- Added error banner in BulkOptimize with fix instructions
- Added manual update commands fallback in AdminPanel
- Increased updater retry count from 10 to 15 for PM2 restart

## Future/Backlog (P2)
- User comment moderation
- Use Bulk Optimize to process all 289 articles for AdSense approval
- Guide user to reapply for Google AdSense after content optimization
