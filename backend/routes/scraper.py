from fastapi import APIRouter, HTTPException
from database import snippets_collection
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime, timezone
import uuid, re, requests
from bs4 import BeautifulSoup

router = APIRouter(prefix="/scraper", tags=["scraper"])

OPEN_SOURCES = [
    {"name": "Linuxize", "base": "https://linuxize.com", "list_url": "https://linuxize.com/post/", "selector": "article.post", "title_sel": "h1", "content_sel": ".post-content"},
    {"name": "LinuxHint", "base": "https://linuxhint.com", "list_url": "https://linuxhint.com/category/linux/", "selector": "div.post-item", "title_sel": "h1.title", "content_sel": "div.post-content"},
]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

def create_slug(title):
    s = re.sub(r'[^a-z0-9]+', '-', title.lower())
    return s.strip('-')

def detect_category(title, text):
    title_lower = (title + " " + text).lower()
    mapping = [
        ('docker', 'virtualization'), ('container', 'virtualization'), ('vm', 'virtualization'), ('kvm', 'virtualization'),
        ('nginx', 'web-server'), ('apache', 'web-server'), ('caddy', 'web-server'),
        ('mysql', 'database'), ('postgres', 'database'), ('mongo', 'database'), ('redis', 'database'), ('mariadb', 'database'),
        ('firewall', 'security'), ('ssl', 'security'), ('ufw', 'security'), ('iptables', 'security'), ('encrypt', 'security'),
        ('install', 'installation'), ('setup', 'installation'),
        ('backup', 'backup'), ('rsync', 'backup'), ('cron', 'backup'),
        ('monitor', 'monitoring'), ('prometheus', 'monitoring'), ('grafana', 'monitoring'), ('nagios', 'monitoring'),
        ('network', 'networking'), ('dns', 'networking'), ('ip ', 'networking'), ('vpn', 'networking'), ('ssh', 'networking'),
        ('deploy', 'web-hosting'), ('hosting', 'web-hosting'), ('pm2', 'web-hosting'),
        ('config', 'configuration'), ('conf', 'configuration'), ('setting', 'configuration'),
        ('cctv', 'cctv-cameras'), ('camera', 'cctv-cameras'),
        ('billing', 'billing'), ('invoice', 'billing'), ('whmcs', 'billing'),
        ('git', 'learning'), ('bash', 'learning'), ('linux', 'learning'), ('command', 'learning'),
    ]
    for keyword, cat in mapping:
        if keyword in title_lower:
            return cat
    return 'learning'

def detect_difficulty(text):
    text_lower = text.lower()
    advanced_keywords = ['advanced', 'complex', 'production', 'cluster', 'replication', 'high availability']
    beginner_keywords = ['basic', 'beginner', 'getting started', 'introduction', 'simple', 'first']
    for kw in advanced_keywords:
        if kw in text_lower:
            return 'advanced'
    for kw in beginner_keywords:
        if kw in text_lower:
            return 'beginner'
    return 'intermediate'

def detect_os(text):
    text_lower = text.lower()
    os_list = []
    os_map = {'ubuntu': 'ubuntu', 'debian': 'debian', 'centos': 'centos', 'rhel': 'rhel', 'fedora': 'fedora', 'windows': 'windows', 'macos': 'mac'}
    for keyword, os_slug in os_map.items():
        if keyword in text_lower:
            os_list.append(os_slug)
    return os_list if os_list else ['linux']

def extract_tags(title, text):
    combined = (title + " " + text).lower()
    all_tags = ['docker', 'nginx', 'apache', 'mysql', 'postgresql', 'mongodb', 'redis', 'python', 'nodejs',
                'git', 'ssh', 'ssl', 'firewall', 'ufw', 'backup', 'cron', 'systemd', 'bash', 'linux',
                'ubuntu', 'centos', 'debian', 'vim', 'nano', 'curl', 'wget', 'tar', 'zip', 'dns',
                'php', 'java', 'golang', 'rust', 'pm2', 'certbot', 'letsencrypt', 'kubernetes', 'k8s']
    found = [t for t in all_tags if t in combined]
    return found[:8]

def parse_article_to_steps(soup, content_sel):
    """Parse article HTML into 9xCodes step format"""
    content = soup.select_one(content_sel)
    if not content:
        content = soup.select_one('article') or soup.select_one('.content') or soup.select_one('main')
    if not content:
        return []

    steps = []
    current_title = ""
    current_desc = ""
    current_code = ""

    for element in content.find_all(['h2', 'h3', 'p', 'pre', 'code', 'ol', 'ul']):
        tag = element.name

        if tag in ('h2', 'h3'):
            # Save previous step
            if current_title and current_code:
                steps.append({
                    'title': current_title.strip(),
                    'description': current_desc.strip(),
                    'code': current_code.strip(),
                    'language': 'bash'
                })
            current_title = element.get_text(strip=True)
            current_desc = ""
            current_code = ""

        elif tag == 'p':
            text = element.get_text(strip=True)
            if text:
                current_desc += text + " "

        elif tag in ('pre', 'code'):
            code_text = element.get_text(strip=True)
            if code_text and len(code_text) > 3:
                if current_code:
                    current_code += "\n" + code_text
                else:
                    current_code = code_text

        elif tag in ('ol', 'ul'):
            for li in element.find_all('li'):
                li_text = li.get_text(strip=True)
                if li_text:
                    current_desc += "- " + li_text + " "

    # Save last step
    if current_title and current_code:
        steps.append({
            'title': current_title.strip(),
            'description': current_desc.strip(),
            'code': current_code.strip(),
            'language': 'bash'
        })

    # If no structured steps found, create one big step
    if not steps and content:
        all_code = []
        all_text = []
        for el in content.find_all(['pre', 'code']):
            code = el.get_text(strip=True)
            if code and len(code) > 5:
                all_code.append(code)
        for el in content.find_all('p'):
            text = el.get_text(strip=True)
            if text:
                all_text.append(text)
        if all_code:
            steps.append({
                'title': 'Commands',
                'description': ' '.join(all_text[:3]),
                'code': '\n'.join(all_code[:5]),
                'language': 'bash'
            })

    return steps[:10]  # Max 10 steps

