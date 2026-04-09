from fastapi import APIRouter, HTTPException, Body
from database import snippets_collection
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime, timezone
import uuid, re, requests
from bs4 import BeautifulSoup

try:
    import cloudscraper
    HAS_CLOUDSCRAPER = True
except ImportError:
    HAS_CLOUDSCRAPER = False

router = APIRouter(prefix="/scraper", tags=["scraper"])

HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "Connection": "keep-alive",
}

CONTENT_SELECTORS = [
    'article .post-content', 'article .entry-content', '.post-content',
    '.entry-content', '.article-content', '.article-body', '.content-body',
    '.tutorial-content', '.markdown-body', '.single-post-content',
    '.wp-block-post-content', '.kb-content', '.blog-content',
    'article', '.content', 'main',
    '#content', '#main-content', '.post', '.blog-post',
]


def create_slug(title):
    s = re.sub(r'[^a-z0-9]+', '-', title.lower())
    return s.strip('-')


def detect_category(title, text):
    title_lower = (title + " " + text[:2000]).lower()
    mapping = [
        ('docker', 'virtualization'), ('container', 'virtualization'), ('vm', 'virtualization'), ('kvm', 'virtualization'), ('virtualbox', 'virtualization'),
        ('nginx', 'web-hosting'), ('apache', 'web-hosting'), ('caddy', 'web-hosting'), ('hosting', 'web-hosting'), ('deploy', 'web-hosting'), ('pm2', 'web-hosting'),
        ('mysql', 'computers'), ('postgres', 'computers'), ('mongo', 'computers'), ('redis', 'computers'), ('mariadb', 'computers'), ('database', 'computers'),
        ('firewall', 'networking'), ('ssl', 'networking'), ('ufw', 'networking'), ('iptables', 'networking'),
        ('network', 'networking'), ('dns', 'networking'), ('ip ', 'networking'), ('vpn', 'networking'), ('ssh', 'networking'),
        ('cctv', 'cctv-cameras'), ('camera', 'cctv-cameras'), ('surveillance', 'cctv-cameras'),
        ('billing', 'billing-systems'), ('invoice', 'billing-systems'), ('whmcs', 'billing-systems'), ('payment', 'billing-systems'),
        ('install', 'computers'), ('setup', 'computers'), ('config', 'computers'),
        ('python', 'learning'), ('javascript', 'learning'), ('programming', 'learning'), ('tutorial', 'learning'),
        ('git', 'learning'), ('bash', 'learning'), ('linux', 'learning'), ('command', 'learning'),
    ]
    for keyword, cat in mapping:
        if keyword in title_lower:
            return cat
    return 'learning'


def detect_difficulty(text):
    text_lower = text[:3000].lower()
    advanced = ['advanced', 'complex', 'production', 'cluster', 'replication', 'high availability', 'scaling']
    beginner = ['basic', 'beginner', 'getting started', 'introduction', 'simple', 'first', 'how to']
    for kw in advanced:
        if kw in text_lower:
            return 'advanced'
    for kw in beginner:
        if kw in text_lower:
            return 'beginner'
    return 'intermediate'


def detect_os(text):
    text_lower = text[:3000].lower()
    os_map = {'ubuntu': 'ubuntu', 'debian': 'debian', 'centos': 'centos', 'rhel': 'rhel', 'fedora': 'fedora', 'windows': 'windows', 'macos': 'mac'}
    os_list = [v for k, v in os_map.items() if k in text_lower]
    return os_list if os_list else ['linux']


def extract_tags(title, text):
    combined = (title + " " + text[:3000]).lower()
    all_tags = ['docker', 'nginx', 'apache', 'mysql', 'postgresql', 'mongodb', 'redis', 'python', 'nodejs',
                'git', 'ssh', 'ssl', 'firewall', 'ufw', 'backup', 'cron', 'systemd', 'bash', 'linux',
                'ubuntu', 'centos', 'debian', 'vim', 'nano', 'curl', 'wget', 'tar', 'zip', 'dns',
                'php', 'java', 'golang', 'rust', 'pm2', 'certbot', 'kubernetes']
    return [t for t in all_tags if t in combined][:8]


def detect_code_language(code_text):
    code = code_text.lower()
    if any(k in code for k in ['import ', 'def ', 'print(', 'class ', '__init__']):
        return 'python'
    if any(k in code for k in ['const ', 'let ', 'var ', 'function ', 'console.log', '=>']):
        return 'javascript'
    if any(k in code for k in ['<?php', '$_', '->']):
        return 'php'
    if any(k in code for k in ['server {', 'location /', 'proxy_pass', 'listen ']):
        return 'nginx'
    if any(k in code for k in ['<VirtualHost', 'DocumentRoot', 'ServerName']):
        return 'apache'
    if any(k in code for k in ['FROM ', 'RUN ', 'COPY ', 'EXPOSE ', 'CMD [']):
        return 'dockerfile'
    if any(k in code for k in ['version:', 'services:', 'volumes:']):
        return 'yaml'
    if any(k in code for k in ['{', '":', 'true', 'false', 'null']) and code.strip().startswith('{'):
        return 'json'
    return 'bash'


