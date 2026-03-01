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
- 237+ articles across 14 categories
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
- **Search Autocomplete** - Real-time suggestions with keyword highlighting, category labels, keyboard navigation (↑↓ Enter Escape)

### Admin Features
- Newsletter Subscribers management (/admin/subscribers)
- Bulk Article Management (/admin/articles)
- Article Seeder (/admin/seeder) - 14 categories x 8 OS templates
- Newsletter subscription form in footer

## Key API Endpoints
- `GET /api/snippets/search-suggestions?q=` - Autocomplete suggestions (max 8)
- `GET /api/snippets/popular` - Top viewed articles
- `GET /api/snippets/{slug}/related` - Related articles
- `POST /api/seeder/preview` / `POST /api/seeder/seed` - Article seeder
- `POST /api/newsletter/subscribe` - Newsletter
- `POST /api/articles/bulk-delete` / `POST /api/articles/bulk-category` - Bulk ops

## Credentials
- Admin: admin / admin123

## Pending / Backlog
- P3: Cleanup old individual seed_*.py files
- P3: Homepage articles pagination
- P3: Dark/Light mode toggle
- P3: Per-article analytics view
