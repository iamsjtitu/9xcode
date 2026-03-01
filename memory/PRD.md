# 9xCodes.com - Product Requirements Document

## Original Problem Statement
Build a website named `www.9xcodes.com`, a platform for posting code snippets and server commands.

## Tech Stack
- **Frontend**: React, React Router, TailwindCSS, Shadcn UI, Axios
- **Backend**: FastAPI, Pydantic, Motor, Passlib
- **Database**: MongoDB
- **Deployment**: Nginx, PM2, Certbot (SSL), Ubuntu VPS

## What's Been Implemented (Complete)
### Core Features
- Full-stack app (React + FastAPI + MongoDB) - Live at 9xcodes.com
- Admin panel with stats dashboard, password change
- 245+ articles across 14 categories
- Social sharing, SEO (sitemap, robots.txt, JSON-LD)
- Automatic daily MongoDB backups

### Reader Features
- Most Popular Articles on homepage
- Related Articles on article pages
- Bookmarks / Save for Later (localStorage)
- Copy Code Button (always visible)
- Tag-based Search (clickable tags)
- Table of Contents (desktop sidebar + mobile)
- Reading time estimate
- Search Autocomplete (debounced, highlighted, keyboard nav)
- **Homepage Pagination** (12 per page, numbered pages, smooth scroll)

### Admin Features
- Newsletter Subscribers management (/admin/subscribers)
- Bulk Article Management (/admin/articles)
- Article Seeder (/admin/seeder) - 14 categories x 8 OS templates
- Newsletter subscription form in footer

### Codebase Cleanup
- Consolidated 18 individual seed_*.py files into seed_all.py + admin UI seeder
- Only seed_all.py and seed_data.py remain

## Key API Endpoints
- `GET /api/snippets?page=1&limit=12` - Paginated articles (returns {snippets, total, page, pages})
- `GET /api/snippets/search-suggestions?q=` - Autocomplete
- `GET /api/snippets/popular` - Top viewed
- `GET /api/snippets/{slug}/related` - Related articles
- `POST /api/seeder/seed` - Seed articles by category+OS
- `POST /api/newsletter/subscribe` - Newsletter
- `POST /api/articles/bulk-delete` / `bulk-category` - Bulk ops
- `GET /api/articles/export?format=csv|json` - Export

## Credentials
- Admin: admin / admin123

## Pending / Backlog
- P3: Dark/Light mode toggle
- P3: Per-article analytics view
