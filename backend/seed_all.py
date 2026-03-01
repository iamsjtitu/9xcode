"""
9xCodes Master Seeder - Consolidated Seeder Utility
Usage: python seed_all.py [--force] [--category CATEGORY] [--dry-run]

Options:
  --force      Seed even if articles already exist (skips duplicates by title)
  --category   Seed only a specific category
  --dry-run    Show what would be added without inserting
"""
from motor.motor_asyncio import AsyncIOMotorClient
import os, re, asyncio, uuid, argparse
from dotenv import load_dotenv
from pathlib import Path
from datetime import datetime

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

def create_slug(title):
    slug = title.lower()
    slug = re.sub(r'[^a-z0-9]+', '-', slug)
    return slug.strip('-')

def article(title, desc, category, os_list, difficulty, tags, steps, post=None):
    return {
        'id': str(uuid.uuid4()),
        'title': title,
        'slug': create_slug(title),
        'description': desc,
        'category': category,
        'os': os_list,
        'difficulty': difficulty,
        'views': 0,
        'likes': 0,
        'author': 'Admin',
        'createdAt': datetime.utcnow(),
        'updatedAt': datetime.utcnow(),
        'tags': tags,
        'steps': steps,
        'postInstallation': post,
    }

def step(title, desc, code, lang='bash'):
    return {'title': title, 'description': desc, 'code': code, 'language': lang}

# ===================== ALL ARTICLES BY CATEGORY =====================

