# 9xCodes.com - Product Requirements Document

## Original Problem Statement
Build a website named `www.9xcodes.com`, a platform for posting code snippets and server commands.

## Tech Stack
- **Frontend**: React, React Router, TailwindCSS, Shadcn UI, Axios
- **Backend**: FastAPI, Pydantic, Motor, Passlib, BeautifulSoup4, cloudscraper, emergentintegrations (LLM)
- **Database**: MongoDB
- **Deployment**: Nginx, PM2, Certbot (SSL), Ubuntu VPS at /var/www/9xcodes

## What's Been Implemented (Complete)

### Core Features
- Full-stack app live at 9xcodes.com
- Admin panel with stats dashboard, password change
- 278+ articles across 15 categories
- Social sharing, SEO (sitemap, robots.txt, JSON-LD, RSS feed)
- Dark/Light Mode Toggle

### Reader Features
- Most Popular Articles, Related Articles, Bookmarks, Copy Code Button
- Search Autocomplete, Table of Contents, Reading time
- Homepage Pagination (12 per page)

### Admin Features
- Newsletter Subscribers (/admin/subscribers)
- Bulk Article Management (/admin/articles)
- Contributions Manager (/admin/contributions)
- Contact Messages (/admin/messages)
- Article Scraper (/admin/scraper) - with Cloudflare bypass (cloudscraper)
- Per-Article Analytics (/admin/per-article-analytics)
- One-Click Website Update (shell script based)
- Google AdSense integration

### Article Scraper
- Uses cloudscraper for Cloudflare bypass (handles 403 errors)
- Sources: TecMint, PhoenixNAP, DigitalOcean
- AI Rewrite with GPT-4o-mini (requires EMERGENT_LLM_KEY)
- Preview, edit, save workflow

### Removed Features
- Article Seeder (removed from admin panel per user request)

## Credentials
- Admin: admin / admin123

## VPS Deployment
- Project path: /var/www/9xcodes
- Backend venv: /var/www/9xcodes/backend/venv
- PM2 process: 9xcodes-backend
- New packages needed on VPS: cloudscraper (pip install cloudscraper)

## Future/Backlog Tasks (P2)
- User comment moderation interface