def find_content_element(soup):
    """Try multiple selectors to find the main content area"""
    for sel in CONTENT_SELECTORS:
        el = soup.select_one(sel)
        if el and len(el.get_text(strip=True)) > 200:
            return el
    return None


def parse_article_to_steps(soup):
    """Parse article HTML into 9xCodes step format"""
    content = find_content_element(soup)
    if not content:
        return []

    # Remove nav, footer, sidebar, ads, comments
    for unwanted in content.select('nav, footer, .sidebar, .ad, .ads, .comments, .related, .share, .social, script, style, .newsletter, .author-bio'):
        unwanted.decompose()

    steps = []
    current_title = ""
    current_desc_parts = []
    current_codes = []

    def flush_step():
        nonlocal current_title, current_desc_parts, current_codes
        desc = ' '.join(current_desc_parts).strip()
        code = '\n'.join(current_codes).strip()
        if current_title and (code or desc):
            lang = detect_code_language(code) if code else 'bash'
            steps.append({
                'title': current_title,
                'description': desc[:500],
                'code': code if code else '# No specific command for this step',
                'language': lang,
            })
        current_title = ""
        current_desc_parts = []
        current_codes = []

    for element in content.find_all(['h1', 'h2', 'h3', 'h4', 'p', 'pre', 'code', 'ol', 'ul', 'div']):
        tag = element.name

        if tag in ('h1', 'h2', 'h3', 'h4'):
            text = element.get_text(strip=True)
            if not text:
                continue
            # Skip generic headings
            if text.lower() in ('conclusion', 'summary', 'table of contents', 'prerequisites', 'share this'):
                continue
            flush_step()
            current_title = text

        elif tag == 'p':
            # Skip if inside a pre/code block
            if element.find_parent('pre'):
                continue
            text = element.get_text(strip=True)
            if text and len(text) > 5:
                current_desc_parts.append(text)

        elif tag == 'pre':
            code_el = element.find('code')
            code_text = code_el.get_text() if code_el else element.get_text()
            code_text = code_text.strip()
            if code_text and len(code_text) > 2:
                current_codes.append(code_text)

        elif tag == 'code' and not element.find_parent('pre'):
            code_text = element.get_text(strip=True)
            if code_text and len(code_text) > 10:
                current_codes.append(code_text)

        elif tag in ('ol', 'ul'):
            if element.find_parent('pre'):
                continue
            items = []
            for li in element.find_all('li', recursive=False):
                li_text = li.get_text(strip=True)
                if li_text:
                    items.append(f"- {li_text}")
            if items:
                current_desc_parts.append('\n'.join(items))

        elif tag == 'div':
            # Check if it's a code block div
            if element.get('class') and any('code' in c or 'highlight' in c for c in element.get('class', [])):
                code_text = element.get_text().strip()
                if code_text and len(code_text) > 2:
                    current_codes.append(code_text)

    flush_step()

    # If no structured steps, create from all code blocks
    if not steps:
        all_codes = []
        all_text = []
        for el in content.find_all('pre'):
            code_el = el.find('code')
            c = (code_el or el).get_text().strip()
            if c and len(c) > 3:
                all_codes.append(c)
        for el in content.find_all('p'):
            t = el.get_text(strip=True)
            if t and len(t) > 10:
                all_text.append(t)

        if all_codes:
            for i, code in enumerate(all_codes[:10]):
                steps.append({
                    'title': f'Step {i+1}',
                    'description': all_text[i] if i < len(all_text) else '',
                    'code': code,
                    'language': detect_code_language(code),
                })

    return steps[:15]


class ScrapeURLRequest(BaseModel):
    url: str