ARTICLES = [
    # --- INSTALLATION ---
    article(
        'Install Node.js via NVM', 'Install and manage multiple Node.js versions using NVM.',
        'installation', ['ubuntu', 'linux'], 'beginner', ['nodejs', 'nvm', 'javascript'],
        [step('Install NVM', 'Download and run NVM installer.', 'curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash\nsource ~/.bashrc'),
         step('Install Node.js', 'Install latest LTS version.', 'nvm install --lts\nnvm use --lts\nnode -v && npm -v'),
         step('Set Default Version', 'Set default Node.js version.', 'nvm alias default lts/*\nnvm list')]
    ),
    article(
        'Install Python 3.12 from Source', 'Compile and install Python 3.12 on Linux.',
        'installation', ['ubuntu', 'centos', 'linux'], 'intermediate', ['python', 'compile', 'source'],
        [step('Install Dependencies', 'Install build dependencies.', 'sudo apt update\nsudo apt install build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libreadline-dev libffi-dev libsqlite3-dev wget -y'),
         step('Download Python Source', 'Get Python 3.12 tarball.', 'cd /tmp\nwget https://www.python.org/ftp/python/3.12.0/Python-3.12.0.tgz\ntar -xf Python-3.12.0.tgz'),
         step('Compile and Install', 'Build Python from source.', 'cd Python-3.12.0\n./configure --enable-optimizations\nmake -j $(nproc)\nsudo make altinstall'),
         step('Verify', 'Check installation.', 'python3.12 --version\npip3.12 --version')]
    ),
    article(
        'Install Redis Server', 'Setup Redis in-memory data store on Linux.',
        'installation', ['ubuntu', 'centos'], 'beginner', ['redis', 'cache', 'nosql'],
        [step('Install Redis', 'Install using package manager.', '# Ubuntu\nsudo apt update && sudo apt install redis-server -y\n\n# CentOS\nsudo yum install redis -y'),
         step('Configure Redis', 'Set supervised mode.', 'sudo sed -i "s/supervised no/supervised systemd/" /etc/redis/redis.conf'),
         step('Start Redis', 'Enable and start service.', 'sudo systemctl enable redis-server\nsudo systemctl start redis-server\nsudo systemctl status redis-server'),
         step('Test Redis', 'Verify it works.', 'redis-cli ping\n# Should output: PONG')]
    ),

    # --- SECURITY ---
    article(
        'Setup Let\'s Encrypt SSL with Certbot', 'Free SSL certificates for your domain using Certbot.',
        'security', ['ubuntu', 'debian'], 'beginner', ['ssl', 'certbot', 'letsencrypt', 'https'],
        [step('Install Certbot', 'Install Certbot with Nginx plugin.', 'sudo apt update\nsudo apt install certbot python3-certbot-nginx -y'),
         step('Obtain Certificate', 'Get SSL certificate for your domain.', 'sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com'),
         step('Auto-Renewal', 'Setup automatic renewal.', 'sudo certbot renew --dry-run\nsudo systemctl enable certbot.timer'),
         step('Verify SSL', 'Check certificate status.', 'sudo certbot certificates\ncurl -I https://yourdomain.com')]
    ),
    article(
        'Setup Two-Factor Authentication for SSH', 'Add Google Authenticator 2FA to SSH login.',
        'security', ['ubuntu', 'linux'], 'advanced', ['2fa', 'ssh', 'google-authenticator'],
        [step('Install Google Authenticator', 'Install the PAM module.', 'sudo apt install libpam-google-authenticator -y'),
         step('Configure for User', 'Run setup as the target user.', 'google-authenticator\n# Answer yes to time-based tokens\n# Scan QR code with authenticator app'),
         step('Configure PAM', 'Enable 2FA in PAM.', 'sudo nano /etc/pam.d/sshd\n# Add at end:\nauth required pam_google_authenticator.so'),
         step('Update SSH Config', 'Enable challenge-response.', 'sudo nano /etc/ssh/sshd_config\n# Set:\nChallengeResponseAuthentication yes\nAuthenticationMethods publickey,keyboard-interactive\n\nsudo systemctl restart sshd')]
    ),

    # --- NETWORKING ---
    article(
        'Configure Static IP Address', 'Set static IP on Ubuntu using Netplan.',
        'networking', ['ubuntu'], 'beginner', ['ip', 'netplan', 'static-ip', 'network'],
        [step('Identify Interface', 'Find your network interface name.', 'ip link show\n# Note your interface name (e.g., eth0, ens33)'),
         step('Edit Netplan Config', 'Configure static IP.', 'sudo nano /etc/netplan/01-netcfg.yaml\n\nnetwork:\n  version: 2\n  ethernets:\n    eth0:\n      addresses:\n        - 192.168.1.100/24\n      routes:\n        - to: default\n          via: 192.168.1.1\n      nameservers:\n        addresses: [8.8.8.8, 8.8.4.4]', 'yaml'),
         step('Apply Configuration', 'Apply the network changes.', 'sudo netplan apply\nip addr show eth0')]
    ),
    article(
        'Setup WireGuard VPN Server', 'Modern, fast VPN using WireGuard protocol.',
        'networking', ['ubuntu', 'linux'], 'advanced', ['vpn', 'wireguard', 'tunnel'],
        [step('Install WireGuard', 'Install WireGuard tools.', 'sudo apt update\nsudo apt install wireguard -y'),
         step('Generate Keys', 'Create server key pair.', 'wg genkey | tee /etc/wireguard/server_private.key | wg pubkey > /etc/wireguard/server_public.key\nchmod 600 /etc/wireguard/server_private.key'),
         step('Configure Server', 'Create WireGuard config.', 'cat > /etc/wireguard/wg0.conf << EOF\n[Interface]\nAddress = 10.0.0.1/24\nListenPort = 51820\nPrivateKey = $(cat /etc/wireguard/server_private.key)\nPostUp = iptables -A FORWARD -i wg0 -j ACCEPT\nPostDown = iptables -D FORWARD -i wg0 -j ACCEPT\nEOF'),
         step('Start VPN', 'Enable and start the VPN.', 'sudo systemctl enable wg-quick@wg0\nsudo systemctl start wg-quick@wg0\nsudo wg show')]
    ),

    # --- DATABASE ---
    article(
        'PostgreSQL Backup and Restore', 'Complete guide to backup and restore PostgreSQL databases.',
        'database', ['ubuntu', 'linux'], 'intermediate', ['postgresql', 'backup', 'pg_dump'],
        [step('Full Database Backup', 'Create a complete backup.', 'pg_dump -U postgres -h localhost mydb > backup_$(date +%Y%m%d).sql\n\n# Compressed backup\npg_dump -U postgres -Fc mydb > backup_$(date +%Y%m%d).dump'),
         step('Backup All Databases', 'Dump all databases at once.', 'pg_dumpall -U postgres > all_databases_$(date +%Y%m%d).sql'),
         step('Restore Database', 'Restore from backup file.', '# From SQL backup\npsql -U postgres mydb < backup.sql\n\n# From compressed dump\npg_restore -U postgres -d mydb backup.dump'),
         step('Automate with Cron', 'Schedule daily backups.', 'crontab -e\n# Add:\n0 2 * * * pg_dump -U postgres -Fc mydb > /backups/mydb_$(date +\\%Y\\%m\\%d).dump')]
    ),

    # --- MONITORING ---
    article(
        'Setup Prometheus and Grafana Monitoring', 'Complete monitoring stack with alerting.',
        'monitoring', ['ubuntu', 'linux'], 'advanced', ['prometheus', 'grafana', 'monitoring', 'alerting'],
        [step('Install Prometheus', 'Download and install Prometheus.', 'wget https://github.com/prometheus/prometheus/releases/download/v2.48.0/prometheus-2.48.0.linux-amd64.tar.gz\ntar xvf prometheus-*.tar.gz\nsudo mv prometheus-*/prometheus /usr/local/bin/\nsudo mv prometheus-*/promtool /usr/local/bin/'),
         step('Configure Prometheus', 'Create config file.', 'sudo mkdir /etc/prometheus\ncat > /etc/prometheus/prometheus.yml << EOF\nglobal:\n  scrape_interval: 15s\nscrape_configs:\n  - job_name: "node"\n    static_configs:\n      - targets: ["localhost:9100"]\nEOF', 'yaml'),
         step('Install Grafana', 'Install Grafana for dashboards.', 'sudo apt install -y apt-transport-https software-properties-common\nwget -q -O - https://packages.grafana.com/gpg.key | sudo apt-key add -\nsudo add-apt-repository "deb https://packages.grafana.com/oss/deb stable main"\nsudo apt update && sudo apt install grafana -y'),
         step('Start Services', 'Enable and start both services.', 'sudo systemctl enable --now prometheus\nsudo systemctl enable --now grafana-server\necho "Grafana: http://localhost:3000 (admin/admin)"')]
    ),

    # --- CONFIGURATION ---
    article(
        'Configure Nginx as Reverse Proxy', 'Setup Nginx reverse proxy for Node.js, Python apps.',
        'configuration', ['ubuntu', 'linux'], 'intermediate', ['nginx', 'reverse-proxy', 'proxy'],
        [step('Create Server Block', 'Configure Nginx for your app.', 'sudo nano /etc/nginx/sites-available/myapp\n\nserver {\n    listen 80;\n    server_name myapp.com;\n\n    location / {\n        proxy_pass http://localhost:3000;\n        proxy_http_version 1.1;\n        proxy_set_header Upgrade $http_upgrade;\n        proxy_set_header Connection \'upgrade\';\n        proxy_set_header Host $host;\n        proxy_cache_bypass $http_upgrade;\n    }\n}'),
         step('Enable Site', 'Link and test config.', 'sudo ln -s /etc/nginx/sites-available/myapp /etc/nginx/sites-enabled/\nsudo nginx -t\nsudo systemctl reload nginx'),
         step('Add SSL', 'Secure with Let\'s Encrypt.', 'sudo certbot --nginx -d myapp.com')]
    ),
    article(
        'Setup Cron Jobs for Task Automation', 'Schedule recurring tasks with crontab.',
        'configuration', ['ubuntu', 'centos', 'linux'], 'beginner', ['cron', 'automation', 'scheduling'],
        [step('Edit Crontab', 'Open cron editor.', 'crontab -e\n\n# Cron format:\n# MIN HOUR DOM MON DOW COMMAND\n# *    *    *   *   *'),
         step('Common Examples', 'Useful cron schedules.', '# Every day at midnight\n0 0 * * * /path/to/script.sh\n\n# Every 5 minutes\n*/5 * * * * /path/to/check.sh\n\n# Every Monday at 9 AM\n0 9 * * 1 /path/to/weekly.sh\n\n# First of every month\n0 0 1 * * /path/to/monthly.sh'),
         step('View and Manage', 'List and manage cron jobs.', 'crontab -l          # List all cron jobs\ncrontab -r          # Remove all cron jobs\nsudo crontab -u user -l  # View other user\'s cron')]
    ),

    # --- BACKUP ---
    article(
        'Setup Rsync for Remote Backups', 'Efficient file sync and backup with rsync.',
        'backup', ['ubuntu', 'centos', 'linux'], 'intermediate', ['rsync', 'backup', 'sync', 'remote'],
        [step('Basic Rsync Usage', 'Sync files locally or remotely.', '# Local sync\nrsync -avh /source/ /destination/\n\n# Remote sync\nrsync -avhz -e ssh /local/path/ user@remote:/remote/path/'),
         step('Incremental Backup Script', 'Create backup script with rotation.', '#!/bin/bash\nDATE=$(date +%Y-%m-%d)\nSRC="/var/www/"\nDEST="/backup/$DATE"\nrsync -avh --delete --link-dest=/backup/latest $SRC $DEST\nln -sfn $DEST /backup/latest'),
         step('Schedule with Cron', 'Automate daily backups.', 'chmod +x /usr/local/bin/backup.sh\ncrontab -e\n# Add:\n0 3 * * * /usr/local/bin/backup.sh >> /var/log/backup.log 2>&1')]
    ),

    # --- VIRTUALIZATION ---
    article(
        'Getting Started with Docker Compose', 'Multi-container applications with Docker Compose.',
        'virtualization', ['ubuntu', 'linux'], 'intermediate', ['docker', 'docker-compose', 'containers'],
        [step('Create docker-compose.yml', 'Define multi-container app.', 'version: "3.8"\nservices:\n  web:\n    image: nginx:alpine\n    ports:\n      - "80:80"\n    volumes:\n      - ./html:/usr/share/nginx/html\n  db:\n    image: mysql:8\n    environment:\n      MYSQL_ROOT_PASSWORD: secret\n      MYSQL_DATABASE: myapp\n    volumes:\n      - db_data:/var/lib/mysql\nvolumes:\n  db_data:', 'yaml'),
         step('Common Commands', 'Manage your containers.', 'docker compose up -d        # Start in background\ndocker compose down          # Stop and remove\ndocker compose logs -f       # Follow logs\ndocker compose ps            # List containers\ndocker compose exec web sh   # Shell into container')]
    ),

    # --- WEB HOSTING ---
    article(
        'Deploy Node.js App with PM2', 'Production Node.js deployment with PM2 process manager.',
        'web-hosting', ['ubuntu', 'linux'], 'intermediate', ['nodejs', 'pm2', 'deployment', 'production'],
        [step('Install PM2', 'Install PM2 globally.', 'npm install -g pm2'),
         step('Start Application', 'Launch with PM2.', 'pm2 start app.js --name myapp\npm2 start npm --name myapp -- start  # For npm start\npm2 start ecosystem.config.js        # Using config'),
         step('PM2 Management', 'Monitor and manage processes.', 'pm2 list             # List all processes\npm2 monit            # Real-time monitoring\npm2 logs myapp       # View logs\npm2 restart myapp    # Restart\npm2 stop myapp       # Stop'),
         step('Auto-Start on Boot', 'Configure PM2 startup.', 'pm2 startup systemd\npm2 save')]
    ),

    # --- COMPUTERS ---
    article(
        'Windows PowerShell Essential Commands', 'Key PowerShell commands for system administration.',
        'computers', ['windows'], 'beginner', ['powershell', 'windows', 'commands', 'admin'],
        [step('System Information', 'Get system details.', 'Get-ComputerInfo | Select-Object CsName, OsName, OsArchitecture\nGet-WmiObject -Class Win32_OperatingSystem | Select-Object Caption, Version\nGet-Process | Sort-Object CPU -Descending | Select-Object -First 10', 'powershell'),
         step('File Operations', 'File management commands.', 'Get-ChildItem -Path C:\\ -Recurse -Filter "*.log"\nCopy-Item -Path "C:\\source" -Destination "C:\\dest" -Recurse\nRemove-Item -Path "C:\\temp\\*" -Recurse -Force', 'powershell'),
         step('Network Commands', 'Network diagnostics.', 'Test-NetConnection -ComputerName google.com -Port 443\nGet-NetIPAddress | Where-Object {$_.AddressFamily -eq "IPv4"}\nResolve-DnsName google.com', 'powershell')]
    ),

    # --- LEARNING ---
    article(
        'Git Essential Commands Cheatsheet', 'Must-know Git commands for daily development.',
        'learning', ['linux', 'windows', 'mac'], 'beginner', ['git', 'version-control', 'github'],
        [step('Setup and Init', 'Configure Git and create repos.', 'git config --global user.name "Your Name"\ngit config --global user.email "you@email.com"\ngit init\ngit clone https://github.com/user/repo.git'),
         step('Daily Workflow', 'Common daily commands.', 'git status                    # Check status\ngit add .                     # Stage all changes\ngit commit -m "message"       # Commit\ngit push origin main          # Push to remote\ngit pull origin main          # Pull latest'),
         step('Branching', 'Work with branches.', 'git branch feature-x          # Create branch\ngit checkout feature-x         # Switch branch\ngit checkout -b feature-y      # Create and switch\ngit merge feature-x            # Merge branch\ngit branch -d feature-x        # Delete branch'),
         step('Undo Changes', 'Revert and reset.', 'git stash                     # Stash changes\ngit stash pop                 # Apply stashed\ngit reset --soft HEAD~1       # Undo last commit (keep changes)\ngit reset --hard HEAD~1       # Undo last commit (discard)\ngit revert <commit-hash>      # Revert specific commit')]
    ),

    # --- CCTV ---
    article(
        'Setup IP Camera with RTSP Stream', 'Configure RTSP streaming from IP cameras.',
        'cctv-cameras', ['linux', 'windows'], 'intermediate', ['rtsp', 'ip-camera', 'streaming', 'cctv'],
        [step('Find Camera RTSP URL', 'Common RTSP URL formats.', '# Common formats:\nrtsp://admin:password@192.168.1.100:554/stream1\nrtsp://admin:password@192.168.1.100/cam/realmonitor?channel=1&subtype=0\n\n# Test with VLC:\nvlc rtsp://admin:password@192.168.1.100:554/stream1'),
         step('Record with FFmpeg', 'Save RTSP stream to file.', 'ffmpeg -i rtsp://admin:pass@192.168.1.100:554/stream1 \\\n  -c copy -f segment -segment_time 3600 \\\n  -strftime 1 "/recordings/%Y-%m-%d_%H-%M-%S.mp4"'),
         step('Auto-Record Script', 'Create recording service.', '#!/bin/bash\nCAM_URL="rtsp://admin:pass@192.168.1.100:554/stream1"\nOUT_DIR="/recordings/$(date +%Y-%m-%d)"\nmkdir -p "$OUT_DIR"\nffmpeg -i "$CAM_URL" -c copy -f segment -segment_time 3600 "$OUT_DIR/cam1_%H-%M-%S.mp4"')]
    ),

    # --- BILLING ---
    article(
        'Setup WHMCS Billing System', 'Install and configure WHMCS for web hosting billing.',
        'billing', ['ubuntu', 'linux'], 'advanced', ['whmcs', 'billing', 'hosting', 'automation'],
        [step('Prerequisites', 'Install required components.', 'sudo apt update\nsudo apt install apache2 mysql-server php php-mysql php-curl php-gd php-mbstring php-xml php-zip -y\nsudo systemctl enable apache2 mysql'),
         step('Create Database', 'Setup MySQL database for WHMCS.', 'sudo mysql -u root -p\nCREATE DATABASE whmcs;\nCREATE USER \'whmcs_user\'@\'localhost\' IDENTIFIED BY \'strong_password\';\nGRANT ALL PRIVILEGES ON whmcs.* TO \'whmcs_user\'@\'localhost\';\nFLUSH PRIVILEGES;\nEXIT;', 'sql'),
         step('Configure Apache', 'Set up virtual host.', 'sudo nano /etc/apache2/sites-available/billing.conf\n<VirtualHost *:80>\n    ServerName billing.yourdomain.com\n    DocumentRoot /var/www/whmcs\n    <Directory /var/www/whmcs>\n        AllowOverride All\n    </Directory>\n</VirtualHost>'),
         step('Secure Installation', 'Post-install security.', 'chmod 400 /var/www/whmcs/configuration.php\nmv /var/www/whmcs/install /var/www/whmcs/install_disabled\nsudo certbot --apache -d billing.yourdomain.com')]
    ),
]

async def seed(force=False, category=None, dry_run=False):
    articles_to_seed = ARTICLES
    if category:
        articles_to_seed = [a for a in ARTICLES if a['category'] == category]
        print(f"Filtered to {len(articles_to_seed)} articles for category: {category}")

    added = 0
    skipped = 0
    for art in articles_to_seed:
        existing = await db.code_snippets.find_one({'title': art['title']})
        if existing:
            skipped += 1
            continue
        if dry_run:
            print(f"  [DRY-RUN] Would add: {art['title']} ({art['category']})")
            added += 1
            continue
        await db.code_snippets.insert_one(art)
        print(f"  Added: {art['title']}")
        added += 1

    total = await db.code_snippets.count_documents({})
    print(f"\nResults: {added} added, {skipped} skipped (duplicates)")
    print(f"Total articles in database: {total}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='9xCodes Master Seeder')
    parser.add_argument('--force', action='store_true', help='Seed even if articles exist')
    parser.add_argument('--category', type=str, help='Seed specific category only')
    parser.add_argument('--dry-run', action='store_true', help='Show what would be added')
    args = parser.parse_args()
    asyncio.run(seed(force=args.force, category=args.category, dry_run=args.dry_run))
