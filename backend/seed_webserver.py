from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
from pathlib import Path
import asyncio
from datetime import datetime
import uuid
import re

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

def create_slug(title):
    slug = title.lower()
    slug = re.sub(r'[^a-z0-9]+', '-', slug)
    return slug.strip('-')

WEBSERVER_ARTICLES = [
    {
        'title': 'Install Nginx on Ubuntu 22.04',
        'description': 'Complete guide to install and configure Nginx web server on Ubuntu.',
        'category': 'web-server',
        'os': ['ubuntu', 'linux'],
        'difficulty': 'beginner',
        'tags': ['nginx', 'web-server', 'ubuntu', 'installation'],
        'steps': [
            {'title': 'Install Nginx', 'description': 'Install Nginx from Ubuntu repositories.', 'code': 'sudo apt update\nsudo apt install -y nginx\n\n# Start and enable\nsudo systemctl start nginx\nsudo systemctl enable nginx\n\n# Check status\nsudo systemctl status nginx\n\n# Verify installation\nnginx -v', 'language': 'bash'},
            {'title': 'Configure Firewall', 'description': 'Allow HTTP and HTTPS traffic.', 'code': '# Check available profiles\nsudo ufw app list\n\n# Allow Nginx\nsudo ufw allow \'Nginx Full\'\n\n# Or allow specific ports\nsudo ufw allow 80/tcp\nsudo ufw allow 443/tcp\n\n# Enable firewall\nsudo ufw enable\nsudo ufw status', 'language': 'bash'},
            {'title': 'Test Nginx', 'description': 'Verify Nginx is running.', 'code': '# Check if Nginx is listening\nsudo ss -tlnp | grep nginx\n\n# Open in browser\nhttp://your-server-ip\n\n# You should see "Welcome to nginx!" page\n\n# Check Nginx config\nsudo nginx -t', 'language': 'bash'},
            {'title': 'Basic Configuration', 'description': 'Understand Nginx file structure.', 'code': '# Main config file\n/etc/nginx/nginx.conf\n\n# Server blocks (virtual hosts)\n/etc/nginx/sites-available/  # Available sites\n/etc/nginx/sites-enabled/    # Enabled sites\n\n# Default site\n/etc/nginx/sites-available/default\n\n# Web root\n/var/www/html/\n\n# Logs\n/var/log/nginx/access.log\n/var/log/nginx/error.log', 'language': 'bash'}
        ],
        'postInstallation': {'title': 'Next Steps', 'content': 'Create server blocks for multiple sites. Configure SSL with Let\'s Encrypt. Setup reverse proxy for applications. Enable gzip compression for better performance.'}
    },
    {
        'title': 'Install Apache on Ubuntu',
        'description': 'Install and configure Apache HTTP Server on Ubuntu Linux.',
        'category': 'web-server',
        'os': ['ubuntu', 'linux'],
        'difficulty': 'beginner',
        'tags': ['apache', 'httpd', 'web-server', 'ubuntu'],
        'steps': [
            {'title': 'Install Apache', 'description': 'Install Apache from repositories.', 'code': 'sudo apt update\nsudo apt install -y apache2\n\n# Start and enable\nsudo systemctl start apache2\nsudo systemctl enable apache2\n\n# Check status\nsudo systemctl status apache2\n\n# Verify version\napache2 -v', 'language': 'bash'},
            {'title': 'Configure Firewall', 'description': 'Allow Apache through firewall.', 'code': '# Allow Apache\nsudo ufw allow \'Apache Full\'\n\n# Or specific ports\nsudo ufw allow 80/tcp\nsudo ufw allow 443/tcp\n\n# Check status\nsudo ufw status', 'language': 'bash'},
            {'title': 'Apache Directory Structure', 'description': 'Understand Apache file layout.', 'code': '# Main configuration\n/etc/apache2/apache2.conf\n\n# Virtual hosts\n/etc/apache2/sites-available/\n/etc/apache2/sites-enabled/\n\n# Modules\n/etc/apache2/mods-available/\n/etc/apache2/mods-enabled/\n\n# Document root\n/var/www/html/\n\n# Logs\n/var/log/apache2/access.log\n/var/log/apache2/error.log', 'language': 'bash'},
            {'title': 'Enable Modules', 'description': 'Enable common Apache modules.', 'code': '# Enable rewrite module\nsudo a2enmod rewrite\n\n# Enable SSL module\nsudo a2enmod ssl\n\n# Enable headers module\nsudo a2enmod headers\n\n# Enable proxy modules\nsudo a2enmod proxy proxy_http\n\n# Disable module\nsudo a2dismod module_name\n\n# Restart Apache\nsudo systemctl restart apache2', 'language': 'bash'}
        ],
        'postInstallation': {'title': 'Configuration', 'content': 'Create virtual hosts in /etc/apache2/sites-available/. Enable sites with a2ensite. Use .htaccess for directory-level configuration. Consider mod_security for WAF.'}
    },
    {
        'title': 'Nginx Server Block Virtual Host Setup',
        'description': 'Configure Nginx server blocks to host multiple websites on single server.',
        'category': 'web-server',
        'os': ['ubuntu', 'centos', 'linux'],
        'difficulty': 'intermediate',
        'tags': ['nginx', 'virtual-host', 'server-block', 'multi-site'],
        'steps': [
            {'title': 'Create Document Root', 'description': 'Setup web directory for new site.', 'code': '# Create directory\nsudo mkdir -p /var/www/example.com/html\n\n# Set ownership\nsudo chown -R $USER:$USER /var/www/example.com/html\n\n# Set permissions\nsudo chmod -R 755 /var/www/example.com\n\n# Create sample page\nnano /var/www/example.com/html/index.html\n\n<html>\n<head><title>Welcome to Example.com</title></head>\n<body><h1>Success! Example.com is working!</h1></body>\n</html>', 'language': 'bash'},
            {'title': 'Create Server Block', 'description': 'Create Nginx configuration file.', 'code': 'sudo nano /etc/nginx/sites-available/example.com\n\nserver {\n    listen 80;\n    listen [::]:80;\n\n    root /var/www/example.com/html;\n    index index.html index.htm index.php;\n\n    server_name example.com www.example.com;\n\n    location / {\n        try_files $uri $uri/ =404;\n    }\n\n    # PHP processing (if needed)\n    location ~ \\.php$ {\n        include snippets/fastcgi-php.conf;\n        fastcgi_pass unix:/var/run/php/php8.1-fpm.sock;\n    }\n\n    # Deny access to .htaccess\n    location ~ /\\.ht {\n        deny all;\n    }\n}', 'language': 'bash'},
            {'title': 'Enable Server Block', 'description': 'Create symbolic link and test.', 'code': '# Enable site\nsudo ln -s /etc/nginx/sites-available/example.com /etc/nginx/sites-enabled/\n\n# Test configuration\nsudo nginx -t\n\n# If successful, reload Nginx\nsudo systemctl reload nginx\n\n# Or restart\nsudo systemctl restart nginx', 'language': 'bash'},
            {'title': 'Multiple Sites Example', 'description': 'Setup additional sites.', 'code': '# Create another site\nsudo mkdir -p /var/www/site2.com/html\nsudo nano /etc/nginx/sites-available/site2.com\n\nserver {\n    listen 80;\n    server_name site2.com www.site2.com;\n    root /var/www/site2.com/html;\n    index index.html;\n\n    location / {\n        try_files $uri $uri/ =404;\n    }\n}\n\n# Enable\nsudo ln -s /etc/nginx/sites-available/site2.com /etc/nginx/sites-enabled/\nsudo nginx -t && sudo systemctl reload nginx\n\n# List enabled sites\nls -la /etc/nginx/sites-enabled/', 'language': 'bash'}
        ],
        'postInstallation': {'title': 'DNS Setup', 'content': 'Point domain A records to your server IP. Use Cloudflare for DNS and CDN. Add SSL certificates using Certbot. Test with curl -I http://example.com'}
    },
    {
        'title': 'Nginx Reverse Proxy Configuration',
        'description': 'Setup Nginx as reverse proxy for backend applications like Node.js, Python, etc.',
        'category': 'web-server',
        'os': ['ubuntu', 'centos', 'linux'],
        'difficulty': 'intermediate',
        'tags': ['nginx', 'reverse-proxy', 'proxy', 'backend'],
        'steps': [
            {'title': 'Basic Reverse Proxy', 'description': 'Proxy to backend application.', 'code': 'sudo nano /etc/nginx/sites-available/app.example.com\n\nserver {\n    listen 80;\n    server_name app.example.com;\n\n    location / {\n        proxy_pass http://localhost:3000;\n        proxy_http_version 1.1;\n        proxy_set_header Upgrade $http_upgrade;\n        proxy_set_header Connection \'upgrade\';\n        proxy_set_header Host $host;\n        proxy_set_header X-Real-IP $remote_addr;\n        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;\n        proxy_set_header X-Forwarded-Proto $scheme;\n        proxy_cache_bypass $http_upgrade;\n    }\n}', 'language': 'bash'},
            {'title': 'Proxy with Path', 'description': 'Proxy specific paths to different backends.', 'code': 'server {\n    listen 80;\n    server_name example.com;\n\n    # Static files\n    location / {\n        root /var/www/html;\n        index index.html;\n    }\n\n    # API backend\n    location /api/ {\n        proxy_pass http://localhost:8000/;\n        proxy_set_header Host $host;\n        proxy_set_header X-Real-IP $remote_addr;\n    }\n\n    # WebSocket\n    location /ws/ {\n        proxy_pass http://localhost:8001/;\n        proxy_http_version 1.1;\n        proxy_set_header Upgrade $http_upgrade;\n        proxy_set_header Connection "upgrade";\n    }\n}', 'language': 'bash'},
            {'title': 'Load Balancing', 'description': 'Distribute traffic across multiple backends.', 'code': '# Define upstream servers\nupstream backend {\n    least_conn;  # Load balancing method\n    server 127.0.0.1:3001 weight=3;\n    server 127.0.0.1:3002 weight=2;\n    server 127.0.0.1:3003 backup;\n}\n\nserver {\n    listen 80;\n    server_name example.com;\n\n    location / {\n        proxy_pass http://backend;\n        proxy_set_header Host $host;\n        proxy_set_header X-Real-IP $remote_addr;\n    }\n}\n\n# Load balancing methods:\n# - round-robin (default)\n# - least_conn\n# - ip_hash (sticky sessions)\n# - hash $request_uri', 'language': 'bash'},
            {'title': 'Caching and Buffering', 'description': 'Enable proxy caching.', 'code': '# In nginx.conf (http block)\nproxy_cache_path /var/cache/nginx levels=1:2 keys_zone=my_cache:10m max_size=1g inactive=60m;\n\n# In server block\nserver {\n    listen 80;\n    server_name example.com;\n\n    location / {\n        proxy_pass http://localhost:3000;\n        \n        # Enable caching\n        proxy_cache my_cache;\n        proxy_cache_valid 200 60m;\n        proxy_cache_valid 404 1m;\n        proxy_cache_use_stale error timeout updating;\n        add_header X-Cache-Status $upstream_cache_status;\n        \n        # Buffering\n        proxy_buffering on;\n        proxy_buffer_size 4k;\n        proxy_buffers 8 4k;\n    }\n}', 'language': 'bash'}
        ],
        'postInstallation': {'title': 'Testing', 'content': 'Test with curl -I to check headers. Monitor with access.log. Add SSL with Certbot. Use nginx -t before reloading configuration.'}
    },
    {
        'title': 'Apache Virtual Host Configuration',
        'description': 'Configure Apache virtual hosts for hosting multiple websites.',
        'category': 'web-server',
        'os': ['ubuntu', 'centos', 'linux'],
        'difficulty': 'intermediate',
        'tags': ['apache', 'virtual-host', 'multi-site', 'httpd'],
        'steps': [
            {'title': 'Create Document Root', 'description': 'Setup directory for website.', 'code': '# Create directory\nsudo mkdir -p /var/www/example.com/public_html\n\n# Set ownership\nsudo chown -R $USER:$USER /var/www/example.com\n\n# Set permissions\nsudo chmod -R 755 /var/www\n\n# Create sample page\necho \'<h1>Hello from example.com</h1>\' > /var/www/example.com/public_html/index.html', 'language': 'bash'},
            {'title': 'Create Virtual Host File', 'description': 'Configure Apache virtual host.', 'code': 'sudo nano /etc/apache2/sites-available/example.com.conf\n\n<VirtualHost *:80>\n    ServerAdmin admin@example.com\n    ServerName example.com\n    ServerAlias www.example.com\n    DocumentRoot /var/www/example.com/public_html\n    \n    <Directory /var/www/example.com/public_html>\n        Options Indexes FollowSymLinks\n        AllowOverride All\n        Require all granted\n    </Directory>\n    \n    ErrorLog ${APACHE_LOG_DIR}/example.com_error.log\n    CustomLog ${APACHE_LOG_DIR}/example.com_access.log combined\n</VirtualHost>', 'language': 'bash'},
            {'title': 'Enable Virtual Host', 'description': 'Enable site and restart Apache.', 'code': '# Enable site\nsudo a2ensite example.com.conf\n\n# Disable default site (optional)\nsudo a2dissite 000-default.conf\n\n# Test configuration\nsudo apache2ctl configtest\n\n# Restart Apache\nsudo systemctl restart apache2\n\n# Check status\nsudo systemctl status apache2', 'language': 'bash'},
            {'title': 'PHP Virtual Host Example', 'description': 'Virtual host with PHP support.', 'code': '<VirtualHost *:80>\n    ServerName phpapp.example.com\n    DocumentRoot /var/www/phpapp/public\n    \n    <Directory /var/www/phpapp/public>\n        Options -Indexes +FollowSymLinks\n        AllowOverride All\n        Require all granted\n    </Directory>\n    \n    # PHP settings\n    <FilesMatch \\.php$>\n        SetHandler "proxy:unix:/var/run/php/php8.1-fpm.sock|fcgi://localhost"\n    </FilesMatch>\n    \n    # Security headers\n    Header always set X-Content-Type-Options "nosniff"\n    Header always set X-Frame-Options "SAMEORIGIN"\n    \n    ErrorLog ${APACHE_LOG_DIR}/phpapp_error.log\n    CustomLog ${APACHE_LOG_DIR}/phpapp_access.log combined\n</VirtualHost>', 'language': 'bash'}
        ],
        'postInstallation': {'title': 'Tips', 'content': 'Use a2ensite and a2dissite for managing sites. Enable mod_rewrite for URL rewriting. Use .htaccess for additional configuration. Add SSL with Certbot.'}
    },
    {
        'title': 'Setup SSL/TLS with Let\'s Encrypt Certbot',
        'description': 'Install free SSL certificates using Let\'s Encrypt Certbot for Nginx and Apache.',
        'category': 'web-server',
        'os': ['ubuntu', 'centos', 'linux'],
        'difficulty': 'intermediate',
        'tags': ['ssl', 'tls', 'https', 'letsencrypt', 'certbot'],
        'steps': [
            {'title': 'Install Certbot', 'description': 'Install Certbot and web server plugin.', 'code': '# Ubuntu/Debian\nsudo apt update\nsudo apt install -y certbot\n\n# For Nginx\nsudo apt install -y python3-certbot-nginx\n\n# For Apache\nsudo apt install -y python3-certbot-apache\n\n# CentOS/RHEL\nsudo yum install -y epel-release\nsudo yum install -y certbot python3-certbot-nginx', 'language': 'bash'},
            {'title': 'Obtain Certificate (Nginx)', 'description': 'Get SSL certificate for Nginx.', 'code': '# Automatic configuration\nsudo certbot --nginx -d example.com -d www.example.com\n\n# Follow prompts:\n# - Enter email\n# - Agree to terms\n# - Choose redirect option (recommended: 2)\n\n# Manual (certificate only)\nsudo certbot certonly --nginx -d example.com\n\n# Verify certificate\nsudo certbot certificates', 'language': 'bash'},
            {'title': 'Obtain Certificate (Apache)', 'description': 'Get SSL certificate for Apache.', 'code': '# Automatic configuration\nsudo certbot --apache -d example.com -d www.example.com\n\n# Certificate only (manual config)\nsudo certbot certonly --apache -d example.com\n\n# Verify\nsudo certbot certificates', 'language': 'bash'},
            {'title': 'Auto-Renewal Setup', 'description': 'Configure automatic certificate renewal.', 'code': '# Test renewal\nsudo certbot renew --dry-run\n\n# Certbot creates automatic cron job or systemd timer\n# Check timer status\nsudo systemctl status certbot.timer\n\n# Manual cron (if needed)\nsudo crontab -e\n0 3 * * * /usr/bin/certbot renew --quiet\n\n# Certificate location\n/etc/letsencrypt/live/example.com/fullchain.pem\n/etc/letsencrypt/live/example.com/privkey.pem', 'language': 'bash'}
        ],
        'postInstallation': {'title': 'Security', 'content': 'Check SSL configuration at ssllabs.com/ssltest. Enable HSTS for better security. Certificates renew automatically every 60-90 days. Monitor expiry with certbot certificates command.'}
    },
    {
        'title': 'Nginx Performance Optimization',
        'description': 'Optimize Nginx configuration for better performance and security.',
        'category': 'web-server',
        'os': ['ubuntu', 'centos', 'linux'],
        'difficulty': 'advanced',
        'tags': ['nginx', 'performance', 'optimization', 'security'],
        'steps': [
            {'title': 'Worker Configuration', 'description': 'Optimize worker processes.', 'code': '# Edit nginx.conf\nsudo nano /etc/nginx/nginx.conf\n\n# Worker settings\nworker_processes auto;  # Or number of CPU cores\nworker_rlimit_nofile 65535;\n\nevents {\n    worker_connections 4096;\n    use epoll;\n    multi_accept on;\n}', 'language': 'bash'},
            {'title': 'Enable Gzip Compression', 'description': 'Compress responses for faster delivery.', 'code': '# In http block or server block\ngzip on;\ngzip_vary on;\ngzip_proxied any;\ngzip_comp_level 6;\ngzip_min_length 1000;\ngzip_types\n    text/plain\n    text/css\n    text/xml\n    application/json\n    application/javascript\n    application/xml\n    application/xml+rss\n    image/svg+xml;', 'language': 'bash'},
            {'title': 'Enable Caching', 'description': 'Configure browser and proxy caching.', 'code': '# Browser caching for static files\nlocation ~* \\.(jpg|jpeg|png|gif|ico|css|js|pdf|woff|woff2)$ {\n    expires 30d;\n    add_header Cache-Control "public, no-transform";\n}\n\n# FastCGI cache for PHP\nfastcgi_cache_path /var/cache/nginx/fastcgi levels=1:2 keys_zone=FASTCGI:100m inactive=60m;\n\nlocation ~ \\.php$ {\n    fastcgi_cache FASTCGI;\n    fastcgi_cache_valid 200 60m;\n    fastcgi_cache_use_stale error timeout;\n    add_header X-FastCGI-Cache $upstream_cache_status;\n}', 'language': 'bash'},
            {'title': 'Security Headers', 'description': 'Add security headers.', 'code': '# In server block\n\n# Security headers\nadd_header X-Frame-Options "SAMEORIGIN" always;\nadd_header X-Content-Type-Options "nosniff" always;\nadd_header X-XSS-Protection "1; mode=block" always;\nadd_header Referrer-Policy "strict-origin-when-cross-origin" always;\nadd_header Content-Security-Policy "default-src \'self\'" always;\n\n# SSL settings (for HTTPS)\nssl_protocols TLSv1.2 TLSv1.3;\nssl_prefer_server_ciphers on;\nssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256;\nssl_session_cache shared:SSL:10m;\nssl_session_timeout 10m;\nadd_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;', 'language': 'bash'}
        ],
        'postInstallation': {'title': 'Testing', 'content': 'Test configuration: nginx -t. Check headers: curl -I. Performance test: ab -n 1000 -c 100 http://example.com/. Monitor: tail -f /var/log/nginx/access.log'}
    },
    {
        'title': 'Install LiteSpeed Web Server',
        'description': 'Install OpenLiteSpeed - high-performance web server on Ubuntu.',
        'category': 'web-server',
        'os': ['ubuntu', 'linux'],
        'difficulty': 'intermediate',
        'tags': ['litespeed', 'openlitespeed', 'web-server', 'performance'],
        'steps': [
            {'title': 'Add LiteSpeed Repository', 'description': 'Add official OpenLiteSpeed repository.', 'code': '# Add repository\nwget -O - https://repo.litespeed.sh | sudo bash\n\n# Update package list\nsudo apt update', 'language': 'bash'},
            {'title': 'Install OpenLiteSpeed', 'description': 'Install OpenLiteSpeed server.', 'code': '# Install OpenLiteSpeed\nsudo apt install -y openlitespeed\n\n# Install PHP (LiteSpeed PHP)\nsudo apt install -y lsphp81 lsphp81-mysql lsphp81-common lsphp81-curl\n\n# Start OpenLiteSpeed\nsudo systemctl start lsws\nsudo systemctl enable lsws\n\n# Check status\nsudo systemctl status lsws', 'language': 'bash'},
            {'title': 'Set Admin Password', 'description': 'Configure admin panel access.', 'code': '# Set admin password\nsudo /usr/local/lsws/admin/misc/admpass.sh\n\n# Enter new admin username and password\n\n# Admin panel URL\nhttps://your-server-ip:7080\n\n# Web server URL\nhttp://your-server-ip:8088', 'language': 'bash'},
            {'title': 'Configure Firewall', 'description': 'Allow LiteSpeed ports.', 'code': '# Allow admin panel\nsudo ufw allow 7080/tcp\n\n# Allow web traffic\nsudo ufw allow 80/tcp\nsudo ufw allow 443/tcp\nsudo ufw allow 8088/tcp  # Default HTTP port\n\n# Check firewall\nsudo ufw status', 'language': 'bash'}
        ],
        'postInstallation': {'title': 'Configuration', 'content': 'Access admin panel at https://server-ip:7080. Change default port from 8088 to 80 in admin panel. Virtual hosts configured through web admin. OpenLiteSpeed is Apache-compatible.'}
    }
]

async def seed_webserver():
    print("=" * 60)
    print("  SEEDING: Web Server Articles")
    print("=" * 60)
    
    added = 0
    for article in WEBSERVER_ARTICLES:
        article['id'] = str(uuid.uuid4())
        article['slug'] = create_slug(article['title'])
        article['author'] = 'Admin'
        article['createdAt'] = datetime.utcnow()
        article['updatedAt'] = datetime.utcnow()
        article['views'] = 1000 + (hash(article['title']) % 5000)
        article['likes'] = 50 + (hash(article['title']) % 200)
        
        existing = await db.code_snippets.find_one({'slug': article['slug']})
        if not existing:
            await db.code_snippets.insert_one(article)
            print(f"✓ Added: {article['title'][:50]}...")
            added += 1
        else:
            print(f"- Skipped: {article['title'][:50]}...")
    
    print(f"\n✓ Added {added} Web Server articles")
    total = await db.code_snippets.count_documents({'category': 'web-server'})
    print(f"Total Web Server articles: {total}")

if __name__ == "__main__":
    asyncio.run(seed_webserver())