@router.post("/from-url")
async def scrape_from_url(req: ScrapeURLRequest):
    """Scrape a single URL and convert to 9xCodes format"""
    resp = None

    # Try cloudscraper first (bypasses Cloudflare)
    if HAS_CLOUDSCRAPER:
        try:
            scraper = cloudscraper.create_scraper(browser={'browser': 'chrome', 'platform': 'linux'})
            resp = scraper.get(req.url, timeout=25)
            resp.raise_for_status()
        except Exception:
            resp = None

    # Fallback to regular requests
    if resp is None:
        try:
            session = requests.Session()
            session.headers.update(HEADERS)
            resp = session.get(req.url, timeout=20, allow_redirects=True)
            resp.raise_for_status()
        except requests.exceptions.HTTPError as e:
            raise HTTPException(status_code=400, detail=f"Site returned error: {e.response.status_code}. Try a different URL.")
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Failed to fetch URL: {str(e)}")

    soup = BeautifulSoup(resp.text, 'html.parser')

    # Extract title
    title = ""
    for sel in ['h1.post-title', 'h1.entry-title', 'h1.article-title', 'h1.title', 'h1', '.post-title', '.entry-title']:
        el = soup.select_one(sel)
        if el:
            title = el.get_text(strip=True)
            if title:
                break
    if not title:
        title_tag = soup.find('title')
        if title_tag:
            title = title_tag.get_text(strip=True).split('|')[0].split('-')[0].strip()
    if not title:
        raise HTTPException(status_code=400, detail="Could not extract title from page")

    # Clean title
    title = re.sub(r'\s+', ' ', title).strip()

    # Extract description
    desc = ""
    meta_desc = soup.find('meta', attrs={'name': 'description'})
    if meta_desc:
        desc = meta_desc.get('content', '')
    if not desc:
        og_desc = soup.find('meta', attrs={'property': 'og:description'})
        if og_desc:
            desc = og_desc.get('content', '')
    if not desc:
        first_p = soup.find('p')
        if first_p:
            desc = first_p.get_text(strip=True)[:300]

    # Parse steps
    steps = parse_article_to_steps(soup)
    if not steps:
        raise HTTPException(status_code=400, detail="Could not extract code steps from this article. The page may not contain code blocks.")

    full_text = soup.get_text()[:5000]
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
async def save_scraped_article(article: dict = Body(...)):
    """Save a scraped article to database"""
    if not article.get('title') or not article.get('steps'):
        raise HTTPException(status_code=400, detail="Article must have title and steps")

    existing = await snippets_collection.find_one({'title': article['title']})
    if existing:
        raise HTTPException(status_code=409, detail="Article with this title already exists")

    # Always regenerate slug from current title to ensure uniqueness
    article['slug'] = create_slug(article['title'])
    
    # Check for duplicate slug
    existing_slug = await snippets_collection.find_one({'slug': article['slug']})
    if existing_slug:
        raise HTTPException(status_code=409, detail="Article with this slug already exists")

    article.setdefault('id', str(uuid.uuid4()))
    article.setdefault('views', 0)
    article.setdefault('likes', 0)
    article.setdefault('author', 'Admin')
    article.setdefault('createdAt', datetime.now(timezone.utc).isoformat())
    article.setdefault('updatedAt', datetime.now(timezone.utc).isoformat())
    article.setdefault('postInstallation', None)

    await snippets_collection.insert_one(article)
    # Remove _id from response
    article.pop('_id', None)
    return {"message": "Article saved!", "slug": article['slug']}


@router.post("/discover")
async def discover_articles(source: str = "tecmint"):
    """Discover article URLs from open source sites"""
    sites_to_scrape = {
        "tecmint": [
            "https://www.tecmint.com/install-docker-on-ubuntu/",
            "https://www.tecmint.com/install-nginx-on-ubuntu/",
            "https://www.tecmint.com/install-mysql-on-ubuntu/",
            "https://www.tecmint.com/install-php-on-ubuntu/",
            "https://www.tecmint.com/install-nodejs-on-ubuntu/",
            "https://www.tecmint.com/install-postgresql-on-ubuntu/",
            "https://www.tecmint.com/install-redis-server-on-ubuntu/",
            "https://www.tecmint.com/install-apache-on-ubuntu/",
            "https://www.tecmint.com/install-mongodb-on-ubuntu/",
            "https://www.tecmint.com/install-java-on-ubuntu/",
        ],
        "phoenixnap": [
            "https://phoenixnap.com/kb/install-docker-ubuntu",
            "https://phoenixnap.com/kb/install-nginx-ubuntu",
            "https://phoenixnap.com/kb/how-to-install-mysql-on-ubuntu",
            "https://phoenixnap.com/kb/install-node-js-ubuntu",
            "https://phoenixnap.com/kb/install-redis-on-ubuntu-20-04",
            "https://phoenixnap.com/kb/how-to-install-git-on-ubuntu",
            "https://phoenixnap.com/kb/install-postgresql-ubuntu",
            "https://phoenixnap.com/kb/install-pip-ubuntu",
        ],
        "digitalocean": [
            "https://www.digitalocean.com/community/tutorials/how-to-install-nginx-on-ubuntu-22-04",
            "https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-ubuntu-22-04",
            "https://www.digitalocean.com/community/tutorials/initial-server-setup-with-ubuntu-22-04",
            "https://www.digitalocean.com/community/tutorials/how-to-set-up-a-firewall-with-ufw-on-ubuntu-22-04",
            "https://www.digitalocean.com/community/tutorials/how-to-install-mysql-on-ubuntu-22-04",
        ],
    }

    urls = sites_to_scrape.get(source, sites_to_scrape["tecmint"])
    return {"source": source, "urls": urls, "count": len(urls), "available_sources": list(sites_to_scrape.keys())}
