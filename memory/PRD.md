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
- **Dark/Light Mode Toggle** (persists in localStorage)

### Pages
- About Us (/about), Contact Us (/contact), Contribute (/contribute)

### Admin Features
- Newsletter Subscribers (/admin/subscribers)
- Bulk Article Management (/admin/articles)
- Article Seeder (/admin/seeder)
- Contributions Manager (/admin/contributions)
- Contact Messages (/admin/messages)
- **Article Scraper** (/admin/scraper) - Scrape & import external articles with AI rewrite
- **Per-Article Analytics** (/admin/per-article-analytics) - Detailed article performance metrics
- Google AdSense integration

### Dark/Light Mode (NEW - Completed)
- ThemeContext with localStorage persistence
- Toggle button in header (desktop & mobile)
- CSS variable-based theming with dark class overrides
- Affects entire site: backgrounds, text, cards, borders

### Per-Article Analytics (NEW - Completed)
- Overview: total articles, views, likes, averages, zero-view count
- Category performance chart with horizontal bars
- Sortable article table (by views/likes) with search filter
- Click-to-view article detail panel (engagement rate, code lines, steps count)
- Backend endpoints: /api/article-analytics/overview, /top-articles, /category-stats, /article/{slug}

### AI Content Rewriting (NEW - Completed)
- Uses OpenAI GPT-4o-mini via emergentintegrations (EMERGENT_LLM_KEY)
- "AI Rewrite" button in Scraper preview to convert content to 9xCodes style
- Backend endpoint: POST /api/ai-rewrite/rewrite
- Auto-switches to edit mode after rewrite for review

### Article Scraper (Completed)
- Scrape any article URL, extract title, code blocks, metadata
- Auto-detect category, difficulty, OS, tags
- Preview, edit, and save workflow
- Discover URLs from Linuxize, DigitalOcean, TecMint

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

## DB Collections
- code_snippets, comments, google_ads_config, subscribers, users, contributions, contact_messages

## Credentials
- Admin: admin / admin123

## Future/Backlog Tasks (P2)
- Moderation interface for user comments
