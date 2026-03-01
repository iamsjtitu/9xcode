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

CENTOS_ARTICLES = [
    {
        'title': 'CentOS Stream 9 Server Installation Guide',
        'description': 'Complete guide to install CentOS Stream 9 as a server operating system.',
        'category': 'installation',
        'subcategory': 'centos',
        'os': ['centos', 'rhel', 'linux'],
        'difficulty': 'beginner',
        'tags': ['centos', 'installation', 'server', 'linux', 'rhel'],
        'steps': [
            {'title': 'Download CentOS Stream', 'description': 'Get the ISO file.', 'code': 'Download from:\nhttps://www.centos.org/centos-stream/\n\nChoose:\n- CentOS Stream 9 DVD ISO\n- Or Boot ISO (network install)\n\nVerify checksum:\nsha256sum CentOS-Stream-9-latest-x86_64-dvd1.iso', 'language': 'bash'},
            {'title': 'Create Bootable USB', 'description': 'Create installation media.', 'code': '# Linux:\nsudo dd if=CentOS-Stream-9-*.iso of=/dev/sdX bs=4M status=progress sync\n\n# Windows:\n# Use Rufus (DD mode)\n\n# Verify USB:\nlsblk', 'language': 'bash'},
            {'title': 'Install CentOS', 'description': 'Follow Anaconda installer.', 'code': 'Installation Steps:\n1. Boot from USB\n2. Select "Install CentOS Stream 9"\n3. Choose language\n4. Installation Summary:\n   - Keyboard\n   - Time & Date\n   - Installation Destination (select disk)\n   - Network & Host Name (enable, set hostname)\n   - Software Selection:\n     * Server with GUI\n     * Server\n     * Minimal Install\n5. Root Password\n6. Create User\n7. Begin Installation\n8. Reboot', 'language': 'bash'},
            {'title': 'Post-Installation Setup', 'description': 'Initial configuration.', 'code': '# Update system\nsudo dnf update -y\n\n# Install EPEL repository\nsudo dnf install epel-release -y\n\n# Install common tools\nsudo dnf install -y vim wget curl git htop net-tools\n\n# Configure firewall\nsudo systemctl start firewalld\nsudo systemctl enable firewalld\nsudo firewall-cmd --permanent --add-service=ssh\nsudo firewall-cmd --reload\n\n# Disable SELinux (optional, not recommended)\nsudo setenforce 0\nsudo sed -i \'s/SELINUX=enforcing/SELINUX=permissive/\' /etc/selinux/config', 'language': 'bash'}
        ],
        'postInstallation': {'title': 'Next Steps', 'content': 'Configure static IP in /etc/sysconfig/network-scripts/ or use nmcli. Setup SSH keys. Install required services. Consider using Cockpit for web-based management.'}
    },
    {
        'title': 'CentOS DNF Package Manager Guide',
        'description': 'Master DNF package management commands on CentOS and RHEL systems.',
        'category': 'configuration',
        'subcategory': 'centos',
        'os': ['centos', 'rhel', 'linux'],
        'difficulty': 'beginner',
        'tags': ['centos', 'dnf', 'yum', 'package-manager', 'linux'],
        'steps': [
            {'title': 'Update System', 'description': 'Keep system up to date.', 'code': '# Check for updates\nsudo dnf check-update\n\n# Update all packages\nsudo dnf update -y\n\n# Upgrade (same as update in DNF)\nsudo dnf upgrade -y\n\n# Update specific package\nsudo dnf update nginx', 'language': 'bash'},
            {'title': 'Install and Remove', 'description': 'Manage packages.', 'code': '# Install package\nsudo dnf install nginx -y\n\n# Install multiple packages\nsudo dnf install nginx mariadb-server php -y\n\n# Install from URL\nsudo dnf install https://example.com/package.rpm\n\n# Remove package\nsudo dnf remove nginx\n\n# Remove with dependencies\nsudo dnf autoremove', 'language': 'bash'},
            {'title': 'Search and Info', 'description': 'Find package information.', 'code': '# Search packages\ndnf search nginx\n\n# Get package info\ndnf info nginx\n\n# List installed packages\ndnf list installed\n\n# List available packages\ndnf list available\n\n# What provides a file\ndnf provides /usr/bin/vim\n\n# Package history\ndnf history', 'language': 'bash'},
            {'title': 'Repository Management', 'description': 'Manage DNF repositories.', 'code': '# List repositories\ndnf repolist\ndnf repolist all\n\n# Enable repository\nsudo dnf config-manager --enable powertools\n\n# Disable repository\nsudo dnf config-manager --disable epel\n\n# Add repository\nsudo dnf config-manager --add-repo https://example.com/repo.repo\n\n# Install EPEL\nsudo dnf install epel-release -y\n\n# Clean cache\nsudo dnf clean all', 'language': 'bash'}
        ],
        'postInstallation': {'title': 'DNF vs YUM', 'content': 'DNF is the successor to YUM. Most YUM commands work with DNF. DNF is faster and handles dependencies better. Config file: /etc/dnf/dnf.conf'}
    },
    {
        'title': 'CentOS Firewalld Configuration',
        'description': 'Configure firewall using firewalld on CentOS and RHEL.',
        'category': 'security',
        'subcategory': 'centos',
        'os': ['centos', 'rhel', 'linux'],
        'difficulty': 'intermediate',
        'tags': ['centos', 'firewalld', 'firewall', 'security', 'linux'],
        'steps': [
            {'title': 'Firewalld Basics', 'description': 'Start and check firewalld.', 'code': '# Start firewalld\nsudo systemctl start firewalld\nsudo systemctl enable firewalld\n\n# Check status\nsudo systemctl status firewalld\nsudo firewall-cmd --state\n\n# List all settings\nsudo firewall-cmd --list-all', 'language': 'bash'},
            {'title': 'Manage Services', 'description': 'Allow services through firewall.', 'code': '# List available services\nfirewall-cmd --get-services\n\n# Add service (runtime)\nsudo firewall-cmd --add-service=http\n\n# Add service (permanent)\nsudo firewall-cmd --permanent --add-service=http\nsudo firewall-cmd --permanent --add-service=https\n\n# Remove service\nsudo firewall-cmd --permanent --remove-service=http\n\n# Reload to apply permanent changes\nsudo firewall-cmd --reload', 'language': 'bash'},
            {'title': 'Manage Ports', 'description': 'Open specific ports.', 'code': '# Add port\nsudo firewall-cmd --permanent --add-port=8080/tcp\n\n# Add port range\nsudo firewall-cmd --permanent --add-port=3000-3010/tcp\n\n# Remove port\nsudo firewall-cmd --permanent --remove-port=8080/tcp\n\n# List open ports\nsudo firewall-cmd --list-ports\n\n# Reload\nsudo firewall-cmd --reload', 'language': 'bash'},
            {'title': 'Zones and Rich Rules', 'description': 'Advanced firewall configuration.', 'code': '# List zones\nfirewall-cmd --get-zones\nfirewall-cmd --get-active-zones\n\n# Change default zone\nsudo firewall-cmd --set-default-zone=public\n\n# Add interface to zone\nsudo firewall-cmd --zone=public --change-interface=eth0\n\n# Rich rule - allow from specific IP\nsudo firewall-cmd --permanent --add-rich-rule=\'rule family="ipv4" source address="192.168.1.100" accept\'\n\n# Rich rule - allow port from IP\nsudo firewall-cmd --permanent --add-rich-rule=\'rule family="ipv4" source address="192.168.1.0/24" port protocol="tcp" port="3306" accept\'\n\nsudo firewall-cmd --reload', 'language': 'bash'}
        ],
        'postInstallation': {'title': 'Troubleshooting', 'content': 'Check logs: journalctl -u firewalld. List rich rules: firewall-cmd --list-rich-rules. Always use --permanent for persistent rules. Test before applying to production.'}
    },
    {
        'title': 'CentOS SELinux Configuration',
        'description': 'Understand and configure SELinux on CentOS and RHEL systems.',
        'category': 'security',
        'subcategory': 'centos',
        'os': ['centos', 'rhel', 'linux'],
        'difficulty': 'advanced',
        'tags': ['centos', 'selinux', 'security', 'linux', 'rhel'],
        'steps': [
            {'title': 'Check SELinux Status', 'description': 'View current SELinux state.', 'code': '# Check status\ngetenforce\nsestatus\n\n# Modes:\n# Enforcing - SELinux policy enforced\n# Permissive - Policy not enforced, only logged\n# Disabled - SELinux off', 'language': 'bash'},
            {'title': 'Change SELinux Mode', 'description': 'Switch between modes.', 'code': '# Temporary change (until reboot)\nsudo setenforce 0  # Permissive\nsudo setenforce 1  # Enforcing\n\n# Permanent change\nsudo nano /etc/selinux/config\n\n# Set:\nSELINUX=enforcing   # or permissive or disabled\n\n# Reboot required for disabled mode\nsudo reboot', 'language': 'bash'},
            {'title': 'SELinux Booleans', 'description': 'Toggle SELinux features.', 'code': '# List all booleans\ngetsebool -a\n\n# Search boolean\ngetsebool -a | grep httpd\n\n# Enable boolean (temporary)\nsudo setsebool httpd_can_network_connect on\n\n# Enable boolean (permanent)\nsudo setsebool -P httpd_can_network_connect on\n\n# Common web server booleans:\nsudo setsebool -P httpd_can_network_connect 1\nsudo setsebool -P httpd_can_sendmail 1\nsudo setsebool -P httpd_enable_homedirs 1', 'language': 'bash'},
            {'title': 'SELinux Context and Troubleshooting', 'description': 'Fix SELinux permission issues.', 'code': '# View file context\nls -Z /var/www/html/\n\n# Change file context\nsudo chcon -t httpd_sys_content_t /var/www/mysite/\n\n# Restore default context\nsudo restorecon -Rv /var/www/html/\n\n# Check audit log for denials\nsudo ausearch -m avc -ts recent\n\n# Generate policy fix suggestions\nsudo ausearch -m avc -ts recent | audit2why\n\n# Generate and apply policy\nsudo ausearch -m avc | audit2allow -M mypolicy\nsudo semodule -i mypolicy.pp', 'language': 'bash'}
        ],
        'postInstallation': {'title': 'Best Practice', 'content': 'Keep SELinux in Enforcing mode for security. Use audit2why to understand denials. Use setsebool for common issues. restorecon fixes most file context issues.'}
    },
    {
        'title': 'CentOS Network Configuration with nmcli',
        'description': 'Configure network settings using NetworkManager CLI on CentOS.',
        'category': 'networking',
        'subcategory': 'centos',
        'os': ['centos', 'rhel', 'linux'],
        'difficulty': 'intermediate',
        'tags': ['centos', 'nmcli', 'networking', 'networkmanager', 'linux'],
        'steps': [
            {'title': 'View Network Status', 'description': 'Check current configuration.', 'code': '# List connections\nnmcli connection show\n\n# Show active connections\nnmcli connection show --active\n\n# List devices\nnmcli device status\n\n# Show device details\nnmcli device show eth0\n\n# General status\nnmcli general status', 'language': 'bash'},
            {'title': 'Configure DHCP', 'description': 'Set up automatic IP.', 'code': '# Create DHCP connection\nsudo nmcli connection add \\\n    type ethernet \\\n    con-name "dhcp-conn" \\\n    ifname eth0 \\\n    ipv4.method auto\n\n# Activate connection\nsudo nmcli connection up dhcp-conn', 'language': 'bash'},
            {'title': 'Configure Static IP', 'description': 'Set manual IP address.', 'code': '# Create static connection\nsudo nmcli connection add \\\n    type ethernet \\\n    con-name "static-conn" \\\n    ifname eth0 \\\n    ipv4.addresses 192.168.1.100/24 \\\n    ipv4.gateway 192.168.1.1 \\\n    ipv4.dns "8.8.8.8,8.8.4.4" \\\n    ipv4.method manual\n\n# Or modify existing connection\nsudo nmcli connection modify "Wired connection 1" \\\n    ipv4.addresses 192.168.1.100/24 \\\n    ipv4.gateway 192.168.1.1 \\\n    ipv4.dns "8.8.8.8" \\\n    ipv4.method manual\n\n# Activate\nsudo nmcli connection up static-conn', 'language': 'bash'},
            {'title': 'Common Operations', 'description': 'Manage network connections.', 'code': '# Bring connection up/down\nsudo nmcli connection up "connection-name"\nsudo nmcli connection down "connection-name"\n\n# Delete connection\nsudo nmcli connection delete "connection-name"\n\n# Reload connections\nsudo nmcli connection reload\n\n# Set hostname\nsudo nmcli general hostname myserver.example.com\n\n# Set DNS\nsudo nmcli connection modify "connection-name" ipv4.dns "8.8.8.8 8.8.4.4"\n\n# Restart NetworkManager\nsudo systemctl restart NetworkManager', 'language': 'bash'}
        ],
        'postInstallation': {'title': 'Alternative', 'content': 'Use nmtui for text-based UI. Config files in /etc/NetworkManager/system-connections/. For servers without NetworkManager, use /etc/sysconfig/network-scripts/'}
    },
    {
        'title': 'Install LAMP Stack on CentOS',
        'description': 'Install Linux, Apache, MariaDB, PHP stack on CentOS server.',
        'category': 'installation',
        'subcategory': 'centos',
        'os': ['centos', 'rhel', 'linux'],
        'difficulty': 'intermediate',
        'tags': ['centos', 'lamp', 'apache', 'mariadb', 'php'],
        'steps': [
            {'title': 'Install Apache', 'description': 'Install Apache web server.', 'code': '# Install Apache\nsudo dnf install httpd -y\n\n# Start and enable\nsudo systemctl start httpd\nsudo systemctl enable httpd\n\n# Open firewall\nsudo firewall-cmd --permanent --add-service=http\nsudo firewall-cmd --permanent --add-service=https\nsudo firewall-cmd --reload\n\n# Verify\ncurl http://localhost', 'language': 'bash'},
            {'title': 'Install MariaDB', 'description': 'Install MariaDB database server.', 'code': '# Install MariaDB\nsudo dnf install mariadb-server -y\n\n# Start and enable\nsudo systemctl start mariadb\nsudo systemctl enable mariadb\n\n# Secure installation\nsudo mysql_secure_installation\n\n# Login\nmysql -u root -p', 'language': 'bash'},
            {'title': 'Install PHP', 'description': 'Install PHP and modules.', 'code': '# Enable Remi repository for latest PHP\nsudo dnf install https://rpms.remirepo.net/enterprise/remi-release-9.rpm -y\nsudo dnf module reset php\nsudo dnf module enable php:remi-8.2 -y\n\n# Install PHP and modules\nsudo dnf install php php-cli php-mysqlnd php-gd php-mbstring php-xml php-curl php-zip -y\n\n# Restart Apache\nsudo systemctl restart httpd\n\n# Verify\nphp -v', 'language': 'bash'},
            {'title': 'Test LAMP', 'description': 'Verify installation.', 'code': '# Create PHP info file\necho "<?php phpinfo(); ?>" | sudo tee /var/www/html/info.php\n\n# Set ownership\nsudo chown apache:apache /var/www/html/info.php\n\n# SELinux context\nsudo restorecon -v /var/www/html/info.php\n\n# Test in browser\nhttp://your-server-ip/info.php\n\n# Remove test file (security)\nsudo rm /var/www/html/info.php', 'language': 'bash'}
        ],
        'postInstallation': {'title': 'Configuration', 'content': 'PHP config: /etc/php.ini. Apache config: /etc/httpd/conf/httpd.conf. Virtual hosts: /etc/httpd/conf.d/. Document root: /var/www/html/'}
    }
]

async def seed_centos():
    print("=" * 60)
    print("  SEEDING: CentOS/RHEL Articles")
    print("=" * 60)
    
    added = 0
    for article in CENTOS_ARTICLES:
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
    
    print(f"\n✓ Added {added} CentOS articles")

if __name__ == "__main__":
    asyncio.run(seed_centos())
