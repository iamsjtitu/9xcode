# 9xCodes.com - Product Requirements Document

## Original Problem Statement
Build a website named `www.9xcodes.com`, a platform for posting code snippets and server commands.

## Tech Stack
- **Frontend**: React, React Router, TailwindCSS, Shadcn UI, Axios, react-helmet
- **Backend**: FastAPI, Pydantic, Motor, Passlib, BeautifulSoup4, curl_cffi, emergentintegrations, litellm
- **Database**: MongoDB
- **Deployment**: Nginx, PM2, Certbot (SSL), Ubuntu VPS at /var/www/9xcodes

## All Implemented Features

### Core
- Full-stack app live at 9xcodes.com
- Admin panel with dashboard, password change
- 289+ articles, Dark/Light mode toggle
- Social sharing, SEO (sitemap, robots.txt, JSON-LD, RSS feed)

### Monetization
- **Adsterra Ads** (replaced Google AdSense):
  - Native Banner (between articles on homepage, in article pages)
  - Banner 728x90 (header, footer desktop, after article intro)
  - Banner 300x250 (sidebar, footer mobile)
- Google AdSense config still available via admin panel (legacy)

### Content Quality (for ad network approval)
- Rich Article Structure: Introduction (200+ words), Prerequisites, Detailed Steps, FAQs, Conclusion, TL;DR Summary
- FAQ Schema (JSON-LD) for Google FAQ rich snippets
- Article Schema (JSON-LD) TechArticle structured data
- "Last Updated" date display
- Enhanced About Us page with quality standards, stats, CTA

### AI Integration (Dual-mode)
- On Emergent platform: EMERGENT_LLM_KEY via emergentintegrations
- On VPS: Direct OPENAI_API_KEY via litellm (GPT-4o-mini)
- JSON mode enforced, retry logic, auto-stop on failures

### Admin Features
- Article Scraper with AI Tools
- Bulk AI Optimize with rich content prompt
- Per-Article Analytics, Newsletter, Contributions, Messages
- One-Click VPS Update with manual fallback

## DB Schema
- `code_snippets`: title, slug, description, category, os, difficulty, tags, steps, introduction, prerequisites, faqs, conclusion, summary, seo_keywords, ai_optimized, views, likes, author, createdAt, updatedAt

## Credentials
- Admin: admin / admin123
- OPENAI_API_KEY in backend/.env
- EMERGENT_LLM_KEY in backend/.env

## Completed (Apr 22, 2026)
- Fixed AI on VPS (Emergent key external access denied → added direct OpenAI support)
- Upgraded AI prompt for long-form content (intro, prereqs, FAQ, conclusion)
- Added JSON-LD schemas (FAQPage + TechArticle)
- Enhanced About Us page
- Integrated Adsterra ads (native, 728x90, 300x250)
- Reset all 289 articles for re-optimization

## Future/Backlog
- (P1) Re-optimize 289 articles via Bulk Optimize on VPS
- (P2) User comment moderation
- (P2) Content Quality Score dashboard
