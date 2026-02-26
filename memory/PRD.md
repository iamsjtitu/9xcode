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
- **Categories**: 12 main categories with subcategories
  - Installation, Configuration, Security, Networking, Database, Web Server, Monitoring, Backup, Computers, CCTV Cameras, Learning, Virtualization

#### 2. Navigation & Filtering
- **Category filtering**: Filter articles by category
- **Universal subcategories**: All main categories have subcategories for granular filtering
  - Learning: Tally, Busy, MS Excel, MS Word, PowerPoint, Photoshop
  - Computers: Windows Server, Windows, macOS
  - CCTV Cameras: CP Plus, TP-Link VIGI, Setup & Config
  - Networking: Routers, VPN, LAN Setup, WiFi
  - Virtualization: SolusVM, Virtualizor, Proxmox, VMware
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

#### 5. UI/UX
- **Responsive design**: Mobile-friendly layout
- **Code syntax highlighting**: Code blocks with copy functionality
- **Step-by-step tutorials**: Visual step indicators with numbered steps

### Content Library
- **Total Articles**: 158
- **Categories breakdown**:
  - Networking: 26 articles (MikroTik, TP-Link, Cisco, OpenWrt, VPN, pfSense, VLAN, etc.)
  - Virtualization: 9 articles (SolusVM, Virtualizor, Proxmox, VMware ESXi, OpenVZ, WHMCS integration)
  - Learning: 25 articles (Tally, Busy, MS Office)
  - Computers: 18 articles (Windows Server 2008-2026)
  - CCTV Cameras: 6 articles
  - Other categories: Various

## Technical Stack

### Frontend
- **Framework**: React with React Router
- **Styling**: TailwindCSS with Shadcn/UI components
- **Icons**: Lucide React
- **HTTP Client**: Axios

### Backend
- **Framework**: FastAPI
- **Database**: MongoDB with Motor (async driver)
- **Authentication**: JWT (python-jose, passlib)

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

### Protected (requires auth)
- `POST /api/auth/login` - Admin login
- `POST /api/snippets` - Create new snippet
- `POST /api/ads/config` - Update ads config

## File Structure
```
/app
├── backend/
│   ├── server.py (main FastAPI app)
│   ├── auth.py (authentication logic)
│   ├── database.py (MongoDB connection)
│   ├── models.py (Pydantic models)
│   ├── routes/ (API endpoints)
│   └── seed_*.py (database seeding scripts)
└── frontend/
    ├── src/
    │   ├── components/
    │   │   ├── UniversalSubcategories.jsx
    │   │   ├── SocialShare.jsx
    │   │   ├── CodeBlock.jsx
    │   │   └── ...
    │   ├── pages/
    │   │   ├── Home.jsx
    │   │   ├── SnippetDetail.jsx
    │   │   ├── AdminPanel.jsx
    │   │   └── ...
    │   └── data/mockData.js
    └── package.json
```

## Completed Tasks (This Session)
- [x] Fixed frontend compilation errors (emoji characters causing issues)
- [x] Implemented universal subcategory filtering for all main categories
- [x] Added social media share buttons (Facebook, X, WhatsApp, Telegram, Instagram)
- [x] Added Virtualization category with subcategories (SolusVM, Virtualizor, Proxmox, VMware)
- [x] Added 10 Networking articles (Router configuration, VPN setup, etc.)
- [x] Added 9 Virtualization articles (SolusVM, Virtualizor installation and management)

## Pending Tasks

### Priority 1 (P1)
- [ ] Security & Performance optimization
  - Check for common vulnerabilities
  - Optimize loading speeds
  - Add rate limiting to APIs

### Priority 2 (P2)
- [ ] Add more Windows Server articles (2008-2026)
- [ ] Google SEO tracking implementation
- [ ] Meta tags for better SEO

### Future/Backlog
- [ ] Additional content for all categories
- [ ] Article edit/delete functionality in admin
- [ ] User registration for comments
- [ ] Analytics dashboard
