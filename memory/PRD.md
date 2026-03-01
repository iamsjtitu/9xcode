# 9xCodes.com - Product Requirements Document

## Original Problem Statement
Build a website named `www.9xcodes.com`, a platform for posting code snippets and server commands.

## Core Requirements
- **Admin-Only Content**: Only admin can post new articles
- **Admin Authentication**: Secure username/password login
- **Password Management**: Admin can change password
- **Content Categories**: Computers, CCTV, Networking, Learning, Virtualization, Web Hosting, Billing Systems + Installation, Configuration, Security, Database, Monitoring, Backup, Web Server
- **Content Population**: Pre-populated with 237+ articles
- **Social Sharing**: Social media share buttons on article pages
- **SEO & Tracking**: Sitemaps, robots.txt, Analytics/Adsense admin interface
- **Site Optimization**: Security headers and speed optimization
- **Branding**: 9xCodes logo with tagline "solve your coding problems in 9x speed!"
- **Admin Analytics**: Analytics dashboard for admin

## Tech Stack
- **Frontend**: React, React Router, TailwindCSS, Shadcn UI, Axios
- **Backend**: FastAPI, Pydantic, Motor, Passlib
- **Database**: MongoDB
- **Deployment**: Nginx, PM2, Certbot (SSL), Ubuntu VPS

## What's Been Implemented (Complete)
### Core Features
- Full-stack application (React + FastAPI + MongoDB)
- Admin panel with stats dashboard
- 237+ articles across 14 categories
- Social sharing buttons (Facebook, Twitter, WhatsApp, Telegram, Instagram)
- SEO features (sitemap, robots.txt, JSON-LD structured data)
- VPS deployment with SSL (9xcodes.com)
- Automatic daily MongoDB backups
- Public analytics stats endpoint
- "Made with Emergent" branding removed

### Session 2 Features (March 2026)
- Most Popular Articles section on homepage (top 6 by views)
- Related Articles on article detail pages (by category/tags)
- Bookmarks / Save for Later (localStorage based)
- Copy Code Button always visible with green animation
- Tag-based Search (clickable tags filter articles)
- Table of Contents (desktop sidebar + mobile card)
- Reading time estimate on articles
- Consolidated seed_all.py seeder utility

### Session 3 Features (March 2026)
- **Newsletter Subscription** - Email collection in footer + homepage CTA
- **Subscribers Admin** - /admin/subscribers page with search, delete, CSV export
- **Bulk Article Management** - /admin/articles with:
  - Select multiple articles
  - Bulk delete
  - Bulk category change
  - Export as CSV or JSON
  - Search and category filter
  - Pagination (20 per page)

## Key API Endpoints
### Auth
- `POST /api/auth/login` - Admin login
- `POST /api/auth/change-password` - Change admin password

### Snippets
- `GET /api/snippets` - List snippets with filters
- `GET /api/snippets/popular` - Top viewed articles
- `GET /api/snippets/{slug}` - Single article
- `GET /api/snippets/{slug}/related` - Related articles
- `POST /api/snippets` - Create article
- `DELETE /api/snippets/{slug}` - Delete article

### Newsletter
- `POST /api/newsletter/subscribe` - Subscribe email
- `GET /api/newsletter/subscribers` - List (paginated, searchable)
- `GET /api/newsletter/subscribers/export` - Export CSV
- `GET /api/newsletter/subscribers/count` - Count
- `DELETE /api/newsletter/subscribers/{email}` - Remove

### Articles Management
- `GET /api/articles/list` - Paginated list with search/filter
- `POST /api/articles/bulk-delete` - Bulk delete by slugs
- `POST /api/articles/bulk-category` - Bulk change category
- `GET /api/articles/export?format=csv|json` - Export

### Other
- `GET /api/analytics/stats` - Public stats
- `GET /api/analytics/dashboard` - Admin dashboard

## DB Collections
- `code_snippets` - Articles/tutorials
- `comments` - Article comments
- `google_ads_config` - AdSense configuration
- `subscribers` - Newsletter subscribers
- `users` - Admin users

## Credentials
- Admin URL: https://9xcodes.com/login
- Username: admin
- Password: admin123

## Pending / Backlog
- P3: Cleanup old individual seed_*.py files from repo
- P3: Add pagination for main articles list on homepage
- P3: Dark/Light mode toggle
- P3: Article search autocomplete suggestions
