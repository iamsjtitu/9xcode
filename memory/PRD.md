# 9xCodes.com - Product Requirements Document

## Project Overview
**Name:** 9xCodes.com  
**Tagline:** "Solve your coding problems in 9x speed!"  
**Purpose:** A platform to post code snippets and server commands for Linux, Ubuntu, and various technical topics.

## Core Features

### Implemented ✅

#### 1. Content Management
- **Admin-only posting**: Only authenticated admins can create/edit articles
- **Article structure**: Title, description, category, OS tags, difficulty level, step-by-step tutorials with code blocks
- **Categories**: 14 main categories with subcategories
  - Installation, Configuration, Security, Networking, Database, Web Server, Monitoring, Backup, Computers, CCTV Cameras, Learning, Virtualization, Web Hosting, Billing Systems

#### 2. Navigation & Filtering
- **Category filtering**: Filter articles by category (14 categories)
- **Universal subcategories**: All main categories have subcategories for granular filtering
  - Learning: Tally, Busy, MS Excel, MS Word, PowerPoint, Photoshop
  - Computers: Windows Server, Windows, macOS
  - CCTV Cameras: CP Plus, TP-Link VIGI, Setup & Config
  - Networking: Routers, VPN, LAN Setup, WiFi
  - Virtualization: SolusVM, Virtualizor, Proxmox, VMware
  - Web Hosting: cPanel/WHM, Plesk, DirectAdmin, Reseller, Domains, SSL, Email
  - Billing Systems: WHMCS, Blesta, HostBill, FOSSBilling, Automation, Modules
  - Security, Database, Installation: Various subcategories
- **Search functionality**: Search articles by keywords
- **Sorting**: Sort by Most Recent, Most Popular, Most Viewed

#### 3. Social Features
- **Social share buttons**: Facebook, X (Twitter), WhatsApp, Telegram, Instagram on article pages
- **Like system**: Users can like articles
- **Comments**: Users can comment on articles

#### 4. Admin Panel
- **Authentication**: JWT-based login system
- **Credentials**: username: `admin`, password: `admin123`
- **Article creation**: Form to create new code snippets
- **Google Ads management**: Page to configure AdSense integration
- **Analytics Dashboard**: View site statistics, category distribution, top articles, popular tags
- **SEO & Tracking Settings**: Configure Google Analytics, GTM, Search Console, Facebook Pixel

#### 5. Security & Performance ✅
- **Rate Limiting**: API rate limiting with slowapi
- **Security Headers**: X-Content-Type-Options, X-Frame-Options, X-XSS-Protection, Referrer-Policy, Permissions-Policy
- **Response Caching**: Cache-Control headers for GET requests
- **Input Validation**: Pydantic model validation

#### 6. SEO Features ✅
- **Dynamic XML Sitemap**: Auto-generated at `/api/seo/sitemap.xml`
- **Robots.txt**: Configured at `/api/seo/robots.txt`
- **Open Graph meta tags**: For social sharing
- **Twitter Card meta tags**: For Twitter sharing
- **JSON-LD structured data**: For rich snippets in search results
- **Canonical URLs**: Prevent duplicate content
- **Google Analytics Integration**: GA4 support in admin panel
- **Google Tag Manager**: GTM support in admin panel
- **Search Console Verification**: Meta tag support
- **Facebook Pixel**: Tracking support

#### 7. UI/UX
- **Responsive design**: Mobile-friendly layout
- **Code syntax highlighting**: Code blocks with copy functionality
- **Step-by-step tutorials**: Visual step indicators with numbered steps

