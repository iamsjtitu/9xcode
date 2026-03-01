from fastapi import APIRouter, HTTPException
from database import snippets_collection
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime, timezone
import uuid, re

router = APIRouter(prefix="/seeder", tags=["seeder"])

def slug(title):
    s = re.sub(r'[^a-z0-9]+', '-', title.lower())
    return s.strip('-')

def art(title, desc, cat, os_list, diff, tags, steps):
    return {
        'id': str(uuid.uuid4()), 'title': title, 'slug': slug(title),
        'description': desc, 'category': cat, 'os': os_list,
        'difficulty': diff, 'views': 0, 'likes': 0, 'author': 'Admin',
        'createdAt': datetime.now(timezone.utc).isoformat(),
        'updatedAt': datetime.now(timezone.utc).isoformat(),
        'tags': tags,
        'steps': [{'title': s[0], 'description': s[1], 'code': s[2], 'language': s[3] if len(s) > 3 else 'bash'} for s in steps],
        'postInstallation': None,
    }

# ============ ARTICLE TEMPLATES PER CATEGORY ============
TEMPLATES = {
    'installation': [
        lambda os: art(f'Install Docker on {os}', f'Complete guide to install Docker engine on {os}.', 'installation', [os.lower()], 'beginner', ['docker', 'container', os.lower()],
            [('Update System', f'Update {os} packages.', f'sudo apt update && sudo apt upgrade -y'),
             ('Install Docker', 'Install Docker from official repo.', 'curl -fsSL https://get.docker.com | sh'),
             ('Start Docker', 'Enable and start Docker service.', 'sudo systemctl enable docker\nsudo systemctl start docker\ndocker --version'),
             ('Test Installation', 'Verify Docker works.', 'sudo docker run hello-world')]),
        lambda os: art(f'Install Nginx on {os}', f'Setup Nginx web server on {os} with configuration.', 'installation', [os.lower()], 'beginner', ['nginx', 'webserver', os.lower()],
            [('Install Nginx', f'Install Nginx on {os}.', 'sudo apt update\nsudo apt install nginx -y'),
             ('Start Service', 'Enable and start Nginx.', 'sudo systemctl enable nginx\nsudo systemctl start nginx\nsudo systemctl status nginx'),
             ('Configure Firewall', 'Allow HTTP/HTTPS traffic.', 'sudo ufw allow "Nginx Full"\nsudo ufw status'),
             ('Test', 'Verify Nginx is running.', 'curl http://localhost\nnginx -v')]),
        lambda os: art(f'Install MySQL 8 on {os}', f'Install and secure MySQL 8 database server on {os}.', 'installation', [os.lower()], 'intermediate', ['mysql', 'database', os.lower()],
            [('Install MySQL', f'Install MySQL server on {os}.', 'sudo apt update\nsudo apt install mysql-server -y'),
             ('Secure Installation', 'Run MySQL secure installation wizard.', 'sudo mysql_secure_installation'),
             ('Create Database', 'Create a database and user.', "sudo mysql -u root -p\nCREATE DATABASE myapp;\nCREATE USER 'appuser'@'localhost' IDENTIFIED BY 'StrongPass123!';\nGRANT ALL ON myapp.* TO 'appuser'@'localhost';\nFLUSH PRIVILEGES;"),
             ('Verify', 'Check MySQL status.', 'sudo systemctl status mysql\nmysql --version')]),
        lambda os: art(f'Install PostgreSQL on {os}', f'Setup PostgreSQL database on {os} with user configuration.', 'installation', [os.lower()], 'intermediate', ['postgresql', 'database', os.lower()],
            [('Install PostgreSQL', f'Install PostgreSQL on {os}.', 'sudo apt update\nsudo apt install postgresql postgresql-contrib -y'),
             ('Start Service', 'Enable PostgreSQL.', 'sudo systemctl enable postgresql\nsudo systemctl start postgresql'),
             ('Create User & Database', 'Setup database.', 'sudo -u postgres psql\nCREATE USER myuser WITH PASSWORD \'mypassword\';\nCREATE DATABASE mydb OWNER myuser;\n\\q'),
             ('Connect', 'Test connection.', 'psql -U myuser -d mydb -h localhost')]),
        lambda os: art(f'Install Node.js 20 LTS on {os}', f'Install Node.js 20 LTS using NodeSource on {os}.', 'installation', [os.lower()], 'beginner', ['nodejs', 'npm', 'javascript', os.lower()],
            [('Add NodeSource Repo', 'Add official Node.js repository.', 'curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -'),
             ('Install Node.js', 'Install Node.js and npm.', 'sudo apt install nodejs -y\nnode -v\nnpm -v'),
             ('Install Yarn', 'Optional: install Yarn package manager.', 'npm install -g yarn\nyarn --version')]),
    ],
    'configuration': [
        lambda os: art(f'Configure SSH Server on {os}', f'Harden SSH configuration on {os} for security.', 'configuration', [os.lower()], 'intermediate', ['ssh', 'security', os.lower()],
            [('Backup Config', 'Backup SSH config before changes.', 'sudo cp /etc/ssh/sshd_config /etc/ssh/sshd_config.bak'),
             ('Edit SSH Config', 'Change important settings.', 'sudo nano /etc/ssh/sshd_config\n\n# Change these settings:\nPort 2222\nPermitRootLogin no\nPasswordAuthentication no\nMaxAuthTries 3\nClientAliveInterval 300'),
             ('Restart SSH', 'Apply changes.', 'sudo systemctl restart sshd\nsudo systemctl status sshd')]),
        lambda os: art(f'Configure Swap Memory on {os}', f'Create and configure swap space on {os}.', 'configuration', [os.lower()], 'beginner', ['swap', 'memory', os.lower()],
            [('Check Current Swap', 'Check if swap exists.', 'sudo swapon --show\nfree -h'),
             ('Create Swap File', 'Create 2GB swap file.', 'sudo fallocate -l 2G /swapfile\nsudo chmod 600 /swapfile\nsudo mkswap /swapfile\nsudo swapon /swapfile'),
             ('Make Permanent', 'Add to fstab.', 'echo "/swapfile none swap sw 0 0" | sudo tee -a /etc/fstab\nsudo sysctl vm.swappiness=10\necho "vm.swappiness=10" | sudo tee -a /etc/sysctl.conf')]),
        lambda os: art(f'Configure Fail2ban on {os}', f'Setup Fail2ban intrusion prevention on {os}.', 'configuration', [os.lower()], 'intermediate', ['fail2ban', 'security', 'firewall', os.lower()],
            [('Install Fail2ban', 'Install the service.', 'sudo apt update\nsudo apt install fail2ban -y'),
             ('Create Local Config', 'Create custom configuration.', 'sudo cp /etc/fail2ban/jail.conf /etc/fail2ban/jail.local\nsudo nano /etc/fail2ban/jail.local\n\n[sshd]\nenabled = true\nport = ssh\nfilter = sshd\nlogpath = /var/log/auth.log\nmaxretry = 3\nbantime = 3600'),
             ('Start Service', 'Enable and check status.', 'sudo systemctl enable fail2ban\nsudo systemctl start fail2ban\nsudo fail2ban-client status\nsudo fail2ban-client status sshd')]),
    ],
    'security': [
        lambda os: art(f'Setup UFW Firewall on {os}', f'Configure UFW firewall rules on {os}.', 'security', [os.lower()], 'beginner', ['ufw', 'firewall', os.lower()],
            [('Install & Enable', 'Install UFW.', 'sudo apt install ufw -y\nsudo ufw default deny incoming\nsudo ufw default allow outgoing'),
             ('Allow Services', 'Open required ports.', 'sudo ufw allow ssh\nsudo ufw allow 80/tcp\nsudo ufw allow 443/tcp\nsudo ufw allow 8080/tcp'),
             ('Enable & Status', 'Activate firewall.', 'sudo ufw enable\nsudo ufw status verbose\nsudo ufw status numbered')]),
        lambda os: art(f'Setup ClamAV Antivirus on {os}', f'Install and configure ClamAV antivirus scanner on {os}.', 'security', [os.lower()], 'intermediate', ['clamav', 'antivirus', 'malware', os.lower()],
            [('Install ClamAV', 'Install ClamAV and daemon.', 'sudo apt update\nsudo apt install clamav clamav-daemon -y'),
             ('Update Virus Database', 'Update virus definitions.', 'sudo systemctl stop clamav-freshclam\nsudo freshclam\nsudo systemctl start clamav-freshclam'),
             ('Run Scan', 'Scan directories.', 'sudo clamscan -r /home\nsudo clamscan -r --infected --remove /var/www')]),
    ],
    'networking': [
        lambda os: art(f'Configure DNS Server on {os}', f'Setup BIND9 DNS server on {os}.', 'networking', [os.lower()], 'advanced', ['dns', 'bind9', os.lower()],
            [('Install BIND', 'Install DNS server.', 'sudo apt update\nsudo apt install bind9 bind9utils bind9-doc -y'),
             ('Configure Zones', 'Add zone configuration.', 'sudo nano /etc/bind/named.conf.local\n\nzone "example.com" {\n    type master;\n    file "/etc/bind/db.example.com";\n};'),
             ('Create Zone File', 'Define DNS records.', 'sudo cp /etc/bind/db.local /etc/bind/db.example.com\nsudo nano /etc/bind/db.example.com'),
             ('Restart & Test', 'Apply changes.', 'sudo named-checkconf\nsudo systemctl restart bind9\ndig @localhost example.com')]),
        lambda os: art(f'Network Troubleshooting on {os}', f'Essential network diagnostic commands on {os}.', 'networking', [os.lower()], 'beginner', ['network', 'diagnostics', 'troubleshooting', os.lower()],
            [('Check Connectivity', 'Basic network checks.', 'ping -c 4 google.com\ntraceroute google.com\ncurl -I https://google.com'),
             ('DNS Diagnostics', 'DNS resolution checks.', 'nslookup google.com\ndig google.com\ncat /etc/resolv.conf'),
             ('Port & Connection', 'Check open ports and connections.', 'ss -tulnp\nnetstat -tulnp\nsudo lsof -i :80\nnmap -sT localhost')]),
    ],
    'database': [
        lambda os: art(f'MongoDB Administration on {os}', f'Essential MongoDB admin commands and maintenance on {os}.', 'database', [os.lower()], 'intermediate', ['mongodb', 'nosql', os.lower()],
            [('Connect to MongoDB', 'Access MongoDB shell.', 'mongosh\n# Or older versions:\nmongo'),
             ('Database Operations', 'Common database commands.', 'show dbs\nuse mydb\nshow collections\ndb.stats()\ndb.collection.countDocuments({})'),
             ('Backup & Restore', 'Backup and restore databases.', '# Backup\nmongodump --db mydb --out /backup/\n\n# Restore\nmongorestore --db mydb /backup/mydb/')]),
        lambda os: art(f'Redis Administration on {os}', f'Redis server management and optimization on {os}.', 'database', [os.lower()], 'intermediate', ['redis', 'cache', 'nosql', os.lower()],
            [('Redis CLI Basics', 'Common Redis commands.', 'redis-cli\nINFO server\nDBSIZE\nKEYS *\nSELECT 0'),
             ('Data Operations', 'Work with Redis data.', 'SET mykey "value"\nGET mykey\nEXPIRE mykey 300\nTTL mykey\nDEL mykey'),
             ('Persistence & Backup', 'Save and backup data.', 'redis-cli BGSAVE\ncp /var/lib/redis/dump.rdb /backup/\nredis-cli CONFIG SET maxmemory 256mb')]),
    ],
    'web-server': [
        lambda os: art(f'Apache Virtual Hosts on {os}', f'Configure Apache virtual hosts for multiple sites on {os}.', 'web-server', [os.lower()], 'intermediate', ['apache', 'virtualhost', os.lower()],
            [('Create Document Root', 'Setup directory for site.', 'sudo mkdir -p /var/www/mysite.com/html\nsudo chown -R $USER:$USER /var/www/mysite.com'),
             ('Create Virtual Host', 'Configure the vhost.', 'sudo nano /etc/apache2/sites-available/mysite.com.conf\n\n<VirtualHost *:80>\n    ServerName mysite.com\n    ServerAlias www.mysite.com\n    DocumentRoot /var/www/mysite.com/html\n    ErrorLog ${APACHE_LOG_DIR}/error.log\n</VirtualHost>'),
             ('Enable Site', 'Activate the virtual host.', 'sudo a2ensite mysite.com.conf\nsudo a2dissite 000-default.conf\nsudo apache2ctl configtest\nsudo systemctl reload apache2')]),
    ],
    'monitoring': [
        lambda os: art(f'System Monitoring with htop on {os}', f'Use htop and system tools for monitoring on {os}.', 'monitoring', [os.lower()], 'beginner', ['htop', 'monitoring', 'system', os.lower()],
            [('Install Monitoring Tools', 'Install essential tools.', 'sudo apt install htop iotop iftop ncdu -y'),
             ('CPU & Memory', 'Monitor CPU and memory.', 'htop\nfree -h\nvmstat 1 5\nmpstat -P ALL 1 3'),
             ('Disk & Network', 'Monitor disk and network.', 'iotop\ndf -h\ndu -sh /var/*\niftop -i eth0')]),
    ],
    'backup': [
        lambda os: art(f'Automated Backup Script for {os}', f'Create comprehensive backup solution for {os}.', 'backup', [os.lower()], 'intermediate', ['backup', 'automation', 'cron', os.lower()],
            [('Create Backup Script', 'Write backup script.', '#!/bin/bash\nDATE=$(date +%Y-%m-%d_%H-%M)\nBACKUP_DIR="/backup/$DATE"\nmkdir -p "$BACKUP_DIR"\n\n# Backup files\ntar -czf "$BACKUP_DIR/www.tar.gz" /var/www/\n\n# Backup databases\nmongodump --out "$BACKUP_DIR/mongodb/"\nmysqldump --all-databases > "$BACKUP_DIR/mysql_all.sql"\n\necho "Backup completed: $BACKUP_DIR"'),
             ('Schedule Cron', 'Automate daily backup.', 'chmod +x /usr/local/bin/backup.sh\ncrontab -e\n# Add: 0 2 * * * /usr/local/bin/backup.sh >> /var/log/backup.log 2>&1'),
             ('Cleanup Old Backups', 'Remove backups older than 30 days.', 'find /backup -type d -mtime +30 -exec rm -rf {} +')]),
    ],
    'computers': [
        lambda os: art(f'System Administration on {os}', f'Essential system admin commands for {os}.', 'computers', [os.lower()], 'beginner', ['sysadmin', 'commands', os.lower()],
            [('System Information', 'Check system details.', 'uname -a\nhostnamectl\nlsb_release -a\ncat /etc/os-release'),
             ('User Management', 'Manage users and groups.', 'sudo adduser newuser\nsudo usermod -aG sudo newuser\nsudo passwd newuser\ngroups newuser'),
             ('Service Management', 'Control system services.', 'sudo systemctl list-units --type=service\nsudo systemctl status nginx\nsudo journalctl -u nginx --since today')]),
    ],
    'cctv-cameras': [
        lambda os: art(f'Setup ZoneMinder CCTV on {os}', f'Install ZoneMinder surveillance system on {os}.', 'cctv-cameras', [os.lower()], 'advanced', ['zoneminder', 'surveillance', 'cctv', os.lower()],
            [('Install ZoneMinder', 'Install from repository.', 'sudo apt update\nsudo apt install zoneminder -y'),
             ('Configure Database', 'Setup MySQL for ZoneMinder.', 'sudo mysql -u root -p < /usr/share/zoneminder/db/zm_create.sql\nsudo mysql -u root -p -e "GRANT ALL ON zm.* TO \'zmuser\'@localhost IDENTIFIED BY \'zmpass\';"'),
             ('Configure Apache', 'Enable ZoneMinder web interface.', 'sudo a2enmod cgi rewrite\nsudo a2enconf zoneminder\nsudo systemctl restart apache2'),
             ('Start ZoneMinder', 'Enable the service.', 'sudo systemctl enable zoneminder\nsudo systemctl start zoneminder\necho "Access: http://your-server/zm"')]),
    ],
    'learning': [
        lambda os: art(f'Linux Command Line Essentials for {os}', f'Must-know command line tricks for {os} users.', 'learning', [os.lower()], 'beginner', ['cli', 'terminal', 'commands', os.lower()],
            [('File Navigation', 'Navigate the file system.', 'pwd\nls -la\ncd /var/log\nfind / -name "*.conf" -type f 2>/dev/null\nlocate nginx.conf'),
             ('Text Processing', 'Process text files.', 'grep -r "error" /var/log/\nawk \'{print $1}\' access.log | sort | uniq -c | sort -rn\nsed -i \'s/old/new/g\' file.txt\nwc -l file.txt'),
             ('Process Management', 'Manage running processes.', 'ps aux | grep nginx\ntop -bn1 | head -20\nkill -9 <PID>\nnohup ./script.sh &\nscreen -S mysession')]),
    ],
    'virtualization': [
        lambda os: art(f'Docker Compose Multi-Service on {os}', f'Deploy multi-container apps with Docker Compose on {os}.', 'virtualization', [os.lower()], 'intermediate', ['docker', 'docker-compose', 'container', os.lower()],
            [('Create Compose File', 'Define services.', 'version: "3.8"\nservices:\n  app:\n    build: .\n    ports:\n      - "3000:3000"\n    depends_on:\n      - db\n    environment:\n      - DB_HOST=db\n  db:\n    image: mongo:7\n    volumes:\n      - dbdata:/data/db\nvolumes:\n  dbdata:', 'yaml'),
             ('Deploy Stack', 'Launch all services.', 'docker compose up -d\ndocker compose ps\ndocker compose logs -f app'),
             ('Scale Services', 'Scale and manage.', 'docker compose up -d --scale app=3\ndocker compose down\ndocker compose down -v  # Remove volumes too')]),
    ],
    'web-hosting': [
        lambda os: art(f'Deploy Web App with Nginx on {os}', f'Production deployment with Nginx reverse proxy on {os}.', 'web-hosting', [os.lower()], 'intermediate', ['nginx', 'deployment', 'production', os.lower()],
            [('Setup Application', 'Clone and build app.', 'cd /var/www\ngit clone https://github.com/user/app.git\ncd app\nnpm install\nnpm run build'),
             ('Configure Nginx', 'Setup reverse proxy.', 'sudo nano /etc/nginx/sites-available/myapp\n\nserver {\n    listen 80;\n    server_name myapp.com;\n    root /var/www/app/build;\n    index index.html;\n    location /api {\n        proxy_pass http://localhost:8000;\n    }\n}'),
             ('SSL with Certbot', 'Add HTTPS.', 'sudo apt install certbot python3-certbot-nginx -y\nsudo certbot --nginx -d myapp.com\nsudo systemctl reload nginx')]),
    ],
    'billing': [
        lambda os: art(f'Setup Invoice System on {os}', f'Install open-source invoicing system on {os}.', 'billing', [os.lower()], 'intermediate', ['invoice', 'billing', 'php', os.lower()],
            [('Install LAMP Stack', 'Setup PHP environment.', 'sudo apt update\nsudo apt install apache2 mysql-server php php-mysql php-curl php-gd php-zip php-mbstring -y'),
             ('Setup Database', 'Create billing database.', 'sudo mysql -u root -p\nCREATE DATABASE billing_db;\nCREATE USER \'billing\'@\'localhost\' IDENTIFIED BY \'secure_pass\';\nGRANT ALL ON billing_db.* TO \'billing\'@\'localhost\';\nFLUSH PRIVILEGES;'),
             ('Deploy Application', 'Install and configure.', 'cd /var/www/html\nsudo wget https://example.com/invoice-app.zip\nsudo unzip invoice-app.zip\nsudo chown -R www-data:www-data /var/www/html/\nsudo systemctl restart apache2')]),
    ],
}

