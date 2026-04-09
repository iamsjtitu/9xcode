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
- 278+ articles, Dark/Light mode toggle
- Social sharing, SEO (sitemap, robots.txt, JSON-LD, RSS feed)
- Google AdSense integration

### Reader Features
- Most Popular, Related Articles, Bookmarks, Copy Code, Search Autocomplete
- Table of Contents, Reading time, Homepage Pagination

### Public Pages
- Home (/), About (/about), Contact (/contact), Contribute (/contribute)
- **Privacy Policy** (/privacy-policy) - AdSense compliant
- **Terms of Service** (/terms-of-service) - AdSense compliant
- **Disclaimer** (/disclaimer) - AdSense compliant

### Admin Features
- Newsletter (/admin/subscribers), Bulk Articles (/admin/articles)
- Contributions (/admin/contributions), Messages (/admin/messages)
- Article Scraper (/admin/scraper) - curl_cffi for Cloudflare bypass + AI Rewrite
- Per-Article Analytics (/admin/per-article-analytics)
- One-Click VPS Update (update_script.sh)

### SEO
- Dynamic sitemap.xml with all pages (static + articles)
- robots.txt, RSS feed, meta tags via react-helmet
- JSON-LD structured data, ads.txt

## Credentials
- Admin: admin / admin123

## VPS Info
- Path: /var/www/9xcodes, Venv: backend/venv
- New packages: curl_cffi, cloudscraper (pip install)

## Future/Backlog (P2)
- User comment moderation
- More unique content for AdSense approval
