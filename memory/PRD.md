# 9xCodes.com - Product Requirements Document

## Original Problem Statement
Build a website named `www.9xcodes.com`, a platform for posting code snippets and server commands.

## Tech Stack
- **Frontend**: React, React Router, TailwindCSS, Shadcn UI, Axios
- **Backend**: FastAPI, Pydantic, Motor, Passlib, BeautifulSoup4, emergentintegrations (LLM)
- **Database**: MongoDB
- **Deployment**: Nginx, PM2, Certbot (SSL), Ubuntu VPS

## What's Been Implemented (Complete)

### Core Features
- Full-stack app live at 9xcodes.com
- Admin panel with stats dashboard, password change
- 278+ articles across 15 categories
- Social sharing, SEO (sitemap, robots.txt, JSON-LD, RSS feed)

### Reader Features
- Most Popular Articles, Related Articles, Bookmarks, Copy Code Button
- Tag-based Search, Table of Contents, Reading time, Search Autocomplete
- Homepage Pagination (12 per page)
- Dark/Light Mode Toggle (persists in localStorage)

### Pages
- About Us (/about), Contact Us (/contact), Contribute (/contribute)

### Admin Features
- Newsletter Subscribers (/admin/subscribers)
- Bulk Article Management (/admin/articles)
- Article Seeder (/admin/seeder)
- Contributions Manager (/admin/contributions)
- Contact Messages (/admin/messages)
- Article Scraper (/admin/scraper) with AI rewrite
- Per-Article Analytics (/admin/per-article-analytics)
- **One-Click Website Update** (git pull -> build -> restart from Admin Panel)
- Google AdSense integration

### One-Click VPS Update (NEW - Completed)
- "Update Website" banner in Admin Panel
- Runs: git pull -> pip install -> yarn build -> pm2 restart all
- Background execution with real-time log streaming
- Status tracking (running/success/failed/skipped)
- Auto-detects VPS vs preview environment
- Project path: /var/www/9xcodes

## Key API Endpoints
- Snippets: GET /api/snippets, /popular, /search-suggestions, /{slug}, /{slug}/related
- Newsletter: POST /api/newsletter/subscribe, GET /subscribers, /export
- Articles: GET /api/articles/list, POST /bulk-delete, /bulk-category, GET /export
- Seeder: GET /api/seeder/categories, POST /preview, /seed
- Contributions: POST /api/contributions/submit, GET /contributions, POST /{id}/approve, /{id}/reject
- Contact: POST /api/contact, GET /api/contact/messages
- SEO: GET /api/seo/sitemap.xml, /robots.txt, /rss.xml
- Scraper: POST /api/scraper/from-url, /save, /discover
- Article Analytics: GET /api/article-analytics/overview, /top-articles, /category-stats, /article/{slug}
- AI Rewrite: POST /api/ai-rewrite/rewrite
- **Updater**: POST /api/updater/update, GET /api/updater/status

## DB Collections
- code_snippets, comments, google_ads_config, subscribers, users, contributions, contact_messages

## Credentials
- Admin: admin / admin123

## Future/Backlog Tasks (P2)
- Moderation interface for user comments