OS_MAP = {
    'ubuntu': 'Ubuntu', 'centos': 'CentOS', 'debian': 'Debian',
    'rhel': 'RHEL', 'fedora': 'Fedora', 'linux': 'Linux',
    'windows': 'Windows', 'mac': 'macOS',
}

class SeedRequest(BaseModel):
    category: str
    os: Optional[str] = None

class SeedPreview(BaseModel):
    category: str

@router.get("/categories")
async def get_seed_categories():
    """Get all available categories and OS options for seeding"""
    cats = list(TEMPLATES.keys())
    oses = list(OS_MAP.items())
    return {"categories": cats, "operating_systems": [{"slug": k, "name": v} for k, v in oses]}

@router.post("/preview")
async def preview_seed(req: SeedRequest):
    """Preview what articles would be created"""
    templates = TEMPLATES.get(req.category, [])
    if not templates:
        raise HTTPException(status_code=400, detail=f"No templates for category: {req.category}")
    os_name = OS_MAP.get(req.os, 'Ubuntu') if req.os else 'Ubuntu'
    articles = [t(os_name) for t in templates]
    # Check which already exist
    results = []
    for a in articles:
        existing = await snippets_collection.find_one({'title': a['title']})
        results.append({
            'title': a['title'],
            'category': a['category'],
            'difficulty': a['difficulty'],
            'os': a['os'],
            'tags': a['tags'],
            'exists': existing is not None,
        })
    return {"articles": results, "total": len(results), "new": sum(1 for r in results if not r['exists'])}

@router.post("/seed")
async def seed_articles(req: SeedRequest):
    """Seed articles for a category + OS combination"""
    templates = TEMPLATES.get(req.category, [])
    if not templates:
        raise HTTPException(status_code=400, detail=f"No templates for category: {req.category}")
    os_name = OS_MAP.get(req.os, 'Ubuntu') if req.os else 'Ubuntu'
    articles = [t(os_name) for t in templates]
    added = 0
    skipped = 0
    for a in articles:
        existing = await snippets_collection.find_one({'title': a['title']})
        if existing:
            skipped += 1
            continue
        await snippets_collection.insert_one(a)
        added += 1
    total = await snippets_collection.count_documents({})
    return {"added": added, "skipped": skipped, "total_articles": total, "message": f"{added} articles added, {skipped} skipped (duplicates)"}
