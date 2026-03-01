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
- **Site Optimization**: Security and speed optimization
- **Branding**: 9xCodes logo with tagline "solve your coding problems in 9x speed!"
- **Admin Analytics**: Analytics dashboard for admin

## Tech Stack
- **Frontend**: React, React Router, TailwindCSS, Shadcn UI, Axios
- **Backend**: FastAPI, Pydantic, Motor, Passlib
- **Database**: MongoDB
- **Deployment**: Nginx, PM2, Certbot (SSL), Ubuntu VPS

## What's Been Implemented (Complete)
- Full-stack application (React + FastAPI + MongoDB)
- Admin panel with stats dashboard
- 237+ articles across all categories
- Social sharing buttons
- SEO features (sitemap, robots.txt)
- VPS deployment with SSL
- Automatic daily MongoDB backups
- Public analytics stats endpoint
- "Made with Emergent" branding removed
- Most Popular Articles section on homepage
- Related Articles on article detail pages
- Bookmarks / Save for Later (localStorage based)
- Copy Code Button always visible with animation
- Tag-based Search (clickable tags on articles)
- Table of Contents (desktop sidebar + mobile card)
- Reading time estimate on articles
- Consolidated seed_all.py seeder utility

## Key API Endpoints
- `POST /api/auth/login` - Admin login
- `POST /api/auth/change-password` - Change admin password
- `GET /api/snippets` - List snippets with filters
- `GET /api/snippets/popular` - Top viewed articles
- `GET /api/snippets/{slug}` - Single article
- `GET /api/snippets/{slug}/related` - Related articles
- `GET /api/analytics/stats` - Public stats
- `GET /api/analytics/dashboard` - Admin dashboard

## Credentials
- Admin URL: https://9xcodes.com/login
- Username: admin
- Password: admin123

## Pending / Backlog
- P2: Debug old seed_master.py (low priority since seed_all.py works)
- P2: Cleanup old individual seed_*.py files from repo
- P3: Pagination for articles list (currently limited to 100)
