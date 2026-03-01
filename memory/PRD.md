# 9xCodes.com - Product Requirements Document

## Original Problem Statement
Build a website named `www.9xcodes.com`, a platform for posting code snippets and server commands.

## Core Requirements
- **Admin-Only Content**: Only admin can post new articles
- **Admin Authentication**: Secure username/password login
- **Password Management**: Admin can change password
- **Content Categories**: Computers, CCTV, Networking, Learning, Virtualization, Web Hosting, Billing Systems
- **Content Population**: Pre-populated with 250+ articles
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

## What's Been Implemented
- Full-stack application (React + FastAPI + MongoDB)
- Admin panel with stats dashboard
- 250+ articles across all categories
- Social sharing buttons
- SEO features (sitemap, robots.txt)
- VPS deployment with SSL
- Automatic daily MongoDB backups
- Public analytics stats endpoint

## Completed Tasks (This Session - March 2026)
- Removed "Made with Emergent" branding from index.html (title, description, badge, script)

## Pending / Backlog
- P1: Verify "Change Password" feature (untested)
- P2: Debug and consolidate seed_master.py
- P2: Refactor multiple seed_*.py into single robust seeder

## Credentials
- Admin URL: https://9xcodes.com/login
- Username: admin
- Password: admin123

## Key Files
- `/app/frontend/public/index.html` - Updated (branding removed)
- `/app/frontend/src/pages/AdminPanel.jsx` - Admin dashboard
- `/app/backend/routes/analytics.py` - Public stats endpoint
- `/app/DEPLOYMENT_GUIDE.md` - VPS deployment guide