class ScrapeURLRequest(BaseModel):
    url: str

class ScrapeBulkRequest(BaseModel):
    urls: List[str]

@router.post("/from-url")
async def scrape_from_url(req: ScrapeURLRequest):
    """Scrape a single URL and convert to 9xCodes format"""
    try:
        resp = requests.get(req.url, headers=HEADERS, timeout=15)
        resp.raise_for_status()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to fetch URL: {str(e)}")

    soup = BeautifulSoup(resp.text, 'html.parser')

    # Extract title
    title = ""
    for sel in ['h1', 'title', '.post-title', '.entry-title', '.article-title']:
        el = soup.select_one(sel)
        if el:
            title = el.get_text(strip=True)
            break
    if not title:
        raise HTTPException(status_code=400, detail="Could not extract title from page")

    # Extract description
    desc = ""
    meta_desc = soup.find('meta', attrs={'name': 'description'})
    if meta_desc:
        desc = meta_desc.get('content', '')
    if not desc:
        first_p = soup.find('p')
        if first_p:
            desc = first_p.get_text(strip=True)[:200]

    # Parse steps
    steps = parse_article_to_steps(soup, '.post-content, .entry-content, .article-content, article, .content, main')
    if not steps:
        raise HTTPException(status_code=400, detail="Could not extract code steps from this article")

    full_text = soup.get_text()
    article = {
        'id': str(uuid.uuid4()),
        'title': title,
        'slug': create_slug(title),
        'description': desc[:300],
        'category': detect_category(title, full_text),
        'difficulty': detect_difficulty(full_text),
        'os': detect_os(full_text),
        'tags': extract_tags(title, full_text),
        'steps': steps,
        'author': 'Admin',
        'views': 0,
        'likes': 0,
        'createdAt': datetime.now(timezone.utc).isoformat(),
        'updatedAt': datetime.now(timezone.utc).isoformat(),
        'postInstallation': None,
        'source_url': req.url,
    }

    # Check duplicate
    existing = await snippets_collection.find_one({'title': title})
    is_duplicate = existing is not None

    return {
        "article": {
            'title': article['title'],
            'description': article['description'],
            'category': article['category'],
            'difficulty': article['difficulty'],
            'os': article['os'],
            'tags': article['tags'],
            'steps_count': len(article['steps']),
            'steps': article['steps'],
            'source_url': req.url,
        },
        "is_duplicate": is_duplicate,
        "full_article": article,
    }

@router.post("/save")
async def save_scraped_article(article: dict):
    """Save a scraped article to database"""
    if not article.get('title') or not article.get('steps'):
        raise HTTPException(status_code=400, detail="Article must have title and steps")
    
    existing = await snippets_collection.find_one({'title': article['title']})
    if existing:
        raise HTTPException(status_code=409, detail="Article with this title already exists")
    
    # Ensure required fields
    article.setdefault('id', str(uuid.uuid4()))
    article.setdefault('slug', create_slug(article['title']))
    article.setdefault('views', 0)
    article.setdefault('likes', 0)
    article.setdefault('author', 'Admin')
    article.setdefault('createdAt', datetime.now(timezone.utc).isoformat())
    article.setdefault('updatedAt', datetime.now(timezone.utc).isoformat())
    article.setdefault('postInstallation', None)
    
    await snippets_collection.insert_one(article)
    return {"message": "Article saved!", "slug": article['slug']}

@router.post("/discover")
async def discover_articles(source: str = "linuxize"):
    """Discover article URLs from open source sites"""
    urls_found = []
    
    sites_to_scrape = {
        "linuxize": [
            "https://linuxize.com/post/how-to-install-nginx-on-ubuntu-22-04/",
            "https://linuxize.com/post/how-to-install-docker-on-ubuntu-22-04/",
            "https://linuxize.com/post/how-to-install-mysql-on-ubuntu-22-04/",
            "https://linuxize.com/post/how-to-set-up-ssh-keys-on-ubuntu-22-04/",
            "https://linuxize.com/post/how-to-install-node-js-on-ubuntu-22-04/",
            "https://linuxize.com/post/how-to-install-and-use-docker-compose-on-ubuntu-22-04/",
            "https://linuxize.com/post/how-to-configure-static-ip-address-on-ubuntu-22-04/",
            "https://linuxize.com/post/how-to-install-postgresql-on-ubuntu-22-04/",
            "https://linuxize.com/post/how-to-install-and-configure-redis-on-ubuntu-22-04/",
            "https://linuxize.com/post/how-to-install-python-3-10-on-ubuntu-22-04/",
        ],
        "misc": [
            "https://www.digitalocean.com/community/tutorials/how-to-install-nginx-on-ubuntu-22-04",
            "https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-ubuntu-22-04",
            "https://www.digitalocean.com/community/tutorials/initial-server-setup-with-ubuntu-22-04",
            "https://www.digitalocean.com/community/tutorials/how-to-set-up-a-firewall-with-ufw-on-ubuntu-22-04",
            "https://www.digitalocean.com/community/tutorials/how-to-install-mysql-on-ubuntu-22-04",
        ]
    }
    
    urls = sites_to_scrape.get(source, sites_to_scrape["linuxize"])
    return {"source": source, "urls": urls, "count": len(urls)}
