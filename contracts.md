# 9xCodes Backend Integration Contracts

## API Endpoints

### 1. Code Snippets API
**Base URL:** `/api/snippets`

#### GET /api/snippets
- **Purpose:** Fetch all code snippets with filtering
- **Query Parameters:**
  - `category` (optional): Filter by category slug
  - `os` (optional): Filter by operating system
  - `difficulty` (optional): Filter by difficulty level
  - `search` (optional): Search in title, description, tags
  - `sort` (optional): "recent", "popular", "views"
  - `limit` (optional): Number of results (default: 100)
- **Response:** Array of CodeSnippet objects
- **Frontend Integration:** Update `Home.jsx` to fetch from API instead of mockData

#### GET /api/snippets/{slug}
- **Purpose:** Get single snippet by slug
- **Response:** Single CodeSnippet object
- **Frontend Integration:** Update `SnippetDetail.jsx` to fetch from API

#### POST /api/snippets
- **Purpose:** Create new code snippet (Admin only)
- **Request Body:** CodeSnippetCreate schema
- **Response:** Created CodeSnippet object
- **Frontend Integration:** Update `AdminPanel.jsx` form submission

#### POST /api/snippets/{slug}/like
- **Purpose:** Like a snippet
- **Response:** Updated likes count
- **Frontend Integration:** Update like button in `SnippetDetail.jsx`

---

### 2. Comments API
**Base URL:** `/api/comments`

#### GET /api/comments/{snippet_id}
- **Purpose:** Get all comments for a snippet
- **Response:** Array of Comment objects
- **Frontend Integration:** Update `SnippetDetail.jsx` to fetch comments

#### POST /api/comments
- **Purpose:** Create a new comment
- **Request Body:**
  ```json
  {
    "snippetId": "string",
    "user": "string",
    "text": "string"
  }
  ```
- **Response:** Created Comment object
- **Frontend Integration:** Update comment form in `SnippetDetail.jsx`

---

### 3. Google Ads API
**Base URL:** `/api/ads`

#### GET /api/ads/config
- **Purpose:** Get current Google Ads configuration
- **Response:** GoogleAdsConfig object
- **Frontend Integration:** 
  - Fetch in `App.js` on mount
  - Use in `GoogleAdsManager.jsx` to populate form

#### PUT /api/ads/config
- **Purpose:** Update Google Ads configuration
- **Request Body:**
  ```json
  {
    "enabled": boolean,
    "headerAdCode": "string (optional)",
    "sidebarAdCode": "string (optional)",
    "betweenSnippetsAdCode": "string (optional)",
    "footerAdCode": "string (optional)"
  }
  ```
- **Response:** Updated GoogleAdsConfig object
- **Frontend Integration:** Update form submission in `GoogleAdsManager.jsx`

---

## Data Models

### CodeSnippet
```javascript
{
  id: string,
  title: string,
  slug: string,
  description: string,
  category: string,
  os: string[],
  difficulty: string,
  tags: string[],
  steps: [
    {
      title: string,
      description: string,
      code: string,
      language: string
    }
  ],
  postInstallation: {
    title: string,
    content: string
  } (optional),
  views: number,
  likes: number,
  author: string,
  createdAt: datetime,
  updatedAt: datetime
}
```

### Comment
```javascript
{
  id: string,
  snippetId: string,
  user: string,
  text: string,
  createdAt: datetime
}
```

### GoogleAdsConfig
```javascript
{
  id: string,
  enabled: boolean,
  headerAdCode: string (optional),
  sidebarAdCode: string (optional),
  betweenSnippetsAdCode: string (optional),
  footerAdCode: string (optional),
  updatedAt: datetime
}
```

---

## Frontend Changes Required

### 1. Home.jsx
- Remove import of mockData
- Add useEffect to fetch snippets from API
- Use axios to call `/api/snippets` with filters
- Handle loading and error states
- Display Google Ads between snippets if enabled

### 2. SnippetDetail.jsx
- Fetch snippet data from `/api/snippets/{slug}`
- Fetch comments from `/api/comments/{snippet_id}`
- Implement like functionality with POST to `/api/snippets/{slug}/like`
- Implement comment submission with POST to `/api/comments`
- Display sidebar ads if enabled

### 3. AdminPanel.jsx
- Implement form submission to POST `/api/snippets`
- Handle success/error responses
- Show success message and redirect or reset form

### 4. GoogleAdsManager.jsx (Already Created)
- Fetch config on mount from `/api/ads/config`
- Submit updates to `/api/ads/config`
- Handle loading states

### 5. App.js (Already Updated)
- Fetch ads config on mount
- Pass adsConfig to pages as props
- Load AdSense script if ads are enabled

---

## Mock Data Removal
Once backend is integrated, remove:
- `/app/frontend/src/data/mockData.js`
- All imports from mockData in components

---

## Google Ads Integration
1. Admin configures ad codes in `/admin/ads`
2. Config stored in MongoDB
3. Frontend fetches config and conditionally renders ads
4. Ad placements:
   - Header: Top of every page
   - Sidebar: Right sidebar on desktop
   - Between Snippets: After every 3rd snippet in listing
   - Footer: Bottom of every page
