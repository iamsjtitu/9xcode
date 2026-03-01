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

CONFIGURATION_ARTICLES = [
    {
        'title': 'Configure SSH Server Security on Linux',
        'description': 'Harden SSH server configuration for better security on Linux servers.',
        'category': 'configuration',
        'os': ['ubuntu', 'centos', 'linux'],
        'difficulty': 'intermediate',
        'tags': ['ssh', 'security', 'configuration', 'linux', 'hardening'],
        'steps': [
            {'title': 'Backup SSH Config', 'description': 'Create backup before changes.', 'code': 'sudo cp /etc/ssh/sshd_config /etc/ssh/sshd_config.backup', 'language': 'bash'},
            {'title': 'Change Default Port', 'description': 'Change SSH from port 22.', 'code': 'sudo nano /etc/ssh/sshd_config\n\n# Change port (choose random port 1024-65535)\nPort 2222\n\n# Update firewall\nsudo ufw allow 2222/tcp\nsudo ufw delete allow 22/tcp', 'language': 'bash'},
            {'title': 'Disable Root Login', 'description': 'Prevent direct root access.', 'code': '# In sshd_config\nPermitRootLogin no\n\n# Or allow only with key\nPermitRootLogin prohibit-password', 'language': 'bash'},
            {'title': 'Key-Only Authentication', 'description': 'Disable password login.', 'code': '# In sshd_config\nPasswordAuthentication no\nPubkeyAuthentication yes\nChallengeResponseAuthentication no\nUsePAM yes\n\n# Make sure you have SSH key setup first!\n# On client: ssh-keygen\n# Copy to server: ssh-copy-id user@server', 'language': 'bash'},
            {'title': 'Additional Hardening', 'description': 'More security options.', 'code': '# In sshd_config\n\n# Limit login attempts\nMaxAuthTries 3\n\n# Limit concurrent sessions\nMaxSessions 2\n\n# Idle timeout (10 min)\nClientAliveInterval 300\nClientAliveCountMax 2\n\n# Disable empty passwords\nPermitEmptyPasswords no\n\n# Disable X11 forwarding\nX11Forwarding no\n\n# Allow specific users only\nAllowUsers youruser admin\n\n# Restart SSH\nsudo systemctl restart sshd', 'language': 'bash'}
        ],
        'postInstallation': {'title': 'Important', 'content': 'Test SSH in new terminal before closing current session! Use: ssh -p 2222 user@server. Consider fail2ban for brute-force protection.'}
    },
    {
        'title': 'Configure Linux Swap Space',
        'description': 'Create and configure swap file or partition on Linux servers.',
        'category': 'configuration',
        'os': ['ubuntu', 'centos', 'linux'],
        'difficulty': 'beginner',
        'tags': ['swap', 'memory', 'linux', 'configuration'],
        'steps': [
            {'title': 'Check Existing Swap', 'description': 'View current swap configuration.', 'code': '# Check swap usage\nfree -h\n\n# Show swap devices\nswapon --show\n\n# Detailed memory info\ncat /proc/meminfo | grep -i swap', 'language': 'bash'},
            {'title': 'Create Swap File', 'description': 'Create a new swap file.', 'code': '# Create 4GB swap file\nsudo fallocate -l 4G /swapfile\n\n# Or using dd (slower but more compatible)\nsudo dd if=/dev/zero of=/swapfile bs=1G count=4\n\n# Secure the file\nsudo chmod 600 /swapfile\n\n# Verify\nls -lh /swapfile', 'language': 'bash'},
            {'title': 'Enable Swap', 'description': 'Activate the swap file.', 'code': '# Mark as swap\nsudo mkswap /swapfile\n\n# Enable swap\nsudo swapon /swapfile\n\n# Verify\nfree -h\nswapon --show', 'language': 'bash'},
            {'title': 'Make Permanent', 'description': 'Add to fstab for persistence.', 'code': '# Add to fstab\necho \'/swapfile none swap sw 0 0\' | sudo tee -a /etc/fstab\n\n# Verify fstab\ncat /etc/fstab\n\n# Configure swappiness (lower = less aggressive)\necho \'vm.swappiness=10\' | sudo tee -a /etc/sysctl.conf\necho \'vm.vfs_cache_pressure=50\' | sudo tee -a /etc/sysctl.conf\nsudo sysctl -p', 'language': 'bash'}
        ],
        'postInstallation': {'title': 'Recommendations', 'content': 'Swap size: Equal to RAM for servers up to 2GB, half of RAM for 2-8GB, 8GB max for larger systems. SSD: Consider lower swappiness (10) to reduce writes.'}
    },
    {
        'title': 'Configure Timezone on Linux',
        'description': 'Set and manage timezone configuration on Linux servers.',
        'category': 'configuration',
        'os': ['ubuntu', 'centos', 'linux'],
        'difficulty': 'beginner',
        'tags': ['timezone', 'time', 'linux', 'configuration', 'ntp'],
        'steps': [
            {'title': 'Check Current Timezone', 'description': 'View current timezone settings.', 'code': '# Show current time and timezone\ndate\ntimedatectl\n\n# Show timezone name\ncat /etc/timezone\n\n# List available timezones\ntimedatectl list-timezones\ntimedatectl list-timezones | grep Asia', 'language': 'bash'},
            {'title': 'Set Timezone', 'description': 'Change system timezone.', 'code': '# Using timedatectl (recommended)\nsudo timedatectl set-timezone Asia/Kolkata\n\n# Or for US Eastern\nsudo timedatectl set-timezone America/New_York\n\n# Alternative method\nsudo ln -sf /usr/share/zoneinfo/Asia/Kolkata /etc/localtime\n\n# Verify\ndate\ntimedatectl', 'language': 'bash'},
            {'title': 'Configure NTP', 'description': 'Setup automatic time synchronization.', 'code': '# Enable NTP sync\nsudo timedatectl set-ntp on\n\n# Check NTP status\ntimedatectl\n\n# Install and configure chrony (recommended)\nsudo apt install -y chrony\nsudo systemctl start chronyd\nsudo systemctl enable chronyd\n\n# Check sync status\nchronyc tracking\nchronyc sources', 'language': 'bash'},
            {'title': 'Manual Time Set', 'description': 'Set time manually if needed.', 'code': '# Set date and time manually\nsudo timedatectl set-time "2024-01-15 10:30:00"\n\n# Note: Disable NTP first\nsudo timedatectl set-ntp off\nsudo timedatectl set-time "2024-01-15 10:30:00"\nsudo timedatectl set-ntp on\n\n# Using date command\nsudo date -s "15 JAN 2024 10:30:00"', 'language': 'bash'}
        ],
        'postInstallation': {'title': 'Best Practice', 'content': 'Always use NTP for time sync on servers. Use UTC for servers if managing multiple timezones. Check logs have correct timestamps after timezone change.'}
    },
    {
        'title': 'Configure UFW Firewall on Ubuntu',
        'description': 'Setup and manage UFW (Uncomplicated Firewall) on Ubuntu servers.',
        'category': 'configuration',
        'os': ['ubuntu', 'linux'],
        'difficulty': 'beginner',
        'tags': ['ufw', 'firewall', 'security', 'ubuntu', 'configuration'],
        'steps': [
            {'title': 'Install and Enable UFW', 'description': 'Setup UFW firewall.', 'code': '# Install (usually pre-installed)\nsudo apt install -y ufw\n\n# Check status\nsudo ufw status\n\n# Set default policies\nsudo ufw default deny incoming\nsudo ufw default allow outgoing', 'language': 'bash'},
            {'title': 'Allow Common Services', 'description': 'Open ports for services.', 'code': '# Allow SSH (important!)\nsudo ufw allow ssh\n# Or specific port\nsudo ufw allow 22/tcp\n\n# Allow HTTP/HTTPS\nsudo ufw allow http\nsudo ufw allow https\n# Or\nsudo ufw allow 80/tcp\nsudo ufw allow 443/tcp\n\n# Allow specific application\nsudo ufw allow \'Nginx Full\'\nsudo ufw app list  # List available apps', 'language': 'bash'},
            {'title': 'Enable UFW', 'description': 'Activate the firewall.', 'code': '# Enable firewall\nsudo ufw enable\n\n# Check status\nsudo ufw status verbose\nsudo ufw status numbered\n\n# Disable if needed\nsudo ufw disable', 'language': 'bash'},
            {'title': 'Advanced Rules', 'description': 'Create specific rules.', 'code': '# Allow from specific IP\nsudo ufw allow from 192.168.1.100\n\n# Allow to specific port from IP\nsudo ufw allow from 192.168.1.0/24 to any port 3306\n\n# Allow port range\nsudo ufw allow 6000:6007/tcp\n\n# Deny specific IP\nsudo ufw deny from 203.0.113.100\n\n# Delete rule by number\nsudo ufw status numbered\nsudo ufw delete 2\n\n# Delete rule by specification\nsudo ufw delete allow 8080', 'language': 'bash'}
        ],
        'postInstallation': {'title': 'Important', 'content': 'Always allow SSH before enabling UFW! Use ufw status numbered to manage rules. Logs at /var/log/ufw.log. Enable logging: ufw logging on'}
    },
    {
        'title': 'Configure Cron Jobs on Linux',
        'description': 'Schedule automated tasks using cron on Linux servers.',
        'category': 'configuration',
        'os': ['ubuntu', 'centos', 'linux'],
        'difficulty': 'beginner',
        'tags': ['cron', 'automation', 'scheduling', 'linux', 'configuration'],
        'steps': [
            {'title': 'Cron Syntax', 'description': 'Understand cron time format.', 'code': '# Cron format:\n# MIN HOUR DAY MONTH WEEKDAY COMMAND\n# *   *    *   *     *       command\n\n# Examples:\n# Every minute\n* * * * * /path/script.sh\n\n# Every hour at minute 0\n0 * * * * /path/script.sh\n\n# Every day at 2 AM\n0 2 * * * /path/script.sh\n\n# Every Sunday at 3 AM\n0 3 * * 0 /path/script.sh\n\n# Every 15 minutes\n*/15 * * * * /path/script.sh\n\n# First day of every month\n0 0 1 * * /path/script.sh', 'language': 'bash'},
            {'title': 'Edit Crontab', 'description': 'Add cron jobs.', 'code': '# Edit user crontab\ncrontab -e\n\n# Edit root crontab\nsudo crontab -e\n\n# List current jobs\ncrontab -l\n\n# Remove all jobs\ncrontab -r', 'language': 'bash'},
            {'title': 'System Cron Directories', 'description': 'Use predefined cron directories.', 'code': '# Place scripts in these directories:\n/etc/cron.hourly/    # Run every hour\n/etc/cron.daily/     # Run daily\n/etc/cron.weekly/    # Run weekly\n/etc/cron.monthly/   # Run monthly\n\n# Example:\nsudo nano /etc/cron.daily/backup\n#!/bin/bash\n/usr/local/bin/backup.sh\n\nsudo chmod +x /etc/cron.daily/backup', 'language': 'bash'},
            {'title': 'Cron Best Practices', 'description': 'Proper cron job setup.', 'code': '# Use full paths\n0 2 * * * /usr/bin/python3 /home/user/script.py\n\n# Redirect output to log\n0 2 * * * /path/script.sh >> /var/log/myscript.log 2>&1\n\n# Suppress output\n0 2 * * * /path/script.sh > /dev/null 2>&1\n\n# Email output (if mail configured)\nMAILTO="admin@example.com"\n0 2 * * * /path/script.sh\n\n# Set environment\nPATH=/usr/local/bin:/usr/bin:/bin\n0 2 * * * myscript', 'language': 'bash'}
        ],
        'postInstallation': {'title': 'Debugging', 'content': 'Check cron logs: grep CRON /var/log/syslog. Test scripts manually first. Use crontab.guru for schedule building. Ensure scripts are executable.'}
    },
    {
        'title': 'Configure Environment Variables on Linux',
        'description': 'Set and manage environment variables permanently on Linux.',
        'category': 'configuration',
        'os': ['ubuntu', 'centos', 'linux'],
        'difficulty': 'beginner',
        'tags': ['environment', 'variables', 'linux', 'configuration', 'bash'],
        'steps': [
            {'title': 'View Environment Variables', 'description': 'Check current variables.', 'code': '# Show all environment variables\nenv\nprintenv\n\n# Show specific variable\necho $PATH\necho $HOME\necho $USER\n\n# Show with printenv\nprintenv PATH', 'language': 'bash'},
            {'title': 'Set Temporary Variable', 'description': 'Set variable for current session.', 'code': '# Set variable (current shell only)\nexport MY_VAR="value"\n\n# Verify\necho $MY_VAR\n\n# Use in command\nexport API_KEY="abc123"\ncurl -H "Authorization: $API_KEY" https://api.example.com', 'language': 'bash'},
            {'title': 'Set Permanent Variables (User)', 'description': 'Configure user-level variables.', 'code': '# For current user - add to ~/.bashrc\nnano ~/.bashrc\n\n# Add at the end:\nexport MY_VAR="myvalue"\nexport PATH="$PATH:/home/user/bin"\nexport JAVA_HOME="/usr/lib/jvm/java-11"\n\n# Apply changes\nsource ~/.bashrc\n\n# Or add to ~/.profile for login shells\nnano ~/.profile', 'language': 'bash'},
            {'title': 'Set System-Wide Variables', 'description': 'Configure for all users.', 'code': '# Method 1: /etc/environment (simple)\nsudo nano /etc/environment\n\nMY_GLOBAL_VAR="value"\nJAVA_HOME="/usr/lib/jvm/java-11"\n\n# Method 2: /etc/profile.d/ (recommended for scripts)\nsudo nano /etc/profile.d/myenv.sh\n\nexport MY_VAR="value"\nexport PATH="$PATH:/opt/bin"\n\n# Make executable\nsudo chmod +x /etc/profile.d/myenv.sh\n\n# Logout and login to apply', 'language': 'bash'}
        ],
        'postInstallation': {'title': 'Priority Order', 'content': '1. /etc/environment 2. /etc/profile 3. /etc/profile.d/*.sh 4. ~/.profile 5. ~/.bashrc. Use .bashrc for interactive shells, .profile for login shells.'}
    },
    {
        'title': 'Configure Linux Log Rotation',
        'description': 'Setup logrotate to manage log files and prevent disk space issues.',
        'category': 'configuration',
        'os': ['ubuntu', 'centos', 'linux'],
        'difficulty': 'intermediate',
        'tags': ['logrotate', 'logs', 'linux', 'configuration', 'disk'],
        'steps': [
            {'title': 'Check Logrotate Status', 'description': 'Verify logrotate is installed.', 'code': '# Check if installed\nlogrotate --version\n\n# Main config file\ncat /etc/logrotate.conf\n\n# Application-specific configs\nls /etc/logrotate.d/', 'language': 'bash'},
            {'title': 'Create Custom Config', 'description': 'Configure rotation for application.', 'code': 'sudo nano /etc/logrotate.d/myapp\n\n/var/log/myapp/*.log {\n    daily              # Rotate daily\n    rotate 7           # Keep 7 rotated files\n    compress           # Compress rotated files\n    delaycompress      # Delay compression by 1 cycle\n    missingok          # Don\'t error if log missing\n    notifempty         # Don\'t rotate empty files\n    create 0640 www-data www-data  # New file permissions\n    sharedscripts      # Run scripts once for all logs\n    postrotate\n        systemctl reload myapp > /dev/null 2>&1 || true\n    endscript\n}', 'language': 'bash'},
            {'title': 'Nginx Log Rotation Example', 'description': 'Configure Nginx log rotation.', 'code': 'sudo nano /etc/logrotate.d/nginx\n\n/var/log/nginx/*.log {\n    daily\n    rotate 14\n    compress\n    delaycompress\n    notifempty\n    missingok\n    sharedscripts\n    postrotate\n        [ -f /var/run/nginx.pid ] && kill -USR1 `cat /var/run/nginx.pid`\n    endscript\n}', 'language': 'bash'},
            {'title': 'Test and Debug', 'description': 'Test logrotate configuration.', 'code': '# Test config (dry run)\nsudo logrotate -d /etc/logrotate.d/myapp\n\n# Force rotation (for testing)\nsudo logrotate -f /etc/logrotate.d/myapp\n\n# Check last rotation\ncat /var/lib/logrotate/status\n\n# Run logrotate manually\nsudo logrotate /etc/logrotate.conf\n\n# Debug verbose\nsudo logrotate -v /etc/logrotate.conf', 'language': 'bash'}
        ],
        'postInstallation': {'title': 'Options', 'content': 'Rotation options: daily, weekly, monthly, yearly. Size-based: size 100M, minsize 100M, maxsize 100M. Use copytruncate for logs that can\'t be closed.'}
    },
    {
        'title': 'Configure System Limits on Linux',
        'description': 'Set ulimit and system limits for better performance and security.',
        'category': 'configuration',
        'os': ['ubuntu', 'centos', 'linux'],
        'difficulty': 'intermediate',
        'tags': ['ulimit', 'limits', 'linux', 'configuration', 'performance'],
        'steps': [
            {'title': 'Check Current Limits', 'description': 'View current system limits.', 'code': '# Show all limits\nulimit -a\n\n# Specific limits\nulimit -n  # Open files\nulimit -u  # Max processes\nulimit -v  # Virtual memory\n\n# System-wide limits\ncat /proc/sys/fs/file-max', 'language': 'bash'},
            {'title': 'Set Temporary Limits', 'description': 'Change limits for current session.', 'code': '# Increase open files (current session)\nulimit -n 65535\n\n# Increase max processes\nulimit -u 65535\n\n# Note: Can\'t exceed hard limit', 'language': 'bash'},
            {'title': 'Set Permanent Limits', 'description': 'Configure permanent limits.', 'code': 'sudo nano /etc/security/limits.conf\n\n# Format: <user/group> <soft/hard> <item> <value>\n\n# For all users\n*               soft    nofile          65535\n*               hard    nofile          65535\n*               soft    nproc           65535\n*               hard    nproc           65535\n\n# For specific user\nnginx           soft    nofile          65535\nnginx           hard    nofile          65535\nmysql           soft    nofile          65535\nmysql           hard    nofile          65535\n\n# For root\nroot            soft    nofile          65535\nroot            hard    nofile          65535', 'language': 'bash'},
            {'title': 'System-Wide Settings', 'description': 'Configure kernel parameters.', 'code': 'sudo nano /etc/sysctl.conf\n\n# Increase file handles\nfs.file-max = 2097152\n\n# Network optimizations\nnet.core.somaxconn = 65535\nnet.core.netdev_max_backlog = 65535\nnet.ipv4.tcp_max_syn_backlog = 65535\n\n# Apply changes\nsudo sysctl -p\n\n# Verify\ncat /proc/sys/fs/file-max', 'language': 'bash'}
        ],
        'postInstallation': {'title': 'Important', 'content': 'Logout and login for limits.conf changes. For services, add LimitNOFILE=65535 in systemd unit file. Check application requirements for recommended limits.'}
    }
]

async def seed_configuration():
    print("=" * 60)
    print("  SEEDING: Configuration Articles")
    print("=" * 60)
    
    added = 0
    for article in CONFIGURATION_ARTICLES:
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
    
    print(f"\n✓ Added {added} Configuration articles")
    total = await db.code_snippets.count_documents({'category': 'configuration'})
    print(f"Total Configuration articles: {total}")

if __name__ == "__main__":
    asyncio.run(seed_configuration())
