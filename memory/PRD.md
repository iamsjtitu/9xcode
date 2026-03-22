# 9xCodes.com - Product Requirements Document

## Original Problem Statement
Build a website named `www.9xcodes.com`, a platform for posting code snippets and server commands.

## Tech Stack
- **Frontend**: React, React Router, TailwindCSS, Shadcn UI, Axios
- **Backend**: FastAPI, Pydantic, Motor, Passlib, BeautifulSoup4
- **Database**: MongoDB
- **Deployment**: Nginx, PM2, Certbot (SSL), Ubuntu VPS

## What's Been Implemented (Complete)

### Core Features
- Full-stack app live at 9xcodes.com
- Admin panel with stats dashboard, password change
- 245+ articles across 14 categories
- Social sharing, SEO (sitemap, robots.txt, JSON-LD, RSS feed)

### Reader Features
- Most Popular Articles, Related Articles, Bookmarks, Copy Code Button
- Tag-based Search, Table of Contents, Reading time, Search Autocomplete
- Homepage Pagination (12 per page)

### Pages
- About Us (/about) - Mission, offerings, community, values
- Contact Us (/contact) - Contact form with name, email, subject, message
- Contribute (/contribute) - Article submission form for community contributors

### Admin Features
- Newsletter Subscribers (/admin/subscribers)
- Bulk Article Management (/admin/articles)
- Article Seeder (/admin/seeder)
- Contributions Manager (/admin/contributions) - Review, approve/reject user-submitted articles
- Contact Messages (/admin/messages) - View and manage contact form submissions
- **Article Scraper** (/admin/scraper) - Scrape articles from external websites and save in 9xCodes format
- RSS Feed at /api/seo/rss.xml
- Google AdSense integration with admin config

### Article Scraper (NEW - Completed)
- Scrape any article URL, extract title, code blocks, metadata
- Auto-detect category, difficulty, OS, tags from content
- Preview scraped article before saving
- Edit mode to modify title, description, category, tags, steps before saving
- Discover feature to browse URLs from Linuxize, DigitalOcean, TecMint
- Duplicate detection (warns if article title already exists)
- Save directly to database in 9xCodes format

### Contributor System
- Users submit articles via /contribute (public)
- Submitted articles stored as "pending" in DB
- Admin reviews in /admin/contributions
- Approve: publishes article to website
- Reject: marks as rejected

## Key API Endpoints
- Snippets: GET /api/snippets, /popular, /search-suggestions, /{slug}, /{slug}/related
- Newsletter: POST /api/newsletter/subscribe, GET /subscribers, /export
- Articles: GET /api/articles/list, POST /bulk-delete, /bulk-category, GET /export
- Seeder: GET /api/seeder/categories, POST /preview, /seed
- Contributions: POST /api/contributions/submit, GET /contributions, POST /{id}/approve, /{id}/reject
- Contact: POST /api/contact, GET /api/contact/messages
- SEO: GET /api/seo/sitemap.xml, /robots.txt, /rss.xml
- **Scraper**: POST /api/scraper/from-url, POST /api/scraper/save, POST /api/scraper/discover

## DB Collections
- code_snippets, comments, google_ads_config, subscribers, users, contributions, contact_messages

## Credentials
- Admin: admin / admin123

## Upcoming Tasks (P1)
- Dark/Light mode toggle
- Per-article analytics view in admin panel

## Future/Backlog Tasks (P2)
- Moderation interface for user comments
