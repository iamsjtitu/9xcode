from fastapi import APIRouter, Response
from fastapi.responses import PlainTextResponse
from database import get_db
from datetime import datetime, timezone
import os
import html

router = APIRouter(prefix="/seo", tags=["seo"])

SITE_URL = "https://9xcodes.com"

@router.get("/sitemap.xml", response_class=PlainTextResponse)
async def get_sitemap():
    """Generate dynamic XML sitemap"""
    db = await get_db()
    
    # Get all articles
    articles = await db.code_snippets.find(
        {},
        {"_id": 0, "slug": 1, "updatedAt": 1, "category": 1}
    ).to_list(1000)
    
    # Build sitemap XML
    xml_content = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml_content += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    
    # Homepage
    xml_content += f'''  <url>
    <loc>{SITE_URL}/</loc>
    <changefreq>daily</changefreq>
    <priority>1.0</priority>
  </url>\n'''
    
    # Static pages
    static_pages = [
        ("/about", "monthly", "0.7"),
        ("/contact", "monthly", "0.7"),
        ("/contribute", "monthly", "0.6"),
        ("/privacy-policy", "yearly", "0.4"),
        ("/terms-of-service", "yearly", "0.4"),
        ("/disclaimer", "yearly", "0.4"),
    ]
    for path, freq, priority in static_pages:
        xml_content += f'''  <url>
    <loc>{SITE_URL}{path}</loc>
    <changefreq>{freq}</changefreq>
    <priority>{priority}</priority>
  </url>\n'''

    # Categories
    categories = set([a.get("category") for a in articles if a.get("category")])
    for category in categories:
        xml_content += f'''  <url>
    <loc>{SITE_URL}/?category={category}</loc>
    <changefreq>daily</changefreq>
    <priority>0.8</priority>
  </url>\n'''
    
    # Individual articles
    for article in articles:
        slug = article.get("slug", "")
        updated = article.get("updatedAt", datetime.now(timezone.utc))
        if isinstance(updated, datetime):
            lastmod = updated.strftime("%Y-%m-%d")
        else:
            lastmod = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        
        xml_content += f'''  <url>
    <loc>{SITE_URL}/snippet/{slug}</loc>
    <lastmod>{lastmod}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.7</priority>
  </url>\n'''
    
    xml_content += '</urlset>'
    
    return Response(
        content=xml_content,
        media_type="application/xml",
        headers={"Cache-Control": "public, max-age=3600"}
    )

@router.get("/robots.txt", response_class=PlainTextResponse)
async def get_robots():
    """Generate robots.txt"""
    robots_content = f"""# robots.txt for 9xCodes
User-agent: *
Allow: /
Disallow: /admin
Disallow: /login
Disallow: /api/

# Sitemap
Sitemap: {SITE_URL}/api/seo/sitemap.xml

# RSS Feed
# {SITE_URL}/api/seo/rss.xml

# Crawl-delay
Crawl-delay: 1
"""
    return PlainTextResponse(
        content=robots_content,
        headers={"Cache-Control": "public, max-age=86400"}
    )

@router.get("/metadata/{slug}")
async def get_article_metadata(slug: str):
    """Get SEO metadata for a specific article"""
    db = await get_db()
    
    article = await db.code_snippets.find_one(
        {"slug": slug},
        {"_id": 0, "title": 1, "description": 1, "category": 1, "tags": 1, "author": 1, "createdAt": 1}
    )
    
    if not article:
        return {"error": "Article not found"}
    
    return {
        "title": f"{article.get('title')} | 9xCodes",
        "description": article.get("description", "")[:160],
        "keywords": ", ".join(article.get("tags", [])),
        "author": article.get("author", "9xCodes"),
        "publishedTime": article.get("createdAt"),
        "category": article.get("category"),
        "url": f"{SITE_URL}/snippet/{slug}",
        "og": {
            "type": "article",
            "title": article.get("title"),
            "description": article.get("description", "")[:200],
            "url": f"{SITE_URL}/snippet/{slug}",
            "site_name": "9xCodes"
        }
    }

@router.get("/rss.xml")
async def get_rss_feed():
    """Generate RSS 2.0 feed for articles"""
    db = await get_db()
    
    articles = await db.code_snippets.find(
        {},
        {"_id": 0, "title": 1, "slug": 1, "description": 1, "category": 1, "author": 1, "createdAt": 1, "tags": 1}
    ).sort("createdAt", -1).to_list(50)
    
    now = datetime.now(timezone.utc).strftime("%a, %d %b %Y %H:%M:%S +0000")
    
    items = ""
    for a in articles:
        title = html.escape(a.get("title", ""))
        desc = html.escape(a.get("description", ""))
        slug = a.get("slug", "")
        author = html.escape(a.get("author", "Admin"))
        category = html.escape(a.get("category", ""))
        created = a.get("createdAt")
        if isinstance(created, datetime):
            pub_date = created.strftime("%a, %d %b %Y %H:%M:%S +0000")
        elif isinstance(created, str):
            try:
                dt = datetime.fromisoformat(created.replace("Z", "+00:00"))
                pub_date = dt.strftime("%a, %d %b %Y %H:%M:%S +0000")
            except:
                pub_date = now
        else:
            pub_date = now
        
        tags_xml = ""
        for tag in a.get("tags", []):
            tags_xml += f"      <category>{html.escape(tag)}</category>\n"
        
        items += f"""    <item>
      <title>{title}</title>
      <link>{SITE_URL}/snippet/{slug}</link>
      <guid isPermaLink="true">{SITE_URL}/snippet/{slug}</guid>
      <description>{desc}</description>
      <author>{author}</author>
      <category>{category}</category>
{tags_xml}      <pubDate>{pub_date}</pubDate>
    </item>
"""
    
    rss_xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
  <channel>
    <title>9xCodes - Solve Your Coding Problems in 9x Speed</title>
    <link>{SITE_URL}</link>
    <description>Code snippets, server commands, and tutorials for Linux, networking, databases, and more.</description>
    <language>en</language>
    <lastBuildDate>{now}</lastBuildDate>
    <atom:link href="{SITE_URL}/api/seo/rss.xml" rel="self" type="application/rss+xml"/>
    <image>
      <url>{SITE_URL}/favicon.ico</url>
      <title>9xCodes</title>
      <link>{SITE_URL}</link>
    </image>
{items}  </channel>
</rss>"""
    
    return Response(
        content=rss_xml,
        media_type="application/rss+xml",
        headers={"Cache-Control": "public, max-age=3600"}
    )
