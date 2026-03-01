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
- "Made with Emergent" branding removed

### Reader Features
- Most Popular Articles on homepage
- Related Articles on article pages
- Bookmarks / Save for Later (localStorage)
- Copy Code Button (always visible)
- Tag-based Search (clickable tags)
- Table of Contents (desktop sidebar + mobile)
- Reading time estimate

### Admin Features
- Newsletter Subscribers management (/admin/subscribers)
- Bulk Article Management (/admin/articles) - select, bulk delete, bulk category change, export CSV/JSON
- Article Seeder (/admin/seeder) - seed articles by category + OS with preview
- Newsletter subscription form in footer

### Seeder
- Consolidated `seed_all.py` CLI utility
- Admin UI Seeder with templates for all 14 categories x 8 OS combinations
- Preview before seeding, duplicate detection, session history

## Key API Endpoints
- Auth: POST /api/auth/login, /api/auth/change-password
- Snippets: GET /api/snippets, /api/snippets/popular, /api/snippets/{slug}, /api/snippets/{slug}/related
- Newsletter: POST /api/newsletter/subscribe, GET /api/newsletter/subscribers, /subscribers/export, /subscribers/count
- Articles: GET /api/articles/list, POST /api/articles/bulk-delete, /api/articles/bulk-category, GET /api/articles/export
- Seeder: GET /api/seeder/categories, POST /api/seeder/preview, POST /api/seeder/seed
- Analytics: GET /api/analytics/stats, /api/analytics/dashboard

## DB Collections
- code_snippets, comments, google_ads_config, subscribers, users

## Credentials
- Admin: admin / admin123

## Pending / Backlog
- P3: Cleanup old individual seed_*.py files
- P3: Homepage articles pagination
- P3: Dark/Light mode toggle
- P3: Article search autocomplete