### Content Library
- **Total Articles**: 220+
- **Categories breakdown**:
  - Learning: 30 articles (Tally, Busy, MS Office, Excel, Word, Photoshop)
  - Networking: 26 articles (MikroTik, TP-Link, Cisco, OpenWrt, VPN, pfSense, VLAN, etc.)
  - Billing Systems: 24 articles (WHMCS, Blesta, HostBill, FOSSBilling)
  - Installation: 22 articles (Docker, Kubernetes, Jenkins, GitLab, Ansible, Terraform, Prometheus, Grafana, Redis, Elasticsearch)
  - Computers: 21 articles (Windows Server, Active Directory, DHCP, File Server)
  - Security: 16 articles (Fail2Ban, 2FA, UFW, Let's Encrypt, Nginx hardening, CSF)
  - Database: 13 articles (MySQL tuning, PostgreSQL backup, MongoDB replica set)
  - Web Server: 13 articles (Nginx load balancer, Apache virtual hosts, reverse proxy)
  - Configuration: 10 articles
  - Monitoring: 10 articles
  - Backup: 10 articles
  - Virtualization: 9 articles (SolusVM, Virtualizor, Proxmox, VMware ESXi, OpenVZ)
  - CCTV Cameras: 8 articles (Hikvision, Dahua, CP Plus)
  - Web Hosting: 8 articles (cPanel/WHM, Plesk, DirectAdmin)

## Technical Stack

### Frontend
- **Framework**: React with React Router
- **Styling**: TailwindCSS with Shadcn/UI components
- **Icons**: Lucide React
- **HTTP Client**: Axios
- **SEO**: React Helmet for meta tags

### Backend
- **Framework**: FastAPI
- **Database**: MongoDB with Motor (async driver)
- **Authentication**: JWT (python-jose, passlib)
- **Rate Limiting**: slowapi
- **Security**: Security headers middleware

### Deployment
- **Process Manager**: Supervisor
- **Ports**: Frontend: 3000, Backend: 8001

## API Endpoints

### Public
- `GET /api/snippets` - List all snippets (with filters)
- `GET /api/snippets/{slug}` - Get single snippet
- `POST /api/snippets/{slug}/like` - Like a snippet
- `GET /api/comments/{snippet_id}` - Get comments
- `POST /api/comments` - Add comment
- `GET /api/ads/config` - Get ads configuration
- `GET /api/seo/sitemap.xml` - Dynamic XML sitemap
- `GET /api/seo/robots.txt` - Robots.txt file
- `GET /api/seo/metadata/{slug}` - Article SEO metadata

### Protected (requires auth)
- `POST /api/auth/login` - Admin login
- `POST /api/snippets` - Create new snippet
- `POST /api/ads/config` - Update ads config
- `GET /api/analytics/dashboard` - Analytics dashboard data
- `GET /api/analytics/traffic` - Traffic data over time

## Admin Routes
- `/admin` - Article creation panel with quick access cards
- `/admin/analytics` - Analytics dashboard with statistics
- `/admin/seo` - SEO & tracking settings
- `/admin/ads` - Google AdSense management

## Completed Tasks
- [x] Full-stack application setup (React + FastAPI + MongoDB)
- [x] 190 articles across 14 categories
- [x] Universal subcategory filtering
- [x] Social media share buttons
- [x] Admin panel with authentication
- [x] Google Ads integration
- [x] Analytics Dashboard
- [x] SEO & Tracking Settings (GA4, GTM, Search Console, FB Pixel)
- [x] Security & Performance optimization (rate limiting, security headers, caching)
- [x] Dynamic sitemap and robots.txt
- [x] Web Hosting category with 8 articles
- [x] Billing Systems category with 24 articles

## File Structure
```
/app
├── backend/
│   ├── server.py (main FastAPI app with security middleware)
│   ├── auth.py (authentication with get_current_user)
│   ├── database.py (MongoDB connection with get_db)
│   ├── models.py (Pydantic models)
│   ├── routes/
│   │   ├── snippets.py
│   │   ├── comments.py
│   │   ├── ads.py
│   │   ├── auth.py
│   │   ├── analytics.py (NEW - dashboard stats)
│   │   └── seo.py (NEW - sitemap, robots.txt)
│   └── seed_*.py (database seeding scripts)
└── frontend/
    ├── src/
    │   ├── components/
    │   │   ├── UniversalSubcategories.jsx
    │   │   ├── SocialShare.jsx
    │   │   └── ...
    │   ├── pages/
    │   │   ├── Home.jsx
    │   │   ├── SnippetDetail.jsx
    │   │   ├── AdminPanel.jsx (with quick access cards)
    │   │   ├── AnalyticsDashboard.jsx (NEW)
    │   │   ├── SEOSettings.jsx (NEW)
    │   │   └── ...
    │   └── App.js
    └── package.json
```

## Admin Credentials
- **Username**: `admin`
- **Password**: `admin123`
