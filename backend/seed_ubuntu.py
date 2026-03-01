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

UBUNTU_ARTICLES = [
    {
        'title': 'Ubuntu 22.04 LTS Server Installation Guide',
        'description': 'Complete step-by-step guide to install Ubuntu 22.04 LTS Server from USB.',
        'category': 'installation',
        'subcategory': 'ubuntu',
        'os': ['ubuntu', 'linux'],
        'difficulty': 'beginner',
        'tags': ['ubuntu', 'installation', 'server', 'linux', '22.04'],
        'steps': [
            {'title': 'Download Ubuntu Server ISO', 'description': 'Get the official ISO file.', 'code': 'Download from:\nhttps://ubuntu.com/download/server\n\nChoose: Ubuntu Server 22.04 LTS\nFile size: ~1.5GB\n\nVerify checksum:\nsha256sum ubuntu-22.04-live-server-amd64.iso', 'language': 'bash'},
            {'title': 'Create Bootable USB', 'description': 'Create installation media.', 'code': '# On Linux:\nsudo dd if=ubuntu-22.04-live-server-amd64.iso of=/dev/sdX bs=4M status=progress\n\n# On Windows:\n# Use Rufus or Balena Etcher\n\n# On Mac:\nsudo dd if=ubuntu-22.04-live-server-amd64.iso of=/dev/diskX bs=4m', 'language': 'bash'},
            {'title': 'Boot and Install', 'description': 'Follow installation wizard.', 'code': 'Installation Steps:\n1. Boot from USB\n2. Select language: English\n3. Keyboard configuration\n4. Network configuration (DHCP or static)\n5. Proxy (skip if none)\n6. Mirror address (default)\n7. Storage configuration:\n   - Use entire disk (simple)\n   - Custom layout (advanced)\n8. Create user account\n9. Install OpenSSH server: Yes\n10. Featured snaps: Skip or select\n11. Wait for installation\n12. Reboot', 'language': 'bash'},
            {'title': 'Post-Installation', 'description': 'First steps after install.', 'code': '# Update system\nsudo apt update && sudo apt upgrade -y\n\n# Set timezone\nsudo timedatectl set-timezone Asia/Kolkata\n\n# Install essential packages\nsudo apt install -y curl wget git htop net-tools\n\n# Enable firewall\nsudo ufw allow ssh\nsudo ufw enable', 'language': 'bash'}
        ],
        'postInstallation': {'title': 'Next Steps', 'content': 'Configure static IP if needed. Setup SSH keys for passwordless login. Install required services like Nginx, MySQL. Configure automatic security updates.'}
    },
    {
        'title': 'Ubuntu Desktop 22.04 Installation and Setup',
        'description': 'Install Ubuntu Desktop 22.04 with GNOME and post-installation tweaks.',
        'category': 'installation',
        'subcategory': 'ubuntu',
        'os': ['ubuntu', 'linux'],
        'difficulty': 'beginner',
        'tags': ['ubuntu', 'desktop', 'gnome', 'installation', 'linux'],
        'steps': [
            {'title': 'Create Installation Media', 'description': 'Download and create bootable USB.', 'code': 'Download:\nhttps://ubuntu.com/download/desktop\n\nCreate USB:\n# Using Startup Disk Creator (Ubuntu)\n# Using Rufus (Windows)\n# Using Balena Etcher (All platforms)', 'language': 'bash'},
            {'title': 'Install Ubuntu Desktop', 'description': 'Follow graphical installer.', 'code': 'Installation Steps:\n1. Boot from USB\n2. Try Ubuntu or Install Ubuntu\n3. Choose language\n4. Keyboard layout\n5. Updates and other software:\n   - Normal installation (recommended)\n   - Download updates while installing\n   - Install third-party software\n6. Installation type:\n   - Erase disk (clean install)\n   - Something else (dual boot)\n7. Select timezone\n8. Create user account\n9. Wait for installation\n10. Restart', 'language': 'bash'},
            {'title': 'Post-Install Updates', 'description': 'Update and install essentials.', 'code': '# Update system\nsudo apt update && sudo apt upgrade -y\n\n# Install restricted extras (codecs, fonts)\nsudo apt install ubuntu-restricted-extras\n\n# Install GNOME tweaks\nsudo apt install gnome-tweaks gnome-shell-extensions\n\n# Install common apps\nsudo apt install vlc gimp libreoffice', 'language': 'bash'},
            {'title': 'Install Additional Drivers', 'description': 'Install proprietary drivers.', 'code': '# Open Software & Updates\n# Go to "Additional Drivers" tab\n# Select and apply proprietary drivers\n\n# Or via command line:\nsudo ubuntu-drivers autoinstall\n\n# For NVIDIA:\nsudo apt install nvidia-driver-535\n\n# Reboot after driver installation\nsudo reboot', 'language': 'bash'}
        ],
        'postInstallation': {'title': 'Customization', 'content': 'Use GNOME Tweaks to customize appearance. Install extensions from extensions.gnome.org. Enable Minimize on click in Settings. Consider Timeshift for system backups.'}
    },
    {
        'title': 'Ubuntu Package Management with APT',
        'description': 'Master APT package manager commands for Ubuntu and Debian systems.',
        'category': 'configuration',
        'subcategory': 'ubuntu',
        'os': ['ubuntu', 'linux'],
        'difficulty': 'beginner',
        'tags': ['ubuntu', 'apt', 'package-manager', 'linux', 'commands'],
        'steps': [
            {'title': 'Update Package Lists', 'description': 'Refresh package information.', 'code': '# Update package lists\nsudo apt update\n\n# Upgrade installed packages\nsudo apt upgrade -y\n\n# Full upgrade (may remove packages)\nsudo apt full-upgrade -y\n\n# Update and upgrade combined\nsudo apt update && sudo apt upgrade -y', 'language': 'bash'},
            {'title': 'Install and Remove Packages', 'description': 'Manage software packages.', 'code': '# Install package\nsudo apt install nginx\n\n# Install multiple packages\nsudo apt install nginx mysql-server php\n\n# Install specific version\nsudo apt install nginx=1.18.0-0ubuntu1\n\n# Remove package\nsudo apt remove nginx\n\n# Remove with config files\nsudo apt purge nginx\n\n# Remove unused dependencies\nsudo apt autoremove', 'language': 'bash'},
            {'title': 'Search and Info', 'description': 'Find and get package information.', 'code': '# Search packages\napt search nginx\n\n# Show package info\napt show nginx\n\n# List installed packages\napt list --installed\n\n# List upgradable packages\napt list --upgradable\n\n# Check if package installed\ndpkg -l | grep nginx', 'language': 'bash'},
            {'title': 'Repository Management', 'description': 'Add and manage repositories.', 'code': '# Add PPA repository\nsudo add-apt-repository ppa:ondrej/php\nsudo apt update\n\n# Remove PPA\nsudo add-apt-repository --remove ppa:ondrej/php\n\n# Add custom repository\necho "deb http://repo.example.com/ubuntu focal main" | sudo tee /etc/apt/sources.list.d/example.list\n\n# Import GPG key\nwget -qO - https://repo.example.com/key.gpg | sudo apt-key add -\n\n# List repositories\ngrep -r "^deb " /etc/apt/', 'language': 'bash'}
        ],
        'postInstallation': {'title': 'Cleanup', 'content': 'Regular cleanup: sudo apt autoremove && sudo apt autoclean. Clear cache: sudo apt clean. Fix broken packages: sudo apt --fix-broken install'}
    },
    {
        'title': 'Ubuntu Network Configuration with Netplan',
        'description': 'Configure network settings using Netplan on Ubuntu 18.04 and later.',
        'category': 'networking',
        'subcategory': 'ubuntu',
        'os': ['ubuntu', 'linux'],
        'difficulty': 'intermediate',
        'tags': ['ubuntu', 'netplan', 'networking', 'static-ip', 'linux'],
        'steps': [
            {'title': 'View Current Configuration', 'description': 'Check existing network setup.', 'code': '# List network interfaces\nip addr\nip link\n\n# View current netplan config\ncat /etc/netplan/*.yaml\n\n# Check routes\nip route\n\n# Check DNS\nresolvectl status', 'language': 'bash'},
            {'title': 'Configure DHCP', 'description': 'Setup automatic IP configuration.', 'code': 'sudo nano /etc/netplan/01-netcfg.yaml\n\nnetwork:\n  version: 2\n  renderer: networkd\n  ethernets:\n    eth0:\n      dhcp4: true\n      dhcp6: false', 'language': 'yaml'},
            {'title': 'Configure Static IP', 'description': 'Set manual IP address.', 'code': 'sudo nano /etc/netplan/01-netcfg.yaml\n\nnetwork:\n  version: 2\n  renderer: networkd\n  ethernets:\n    eth0:\n      addresses:\n        - 192.168.1.100/24\n      routes:\n        - to: default\n          via: 192.168.1.1\n      nameservers:\n        addresses:\n          - 8.8.8.8\n          - 8.8.4.4', 'language': 'yaml'},
            {'title': 'Apply Configuration', 'description': 'Apply and test network changes.', 'code': '# Test configuration (dry run)\nsudo netplan try\n\n# Apply configuration\nsudo netplan apply\n\n# Generate backend config\nsudo netplan generate\n\n# Debug\nsudo netplan --debug apply\n\n# Verify\nip addr show eth0\nping -c 4 google.com', 'language': 'bash'}
        ],
        'postInstallation': {'title': 'Troubleshooting', 'content': 'Check YAML indentation (spaces only, no tabs). Use netplan try for safe testing. Logs: journalctl -u systemd-networkd. Restart networking: sudo systemctl restart systemd-networkd'}
    },
    {
        'title': 'Ubuntu User and Group Management',
        'description': 'Create and manage users and groups on Ubuntu Linux.',
        'category': 'security',
        'subcategory': 'ubuntu',
        'os': ['ubuntu', 'linux'],
        'difficulty': 'beginner',
        'tags': ['ubuntu', 'users', 'groups', 'permissions', 'linux'],
        'steps': [
            {'title': 'Create Users', 'description': 'Add new users to system.', 'code': '# Create user with home directory\nsudo adduser newuser\n\n# Create user (non-interactive)\nsudo useradd -m -s /bin/bash newuser\nsudo passwd newuser\n\n# Create system user (no login)\nsudo useradd -r -s /bin/false serviceuser\n\n# List users\ncat /etc/passwd\ngetent passwd', 'language': 'bash'},
            {'title': 'Manage Groups', 'description': 'Create and manage groups.', 'code': '# Create group\nsudo groupadd developers\n\n# Add user to group\nsudo usermod -aG developers newuser\n\n# Add user to multiple groups\nsudo usermod -aG docker,sudo,www-data newuser\n\n# View user groups\ngroups newuser\nid newuser\n\n# List all groups\ncat /etc/group', 'language': 'bash'},
            {'title': 'Grant Sudo Access', 'description': 'Give administrative privileges.', 'code': '# Add user to sudo group\nsudo usermod -aG sudo newuser\n\n# Or edit sudoers file\nsudo visudo\n\n# Add line for full sudo:\nnewuser ALL=(ALL:ALL) ALL\n\n# Sudo without password:\nnewuser ALL=(ALL) NOPASSWD: ALL\n\n# Verify\nsudo -l -U newuser', 'language': 'bash'},
            {'title': 'Delete Users', 'description': 'Remove users from system.', 'code': '# Delete user (keep home)\nsudo userdel username\n\n# Delete user with home directory\nsudo userdel -r username\n\n# Delete group\nsudo groupdel groupname\n\n# Remove user from group\nsudo gpasswd -d username groupname\n\n# Lock user account\nsudo passwd -l username\n\n# Unlock user account\nsudo passwd -u username', 'language': 'bash'}
        ],
        'postInstallation': {'title': 'Best Practices', 'content': 'Use adduser instead of useradd for interactive creation. Always use sudo group for admin access. Create service accounts with nologin shell. Regularly audit user accounts.'}
    },
    {
        'title': 'Ubuntu Systemd Service Management',
        'description': 'Manage system services using systemctl on Ubuntu.',
        'category': 'configuration',
        'subcategory': 'ubuntu',
        'os': ['ubuntu', 'linux'],
        'difficulty': 'intermediate',
        'tags': ['ubuntu', 'systemd', 'systemctl', 'services', 'linux'],
        'steps': [
            {'title': 'Basic Service Commands', 'description': 'Start, stop, restart services.', 'code': '# Start service\nsudo systemctl start nginx\n\n# Stop service\nsudo systemctl stop nginx\n\n# Restart service\nsudo systemctl restart nginx\n\n# Reload configuration\nsudo systemctl reload nginx\n\n# Check status\nsudo systemctl status nginx', 'language': 'bash'},
            {'title': 'Enable/Disable Services', 'description': 'Control service autostart.', 'code': '# Enable at boot\nsudo systemctl enable nginx\n\n# Disable at boot\nsudo systemctl disable nginx\n\n# Enable and start\nsudo systemctl enable --now nginx\n\n# Check if enabled\nsystemctl is-enabled nginx\n\n# Check if active\nsystemctl is-active nginx', 'language': 'bash'},
            {'title': 'List and View Services', 'description': 'Get service information.', 'code': '# List all services\nsystemctl list-units --type=service\n\n# List running services\nsystemctl list-units --type=service --state=running\n\n# List failed services\nsystemctl --failed\n\n# Show service details\nsystemctl show nginx\n\n# View service logs\njournalctl -u nginx\njournalctl -u nginx --since "1 hour ago"\njournalctl -u nginx -f  # Follow logs', 'language': 'bash'},
            {'title': 'Create Custom Service', 'description': 'Create your own systemd service.', 'code': 'sudo nano /etc/systemd/system/myapp.service\n\n[Unit]\nDescription=My Application\nAfter=network.target\n\n[Service]\nType=simple\nUser=www-data\nWorkingDirectory=/var/www/myapp\nExecStart=/usr/bin/node /var/www/myapp/server.js\nRestart=on-failure\nRestartSec=10\n\n[Install]\nWantedBy=multi-user.target\n\n# Enable and start\nsudo systemctl daemon-reload\nsudo systemctl enable myapp\nsudo systemctl start myapp', 'language': 'bash'}
        ],
        'postInstallation': {'title': 'Troubleshooting', 'content': 'Always run daemon-reload after editing service files. Check logs with journalctl -xe for errors. Service files location: /etc/systemd/system/ (custom) or /lib/systemd/system/ (packages).'}
    }
]

async def seed_ubuntu():
    print("=" * 60)
    print("  SEEDING: Ubuntu Articles")
    print("=" * 60)
    
    added = 0
    for article in UBUNTU_ARTICLES:
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
    
    print(f"\n✓ Added {added} Ubuntu articles")

if __name__ == "__main__":
    asyncio.run(seed_ubuntu())
