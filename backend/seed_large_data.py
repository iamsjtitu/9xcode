from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
from pathlib import Path
import asyncio
from datetime import datetime
import uuid
import random

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

def create_slug(title):
    import re
    slug = title.lower()
    slug = re.sub(r'[^a-z0-9]+', '-', slug)
    return slug.strip('-')

# Generate comprehensive articles for each category
snippets_data = {
    "installation": [
        # Web Servers
        ("Install Apache Web Server", "Complete guide to install and configure Apache HTTP Server on Linux systems", ["apache", "web-server", "installation"], ["ubuntu", "centos", "debian"], "beginner", [
            {"title": "Install Apache (Ubuntu/Debian)", "description": "Install Apache using apt package manager", "code": "sudo apt update\nsudo apt install apache2 -y", "language": "bash"},
            {"title": "Install Apache (CentOS/RHEL)", "description": "Install Apache using yum/dnf", "code": "sudo yum install httpd -y\n# Or with dnf\nsudo dnf install httpd -y", "language": "bash"},
            {"title": "Start Apache Service", "description": "Start and enable Apache", "code": "sudo systemctl start apache2  # Ubuntu\nsudo systemctl start httpd    # CentOS\nsudo systemctl enable apache2", "language": "bash"}
        ]),
        
        ("Install NGINX Web Server", "High-performance web server installation and basic configuration", ["nginx", "web-server", "installation"], ["ubuntu", "centos", "debian"], "beginner", [
            {"title": "Install NGINX (Ubuntu)", "description": "Install NGINX from official repository", "code": "sudo apt update\nsudo apt install nginx -y", "language": "bash"},
            {"title": "Start NGINX", "description": "Start and enable NGINX service", "code": "sudo systemctl start nginx\nsudo systemctl enable nginx\nsudo systemctl status nginx", "language": "bash"}
        ]),
        
        # Databases
        ("Install MySQL 8.0", "Install and secure MySQL database server", ["mysql", "database", "installation"], ["ubuntu", "centos"], "beginner", [
            {"title": "Install MySQL", "description": "Install MySQL server package", "code": "sudo apt update\nsudo apt install mysql-server -y", "language": "bash"},
            {"title": "Secure Installation", "description": "Run MySQL secure installation script", "code": "sudo mysql_secure_installation", "language": "bash"}
        ]),
        
        ("Install PostgreSQL 16", "Install PostgreSQL database server with extensions", ["postgresql", "database", "installation"], ["ubuntu", "debian"], "intermediate", [
            {"title": "Add PostgreSQL Repository", "description": "Add official PostgreSQL apt repository", "code": "sudo apt install curl ca-certificates\nsudo install -d /usr/share/postgresql-common/pgdg\nsudo curl -o /usr/share/postgresql-common/pgdg/apt.postgresql.org.asc --fail https://www.postgresql.org/media/keys/ACCC4CF8.asc\nsudo sh -c 'echo \"deb http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main\" > /etc/apt/sources.list.d/pgdg.list'", "language": "bash"},
            {"title": "Install PostgreSQL", "description": "Install PostgreSQL 16", "code": "sudo apt update\nsudo apt install postgresql-16 postgresql-contrib-16 -y", "language": "bash"}
        ]),
        
        ("Install MongoDB 7.0", "Install MongoDB NoSQL database", ["mongodb", "database", "nosql"], ["ubuntu", "debian"], "intermediate", [
            {"title": "Import MongoDB GPG Key", "description": "Add MongoDB repository key", "code": "curl -fsSL https://www.mongodb.org/static/pgp/server-7.0.asc | sudo gpg --dearmor -o /etc/apt/keyrings/mongodb-server-7.0.gpg", "language": "bash"},
            {"title": "Add MongoDB Repository", "description": "Add MongoDB 7.0 repository", "code": "echo \"deb [ arch=amd64,arm64 signed-by=/etc/apt/keyrings/mongodb-server-7.0.gpg ] https://repo.mongodb.org/apt/ubuntu $(lsb_release -cs)/mongodb-org/7.0 multiverse\" | sudo tee /etc/apt/sources.list.d/mongodb-org-7.0.list", "language": "bash"},
            {"title": "Install MongoDB", "description": "Install MongoDB packages", "code": "sudo apt update\nsudo apt install mongodb-org -y\nsudo systemctl start mongod\nsudo systemctl enable mongod", "language": "bash"}
        ]),
        
        ("Install Redis Cache Server", "Install Redis in-memory database", ["redis", "cache", "database"], ["ubuntu", "centos"], "beginner", [
            {"title": "Install Redis", "description": "Install Redis server", "code": "sudo apt update\nsudo apt install redis-server -y", "language": "bash"},
            {"title": "Configure Redis", "description": "Edit Redis configuration", "code": "sudo nano /etc/redis/redis.conf\n# Change: supervised systemd\nsudo systemctl restart redis-server", "language": "bash"}
        ]),
        
        # Programming Languages
        ("Install Python 3.11", "Install latest Python version", ["python", "programming", "development"], ["ubuntu", "debian"], "beginner", [
            {"title": "Add Deadsnakes PPA", "description": "Add PPA for Python versions", "code": "sudo add-apt-repository ppa:deadsnakes/ppa -y\nsudo apt update", "language": "bash"},
            {"title": "Install Python 3.11", "description": "Install Python and tools", "code": "sudo apt install python3.11 python3.11-venv python3.11-dev -y", "language": "bash"}
        ]),
        
        ("Install Node.js 20 LTS", "Install Node.js runtime and npm", ["nodejs", "javascript", "development"], ["ubuntu", "centos"], "beginner", [
            {"title": "Install NodeSource Repository", "description": "Add Node.js 20.x repository", "code": "curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -", "language": "bash"},
            {"title": "Install Node.js", "description": "Install Node.js and npm", "code": "sudo apt install nodejs -y\nnode --version\nnpm --version", "language": "bash"}
        ]),
        
        ("Install PHP 8.3", "Install PHP with common extensions", ["php", "web-development", "programming"], ["ubuntu", "debian"], "beginner", [
            {"title": "Add PHP Repository", "description": "Add Ondrej PPA for latest PHP", "code": "sudo add-apt-repository ppa:ondrej/php -y\nsudo apt update", "language": "bash"},
            {"title": "Install PHP 8.3", "description": "Install PHP and extensions", "code": "sudo apt install php8.3 php8.3-cli php8.3-fpm php8.3-mysql php8.3-curl php8.3-xml -y", "language": "bash"}
        ]),
        
        ("Install Docker and Docker Compose", "Install container platform", ["docker", "containers", "devops"], ["ubuntu", "centos", "debian"], "intermediate", [
            {"title": "Install Docker (Ubuntu)", "description": "Install Docker from official repository", "code": "sudo apt update\nsudo apt install ca-certificates curl\nsudo install -m 0755 -d /etc/apt/keyrings\nsudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc\nsudo chmod a+r /etc/apt/keyrings/docker.asc\necho \"deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu $(. /etc/os-release && echo \"$VERSION_CODENAME\") stable\" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null\nsudo apt update\nsudo apt install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin -y", "language": "bash"},
            {"title": "Start Docker", "description": "Enable and start Docker service", "code": "sudo systemctl start docker\nsudo systemctl enable docker\nsudo usermod -aG docker $USER", "language": "bash"}
        ]),
        
        # Development Tools
        ("Install Git Version Control", "Install Git for version control", ["git", "version-control", "development"], ["ubuntu", "centos", "linux"], "beginner", [
            {"title": "Install Git", "description": "Install Git package", "code": "sudo apt update\nsudo apt install git -y", "language": "bash"},
            {"title": "Configure Git", "description": "Set up Git user information", "code": "git config --global user.name \"Your Name\"\ngit config --global user.email \"your.email@example.com\"\ngit config --list", "language": "bash"}
        ]),
        
        ("Install VS Code on Linux", "Install Visual Studio Code editor", ["vscode", "editor", "development"], ["ubuntu", "debian"], "beginner", [
            {"title": "Import Microsoft GPG Key", "description": "Add VS Code repository", "code": "wget -qO- https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > packages.microsoft.gpg\nsudo install -D -o root -g root -m 644 packages.microsoft.gpg /etc/apt/keyrings/packages.microsoft.gpg", "language": "bash"},
            {"title": "Install VS Code", "description": "Install Visual Studio Code", "code": "sudo sh -c 'echo \"deb [arch=amd64,arm64,armhf signed-by=/etc/apt/keyrings/packages.microsoft.gpg] https://packages.microsoft.com/repos/code stable main\" > /etc/apt/sources.list.d/vscode.list'\nsudo apt update\nsudo apt install code -y", "language": "bash"}
        ]),
        
        # Monitoring & Management
        ("Install Grafana Monitoring", "Install Grafana dashboard", ["grafana", "monitoring", "visualization"], ["ubuntu", "debian"], "intermediate", [
            {"title": "Add Grafana Repository", "description": "Add Grafana apt repository", "code": "sudo apt install -y software-properties-common\nsudo add-apt-repository \"deb https://packages.grafana.com/oss/deb stable main\"", "language": "bash"},
            {"title": "Install Grafana", "description": "Install Grafana package", "code": "wget -q -O - https://packages.grafana.com/gpg.key | sudo apt-key add -\nsudo apt update\nsudo apt install grafana -y\nsudo systemctl start grafana-server\nsudo systemctl enable grafana-server", "language": "bash"}
        ]),
        
        ("Install Prometheus Monitoring", "Install Prometheus time-series database", ["prometheus", "monitoring", "metrics"], ["ubuntu", "linux"], "intermediate", [
            {"title": "Download Prometheus", "description": "Download latest Prometheus release", "code": "cd /tmp\nwget https://github.com/prometheus/prometheus/releases/download/v2.45.0/prometheus-2.45.0.linux-amd64.tar.gz\ntar -xvf prometheus-2.45.0.linux-amd64.tar.gz", "language": "bash"},
            {"title": "Install Prometheus", "description": "Move files and create service", "code": "sudo mv prometheus-2.45.0.linux-amd64 /opt/prometheus\nsudo useradd --no-create-home --shell /bin/false prometheus\nsudo chown -R prometheus:prometheus /opt/prometheus", "language": "bash"}
        ]),
    ],
    
    "security": [
        ("Configure UFW Firewall", "Set up UFW firewall rules", ["ufw", "firewall", "security"], ["ubuntu", "debian"], "beginner", [
            {"title": "Enable UFW", "description": "Activate UFW firewall", "code": "sudo ufw default deny incoming\nsudo ufw default allow outgoing\nsudo ufw allow ssh\nsudo ufw enable", "language": "bash"}
        ]),
        
        ("SSH Key Authentication Setup", "Configure SSH key-based login", ["ssh", "authentication", "security"], ["ubuntu", "centos", "linux"], "intermediate", [
            {"title": "Generate SSH Key", "description": "Create SSH key pair", "code": "ssh-keygen -t ed25519 -C \"your_email@example.com\"", "language": "bash"},
            {"title": "Copy Key to Server", "description": "Install public key on server", "code": "ssh-copy-id user@server_ip", "language": "bash"}
        ]),
        
        ("Install and Configure Fail2ban", "Protect against brute-force attacks", ["fail2ban", "security", "ssh"], ["ubuntu", "centos"], "intermediate", [
            {"title": "Install Fail2ban", "description": "Install fail2ban package", "code": "sudo apt update\nsudo apt install fail2ban -y", "language": "bash"},
            {"title": "Configure Fail2ban", "description": "Set up fail2ban for SSH", "code": "sudo cp /etc/fail2ban/jail.conf /etc/fail2ban/jail.local\nsudo nano /etc/fail2ban/jail.local\nsudo systemctl restart fail2ban", "language": "bash"}
        ]),
        
        ("SSL Certificate with Let's Encrypt", "Install free SSL certificates", ["ssl", "letsencrypt", "https"], ["ubuntu", "debian"], "intermediate", [
            {"title": "Install Certbot", "description": "Install Let's Encrypt client", "code": "sudo apt update\nsudo apt install certbot python3-certbot-nginx -y", "language": "bash"},
            {"title": "Obtain Certificate", "description": "Get SSL certificate for domain", "code": "sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com", "language": "bash"}
        ]),
        
        ("Configure SELinux", "Security-Enhanced Linux setup", ["selinux", "security", "rhel"], ["centos", "rhel", "fedora"], "advanced", [
            {"title": "Check SELinux Status", "description": "View current SELinux mode", "code": "getenforce\nsestatus", "language": "bash"},
            {"title": "Set SELinux Mode", "description": "Configure SELinux enforcement", "code": "sudo setenforce 1  # Enforcing\nsudo nano /etc/selinux/config", "language": "bash"}
        ]),
        
        ("Configure AppArmor", "Application security profiles", ["apparmor", "security", "ubuntu"], ["ubuntu", "debian"], "advanced", [
            {"title": "Check AppArmor Status", "description": "View AppArmor profiles", "code": "sudo apparmor_status", "language": "bash"},
            {"title": "Manage Profiles", "description": "Enable/disable AppArmor profiles", "code": "sudo aa-enforce /etc/apparmor.d/usr.sbin.nginx\nsudo aa-complain /etc/apparmor.d/usr.sbin.apache2", "language": "bash"}
        ]),
        
        ("Set Up Two-Factor Authentication", "Add 2FA to SSH login", ["2fa", "authentication", "security"], ["ubuntu", "centos"], "advanced", [
            {"title": "Install Google Authenticator", "description": "Install PAM module", "code": "sudo apt install libpam-google-authenticator -y", "language": "bash"},
            {"title": "Configure 2FA", "description": "Set up authenticator for user", "code": "google-authenticator\n# Answer questions and save emergency codes", "language": "bash"}
        ]),
        
        ("Configure iptables Firewall", "Advanced firewall rules", ["iptables", "firewall", "security"], ["linux", "ubuntu", "centos"], "advanced", [
            {"title": "List Current Rules", "description": "View iptables rules", "code": "sudo iptables -L -v -n", "language": "bash"},
            {"title": "Add Rules", "description": "Configure firewall rules", "code": "sudo iptables -A INPUT -p tcp --dport 22 -j ACCEPT\nsudo iptables -A INPUT -p tcp --dport 80 -j ACCEPT\nsudo iptables -A INPUT -p tcp --dport 443 -j ACCEPT\nsudo iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT\nsudo iptables -P INPUT DROP", "language": "bash"}
        ]),
        
        ("Audit System with Lynis", "Security auditing tool", ["lynis", "audit", "security"], ["ubuntu", "centos", "linux"], "intermediate", [
            {"title": "Install Lynis", "description": "Install security auditing tool", "code": "sudo apt update\nsudo apt install lynis -y", "language": "bash"},
            {"title": "Run Security Audit", "description": "Perform system audit", "code": "sudo lynis audit system", "language": "bash"}
        ]),
        
        ("Configure Security Updates", "Automatic security patches", ["updates", "security", "automation"], ["ubuntu", "debian"], "beginner", [
            {"title": "Install Unattended Upgrades", "description": "Enable automatic updates", "code": "sudo apt install unattended-upgrades -y\nsudo dpkg-reconfigure --priority=low unattended-upgrades", "language": "bash"}
        ]),
    ],
    
    "configuration": [
        ("Configure Static IP Address", "Set permanent IP configuration", ["networking", "ip", "configuration"], ["ubuntu", "centos"], "beginner", [
            {"title": "Edit Netplan (Ubuntu)", "description": "Configure static IP with Netplan", "code": "sudo nano /etc/netplan/01-netcfg.yaml\n# Add:\n# network:\n#   version: 2\n#   ethernets:\n#     eth0:\n#       addresses: [192.168.1.100/24]\n#       gateway4: 192.168.1.1\n#       nameservers:\n#         addresses: [8.8.8.8, 8.8.4.4]\nsudo netplan apply", "language": "bash"}
        ]),
        
        ("Configure Hostname", "Change system hostname", ["hostname", "configuration", "system"], ["ubuntu", "centos", "linux"], "beginner", [
            {"title": "Set Hostname", "description": "Change hostname permanently", "code": "sudo hostnamectl set-hostname new-hostname\nsudo nano /etc/hosts\n# Add: 127.0.0.1 new-hostname\nhostname", "language": "bash"}
        ]),
        
        ("Configure Sudo Access", "Manage sudo permissions", ["sudo", "permissions", "security"], ["ubuntu", "centos", "linux"], "beginner", [
            {"title": "Add User to Sudo", "description": "Grant sudo access to user", "code": "sudo usermod -aG sudo username  # Ubuntu\nsudo usermod -aG wheel username # CentOS", "language": "bash"},
            {"title": "Configure Sudoers", "description": "Edit sudoers file", "code": "sudo visudo\n# Add: username ALL=(ALL:ALL) NOPASSWD:ALL", "language": "bash"}
        ]),
        
        ("Configure Time Zone", "Set system timezone", ["timezone", "time", "configuration"], ["ubuntu", "centos", "linux"], "beginner", [
            {"title": "Set Timezone", "description": "Configure system timezone", "code": "timedatectl list-timezones\nsudo timedatectl set-timezone America/New_York\ntimedatectl", "language": "bash"}
        ]),
        
        ("Configure NTP Time Sync", "Network time synchronization", ["ntp", "time", "sync"], ["ubuntu", "centos"], "beginner", [
            {"title": "Install NTP", "description": "Install NTP daemon", "code": "sudo apt install ntp -y\nsudo systemctl start ntp\nsudo systemctl enable ntp", "language": "bash"},
            {"title": "Configure NTP", "description": "Set NTP servers", "code": "sudo nano /etc/ntp.conf\n# Add: server pool.ntp.org\nsudo systemctl restart ntp", "language": "bash"}
        ]),
        
        ("Configure Swap Space", "Add swap memory", ["swap", "memory", "performance"], ["ubuntu", "centos", "linux"], "intermediate", [
            {"title": "Create Swap File", "description": "Create and enable swap", "code": "sudo fallocate -l 2G /swapfile\nsudo chmod 600 /swapfile\nsudo mkswap /swapfile\nsudo swapon /swapfile\necho '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab", "language": "bash"}
        ]),
        
        ("Configure System Limits", "Set resource limits", ["limits", "resources", "performance"], ["ubuntu", "centos", "linux"], "intermediate", [
            {"title": "Edit Limits", "description": "Configure system limits", "code": "sudo nano /etc/security/limits.conf\n# Add:\n# * soft nofile 65535\n# * hard nofile 65535\n# * soft nproc 32000\n# * hard nproc 32000", "language": "bash"}
        ]),
        
        ("Configure Log Rotation", "Manage log files", ["logging", "logrotate", "maintenance"], ["ubuntu", "centos", "linux"], "intermediate", [
            {"title": "Configure Logrotate", "description": "Set up log rotation", "code": "sudo nano /etc/logrotate.d/myapp\n# Add:\n# /var/log/myapp/*.log {\n#   daily\n#   rotate 7\n#   compress\n#   delaycompress\n#   missingok\n#   notifempty\n# }", "language": "bash"}
        ]),
        
        ("Configure Cron Jobs", "Schedule automated tasks", ["cron", "scheduling", "automation"], ["ubuntu", "centos", "linux"], "beginner", [
            {"title": "Edit Crontab", "description": "Add scheduled tasks", "code": "crontab -e\n# Add:\n# 0 2 * * * /path/to/backup.sh\n# */5 * * * * /path/to/monitor.sh", "language": "bash"},
            {"title": "View Cron Jobs", "description": "List scheduled tasks", "code": "crontab -l", "language": "bash"}
        ]),
        
        ("Configure Bash Aliases", "Create command shortcuts", ["bash", "aliases", "productivity"], ["ubuntu", "centos", "linux"], "beginner", [
            {"title": "Add Aliases", "description": "Create bash aliases", "code": "nano ~/.bashrc\n# Add:\n# alias ll='ls -alh'\n# alias update='sudo apt update && sudo apt upgrade'\n# alias ports='netstat -tuln'\nsource ~/.bashrc", "language": "bash"}
        ]),
    ],
    
    "networking": [
        ("Check Network Connectivity", "Test network connections", ["networking", "troubleshooting", "diagnostics"], ["ubuntu", "centos", "linux"], "beginner", [
            {"title": "Basic Connectivity Tests", "description": "Test network connectivity", "code": "ping -c 4 google.com\nping -c 4 8.8.8.8\ntraceroute google.com", "language": "bash"}
        ]),
        
        ("View Network Interfaces", "List network interfaces", ["networking", "interfaces", "diagnostics"], ["ubuntu", "centos", "linux"], "beginner", [
            {"title": "List Interfaces", "description": "View network interfaces", "code": "ip addr show\nip link show\nifconfig -a", "language": "bash"}
        ]),
        
        ("Check Open Ports", "List listening ports", ["networking", "ports", "security"], ["ubuntu", "centos", "linux"], "beginner", [
            {"title": "List Open Ports", "description": "View listening ports", "code": "sudo ss -tuln\nsudo netstat -tuln\nsudo lsof -i -P -n", "language": "bash"}
        ]),
        
        ("Configure DNS Servers", "Set custom DNS", ["dns", "networking", "configuration"], ["ubuntu", "centos"], "beginner", [
            {"title": "Configure DNS (Ubuntu)", "description": "Set DNS servers", "code": "sudo nano /etc/netplan/01-netcfg.yaml\n# Add under nameservers:\n#   addresses: [8.8.8.8, 1.1.1.1]\nsudo netplan apply", "language": "bash"}
        ]),
        
        ("Install OpenVPN Server", "Set up VPN server", ["vpn", "openvpn", "security"], ["ubuntu", "debian"], "advanced", [
            {"title": "Install OpenVPN", "description": "Install OpenVPN package", "code": "sudo apt update\nsudo apt install openvpn easy-rsa -y", "language": "bash"},
            {"title": "Set Up PKI", "description": "Initialize certificate authority", "code": "make-cadir ~/openvpn-ca\ncd ~/openvpn-ca\nsource vars\n./clean-all\n./build-ca", "language": "bash"}
        ]),
        
        ("Configure WireGuard VPN", "Modern VPN setup", ["wireguard", "vpn", "security"], ["ubuntu", "debian"], "intermediate", [
            {"title": "Install WireGuard", "description": "Install WireGuard package", "code": "sudo apt update\nsudo apt install wireguard -y", "language": "bash"},
            {"title": "Generate Keys", "description": "Create WireGuard keys", "code": "wg genkey | sudo tee /etc/wireguard/private.key\nsudo chmod 600 /etc/wireguard/private.key\nsudo cat /etc/wireguard/private.key | wg pubkey | sudo tee /etc/wireguard/public.key", "language": "bash"}
        ]),
        
        ("Set Up Network Bridge", "Bridge network interfaces", ["networking", "bridge", "virtualization"], ["ubuntu", "centos", "linux"], "advanced", [
            {"title": "Install Bridge Utils", "description": "Install bridge utilities", "code": "sudo apt install bridge-utils -y", "language": "bash"},
            {"title": "Create Bridge", "description": "Set up network bridge", "code": "sudo ip link add br0 type bridge\nsudo ip link set br0 up\nsudo ip link set eth0 master br0", "language": "bash"}
        ]),
        
        ("Configure Port Forwarding", "Forward ports with iptables", ["networking", "iptables", "forwarding"], ["ubuntu", "centos", "linux"], "intermediate", [
            {"title": "Enable IP Forwarding", "description": "Enable packet forwarding", "code": "sudo sysctl -w net.ipv4.ip_forward=1\necho 'net.ipv4.ip_forward=1' | sudo tee -a /etc/sysctl.conf", "language": "bash"},
            {"title": "Add Port Forward Rule", "description": "Forward port with iptables", "code": "sudo iptables -t nat -A PREROUTING -p tcp --dport 80 -j REDIRECT --to-port 8080", "language": "bash"}
        ]),
        
        ("Configure Network Bonding", "Bond network interfaces", ["networking", "bonding", "redundancy"], ["ubuntu", "centos"], "advanced", [
            {"title": "Install Bonding Module", "description": "Load bonding kernel module", "code": "sudo modprobe bonding\necho 'bonding' | sudo tee -a /etc/modules", "language": "bash"}
        ]),
        
        ("Monitor Network Traffic", "Track bandwidth usage", ["networking", "monitoring", "bandwidth"], ["ubuntu", "centos", "linux"], "intermediate", [
            {"title": "Install iftop", "description": "Install network monitoring tools", "code": "sudo apt install iftop nethogs vnstat -y", "language": "bash"},
            {"title": "Monitor Traffic", "description": "View network traffic", "code": "sudo iftop -i eth0\nsudo nethogs eth0\nvnstat -l -i eth0", "language": "bash"}
        ]),
    ],
    
    "database": [
        ("MySQL Database Backup", "Backup MySQL databases", ["mysql", "backup", "database"], ["ubuntu", "centos", "linux"], "intermediate", [
            {"title": "Backup Single Database", "description": "Create MySQL backup", "code": "mysqldump -u root -p database_name > backup.sql", "language": "bash"},
            {"title": "Backup All Databases", "description": "Backup all MySQL databases", "code": "mysqldump -u root -p --all-databases > all_databases.sql", "language": "bash"}
        ]),
        
        ("PostgreSQL Database Backup", "Backup PostgreSQL databases", ["postgresql", "backup", "database"], ["ubuntu", "centos", "linux"], "intermediate", [
            {"title": "Backup Database", "description": "Create PostgreSQL backup", "code": "pg_dump -U postgres database_name > backup.sql", "language": "bash"},
            {"title": "Backup with Compression", "description": "Create compressed backup", "code": "pg_dump -U postgres -F c database_name > backup.dump", "language": "bash"}
        ]),
        
        ("MongoDB Backup and Restore", "Backup MongoDB databases", ["mongodb", "backup", "database"], ["ubuntu", "centos", "linux"], "intermediate", [
            {"title": "Backup MongoDB", "description": "Create MongoDB backup", "code": "mongodump --db database_name --out /backup/path", "language": "bash"},
            {"title": "Restore MongoDB", "description": "Restore from backup", "code": "mongorestore --db database_name /backup/path/database_name", "language": "bash"}
        ]),
        
        ("MySQL Performance Tuning", "Optimize MySQL server", ["mysql", "performance", "optimization"], ["ubuntu", "centos"], "advanced", [
            {"title": "Edit MySQL Config", "description": "Tune MySQL parameters", "code": "sudo nano /etc/mysql/my.cnf\n# Add:\n# [mysqld]\n# innodb_buffer_pool_size = 1G\n# max_connections = 200\n# query_cache_size = 64M\nsudo systemctl restart mysql", "language": "bash"}
        ]),
        
        ("PostgreSQL Performance Tuning", "Optimize PostgreSQL", ["postgresql", "performance", "optimization"], ["ubuntu", "centos"], "advanced", [
            {"title": "Configure PostgreSQL", "description": "Tune PostgreSQL settings", "code": "sudo nano /etc/postgresql/16/main/postgresql.conf\n# Modify:\n# shared_buffers = 256MB\n# effective_cache_size = 1GB\n# work_mem = 4MB\nsudo systemctl restart postgresql", "language": "bash"}
        ]),
        
        ("Set Up MySQL Replication", "Configure master-slave replication", ["mysql", "replication", "high-availability"], ["ubuntu", "centos"], "advanced", [
            {"title": "Configure Master", "description": "Set up replication master", "code": "sudo nano /etc/mysql/my.cnf\n# Add:\n# [mysqld]\n# server-id = 1\n# log_bin = /var/log/mysql/mysql-bin.log\n# binlog_do_db = mydb\nsudo systemctl restart mysql", "language": "bash"}
        ]),
        
        ("Install phpMyAdmin", "Web interface for MySQL", ["phpmyadmin", "mysql", "web-interface"], ["ubuntu", "debian"], "beginner", [
            {"title": "Install phpMyAdmin", "description": "Install web interface", "code": "sudo apt update\nsudo apt install phpmyadmin php-mbstring php-zip php-gd php-json php-curl -y", "language": "bash"}
        ]),
        
        ("Install pgAdmin", "Web interface for PostgreSQL", ["pgadmin", "postgresql", "web-interface"], ["ubuntu", "debian"], "beginner", [
            {"title": "Install pgAdmin", "description": "Install PostgreSQL web interface", "code": "curl https://www.pgadmin.org/static/packages_pgadmin_org.pub | sudo apt-key add\nsudo sh -c 'echo \"deb https://ftp.postgresql.org/pub/pgadmin/pgadmin4/apt/$(lsb_release -cs) pgadmin4 main\" > /etc/apt/sources.list.d/pgadmin4.list'\nsudo apt update\nsudo apt install pgadmin4 -y", "language": "bash"}
        ]),
        
        ("Configure Redis Persistence", "Set up Redis data persistence", ["redis", "persistence", "configuration"], ["ubuntu", "centos"], "intermediate", [
            {"title": "Configure RDB Persistence", "description": "Enable Redis snapshots", "code": "sudo nano /etc/redis/redis.conf\n# Modify:\n# save 900 1\n# save 300 10\n# save 60 10000\nsudo systemctl restart redis", "language": "bash"}
        ]),
        
        ("Set Up MySQL Remote Access", "Allow remote MySQL connections", ["mysql", "remote-access", "networking"], ["ubuntu", "centos"], "intermediate", [
            {"title": "Configure MySQL", "description": "Allow remote connections", "code": "sudo nano /etc/mysql/mysql.conf.d/mysqld.cnf\n# Change: bind-address = 0.0.0.0\nsudo systemctl restart mysql", "language": "bash"},
            {"title": "Grant Remote Access", "description": "Create remote user", "code": "mysql -u root -p\nCREATE USER 'remoteuser'@'%' IDENTIFIED BY 'password';\nGRANT ALL PRIVILEGES ON *.* TO 'remoteuser'@'%';\nFLUSH PRIVILEGES;", "language": "sql"}
        ]),
    ],
    
    "web-server": [
        ("Configure Apache Virtual Hosts", "Set up multiple websites", ["apache", "virtualhost", "web-server"], ["ubuntu", "centos"], "intermediate", [
            {"title": "Create Virtual Host", "description": "Configure Apache virtual host", "code": "sudo nano /etc/apache2/sites-available/example.com.conf\n# Add:\n# <VirtualHost *:80>\n#   ServerName example.com\n#   DocumentRoot /var/www/example.com\n# </VirtualHost>\nsudo a2ensite example.com.conf\nsudo systemctl reload apache2", "language": "bash"}
        ]),
        
        ("Configure NGINX Server Blocks", "Set up NGINX sites", ["nginx", "server-block", "web-server"], ["ubuntu", "centos"], "intermediate", [
            {"title": "Create Server Block", "description": "Configure NGINX server block", "code": "sudo nano /etc/nginx/sites-available/example.com\n# Add:\n# server {\n#   listen 80;\n#   server_name example.com;\n#   root /var/www/example.com;\n#   index index.html;\n# }\nsudo ln -s /etc/nginx/sites-available/example.com /etc/nginx/sites-enabled/\nsudo nginx -t\nsudo systemctl reload nginx", "language": "bash"}
        ]),
        
        ("Enable Apache mod_rewrite", "Configure URL rewriting", ["apache", "mod_rewrite", "htaccess"], ["ubuntu", "centos"], "beginner", [
            {"title": "Enable mod_rewrite", "description": "Activate Apache rewrite module", "code": "sudo a2enmod rewrite\nsudo systemctl restart apache2", "language": "bash"}
        ]),
        
        ("Configure NGINX SSL/TLS", "Set up HTTPS on NGINX", ["nginx", "ssl", "https"], ["ubuntu", "centos"], "intermediate", [
            {"title": "Configure SSL", "description": "Add SSL configuration", "code": "sudo nano /etc/nginx/sites-available/example.com\n# Add:\n# server {\n#   listen 443 ssl;\n#   server_name example.com;\n#   ssl_certificate /path/to/cert.pem;\n#   ssl_certificate_key /path/to/key.pem;\n# }\nsudo nginx -t\nsudo systemctl reload nginx", "language": "bash"}
        ]),
        
        ("Configure Apache SSL/TLS", "Set up HTTPS on Apache", ["apache", "ssl", "https"], ["ubuntu", "centos"], "intermediate", [
            {"title": "Enable SSL Module", "description": "Activate Apache SSL", "code": "sudo a2enmod ssl\nsudo a2ensite default-ssl\nsudo systemctl restart apache2", "language": "bash"}
        ]),
        
        ("Set Up Apache MPM", "Configure Apache performance", ["apache", "mpm", "performance"], ["ubuntu", "centos"], "advanced", [
            {"title": "Enable MPM Event", "description": "Use event-driven MPM", "code": "sudo a2dismod mpm_prefork\nsudo a2enmod mpm_event\nsudo systemctl restart apache2", "language": "bash"}
        ]),
        
        ("Configure NGINX Caching", "Enable NGINX proxy cache", ["nginx", "caching", "performance"], ["ubuntu", "centos"], "advanced", [
            {"title": "Set Up Proxy Cache", "description": "Configure NGINX caching", "code": "sudo nano /etc/nginx/nginx.conf\n# Add:\n# proxy_cache_path /var/cache/nginx levels=1:2 keys_zone=my_cache:10m;\n# server {\n#   location / {\n#     proxy_cache my_cache;\n#     proxy_pass http://backend;\n#   }\n# }", "language": "bash"}
        ]),
        
        ("Configure Apache Rate Limiting", "Limit request rates", ["apache", "rate-limit", "security"], ["ubuntu", "centos"], "intermediate", [
            {"title": "Enable mod_evasive", "description": "Install and configure rate limiting", "code": "sudo apt install libapache2-mod-evasive -y\nsudo a2enmod evasive\nsudo systemctl restart apache2", "language": "bash"}
        ]),
        
        ("Set Up NGINX Load Balancing", "Distribute traffic across servers", ["nginx", "load-balancing", "high-availability"], ["ubuntu", "centos"], "advanced", [
            {"title": "Configure Load Balancer", "description": "Set up NGINX load balancing", "code": "sudo nano /etc/nginx/nginx.conf\n# Add:\n# upstream backend {\n#   server 192.168.1.10;\n#   server 192.168.1.11;\n#   server 192.168.1.12;\n# }\n# server {\n#   location / {\n#     proxy_pass http://backend;\n#   }\n# }", "language": "bash"}
        ]),
        
        ("Configure Apache Access Control", "Restrict access by IP", ["apache", "access-control", "security"], ["ubuntu", "centos"], "intermediate", [
            {"title": "Configure IP Restrictions", "description": "Allow/deny by IP address", "code": "sudo nano /etc/apache2/sites-available/example.com.conf\n# Add inside <VirtualHost>:\n# <Directory /var/www/example.com>\n#   Require ip 192.168.1.0/24\n#   Require ip 10.0.0.1\n# </Directory>", "language": "bash"}
        ]),
    ],
    
    "monitoring": [
        ("Monitor System Resources with htop", "Interactive process viewer", ["htop", "monitoring", "processes"], ["ubuntu", "centos", "linux"], "beginner", [
            {"title": "Install htop", "description": "Install interactive process monitor", "code": "sudo apt install htop -y", "language": "bash"},
            {"title": "Run htop", "description": "Launch htop monitor", "code": "htop", "language": "bash"}
        ]),
        
        ("Check Disk Space Usage", "Monitor disk usage", ["disk", "storage", "monitoring"], ["ubuntu", "centos", "linux"], "beginner", [
            {"title": "Check Disk Usage", "description": "View disk space", "code": "df -h\ndf -i  # Check inodes\ndu -sh /var/*", "language": "bash"}
        ]),
        
        ("Monitor System Logs", "View system log files", ["logs", "monitoring", "troubleshooting"], ["ubuntu", "centos", "linux"], "beginner", [
            {"title": "View System Logs", "description": "Check important log files", "code": "sudo tail -f /var/log/syslog  # Ubuntu\nsudo tail -f /var/log/messages # CentOS\nsudo journalctl -f\nsudo journalctl -u nginx -f", "language": "bash"}
        ]),
        
        ("Set Up Nagios Monitoring", "Install Nagios monitoring system", ["nagios", "monitoring", "alerting"], ["ubuntu", "centos"], "advanced", [
            {"title": "Install Nagios", "description": "Install Nagios Core", "code": "sudo apt update\nsudo apt install nagios4 nagios-plugins-contrib nagios-nrpe-plugin -y", "language": "bash"}
        ]),
        
        ("Install Zabbix Agent", "Set up Zabbix monitoring", ["zabbix", "monitoring", "agent"], ["ubuntu", "centos"], "intermediate", [
            {"title": "Install Zabbix Agent", "description": "Install monitoring agent", "code": "wget https://repo.zabbix.com/zabbix/6.0/ubuntu/pool/main/z/zabbix-release/zabbix-release_6.0-4+ubuntu22.04_all.deb\nsudo dpkg -i zabbix-release_6.0-4+ubuntu22.04_all.deb\nsudo apt update\nsudo apt install zabbix-agent -y", "language": "bash"}
        ]),
        
        ("Configure Node Exporter", "Prometheus metrics exporter", ["prometheus", "node-exporter", "monitoring"], ["ubuntu", "centos", "linux"], "intermediate", [
            {"title": "Install Node Exporter", "description": "Set up metrics exporter", "code": "wget https://github.com/prometheus/node_exporter/releases/download/v1.6.1/node_exporter-1.6.1.linux-amd64.tar.gz\ntar xvfz node_exporter-1.6.1.linux-amd64.tar.gz\nsudo mv node_exporter-1.6.1.linux-amd64/node_exporter /usr/local/bin/", "language": "bash"}
        ]),
        
        ("Set Up ELK Stack", "Elasticsearch, Logstash, Kibana", ["elk", "logging", "monitoring"], ["ubuntu", "debian"], "advanced", [
            {"title": "Install Elasticsearch", "description": "Install search engine", "code": "wget -qO - https://artifacts.elastic.co/GPG-KEY-elasticsearch | sudo apt-key add -\necho \"deb https://artifacts.elastic.co/packages/8.x/apt stable main\" | sudo tee -a /etc/apt/sources.list.d/elastic-8.x.list\nsudo apt update\nsudo apt install elasticsearch -y", "language": "bash"}
        ]),
        
        ("Monitor Network with Netdata", "Real-time performance monitoring", ["netdata", "monitoring", "performance"], ["ubuntu", "centos", "linux"], "intermediate", [
            {"title": "Install Netdata", "description": "Install monitoring tool", "code": "bash <(curl -Ss https://my-netdata.io/kickstart.sh)", "language": "bash"}
        ]),
        
        ("Set Up Uptime Monitoring", "Monitor service availability", ["uptime", "monitoring", "availability"], ["ubuntu", "centos", "linux"], "intermediate", [
            {"title": "Create Monitor Script", "description": "Simple uptime monitoring", "code": "#!/bin/bash\nHOST=\"example.com\"\nif ping -c 1 $HOST &> /dev/null; then\n  echo \"$HOST is UP\"\nelse\n  echo \"$HOST is DOWN\"\n  # Send alert\nfi", "language": "bash"}
        ]),
        
        ("Configure Alerting with Alertmanager", "Prometheus alerting", ["alertmanager", "prometheus", "alerts"], ["ubuntu", "centos"], "advanced", [
            {"title": "Install Alertmanager", "description": "Set up alert manager", "code": "wget https://github.com/prometheus/alertmanager/releases/download/v0.26.0/alertmanager-0.26.0.linux-amd64.tar.gz\ntar xvfz alertmanager-0.26.0.linux-amd64.tar.gz\nsudo mv alertmanager-0.26.0.linux-amd64 /opt/alertmanager", "language": "bash"}
        ]),
    ],
    
    "backup": [
        ("Create Automated Backups with rsync", "Sync files and directories", ["rsync", "backup", "automation"], ["ubuntu", "centos", "linux"], "intermediate", [
            {"title": "Basic rsync Backup", "description": "Backup with rsync", "code": "rsync -avz /source/directory/ /backup/destination/\nrsync -avz -e ssh /source/ user@remote:/backup/", "language": "bash"}
        ]),
        
        ("Set Up Duplicity Encrypted Backups", "Encrypted incremental backups", ["duplicity", "backup", "encryption"], ["ubuntu", "debian"], "advanced", [
            {"title": "Install Duplicity", "description": "Install backup tool", "code": "sudo apt install duplicity python3-boto -y", "language": "bash"},
            {"title": "Create Encrypted Backup", "description": "Backup with encryption", "code": "export PASSPHRASE=\"your-secret-passphrase\"\nduplicity /source/directory file:///backup/destination", "language": "bash"}
        ]),
        
        ("Configure Bacula Backup System", "Enterprise backup solution", ["bacula", "backup", "enterprise"], ["ubuntu", "centos"], "advanced", [
            {"title": "Install Bacula", "description": "Install backup system", "code": "sudo apt install bacula-server bacula-client -y", "language": "bash"}
        ]),
        
        ("Create System Image with Clonezilla", "Disk imaging and cloning", ["clonezilla", "backup", "imaging"], ["linux"], "intermediate", [
            {"title": "Install Clonezilla", "description": "Download and create bootable media", "code": "# Download from https://clonezilla.org/downloads.php\n# Create bootable USB with dd command\nsudo dd if=clonezilla.iso of=/dev/sdX bs=4M status=progress", "language": "bash"}
        ]),
        
        ("Backup to AWS S3", "Cloud backup solution", ["s3", "aws", "cloud-backup"], ["ubuntu", "centos", "linux"], "intermediate", [
            {"title": "Install AWS CLI", "description": "Install AWS command line tool", "code": "curl \"https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip\" -o \"awscliv2.zip\"\nunzip awscliv2.zip\nsudo ./aws/install", "language": "bash"},
            {"title": "Sync to S3", "description": "Backup files to S3", "code": "aws s3 sync /local/directory s3://my-backup-bucket/", "language": "bash"}
        ]),
        
        ("Set Up Automated Database Backups", "Schedule database backups", ["database", "backup", "automation"], ["ubuntu", "centos", "linux"], "intermediate", [
            {"title": "Create Backup Script", "description": "Automated database backup", "code": "#!/bin/bash\nDATABASE=\"mydb\"\nBACKUP_DIR=\"/backups/mysql\"\nDATE=$(date +\"%Y%m%d_%H%M%S\")\nmysqldump -u root -p$DB_PASSWORD $DATABASE > $BACKUP_DIR/$DATABASE_$DATE.sql\ngzip $BACKUP_DIR/$DATABASE_$DATE.sql\nfind $BACKUP_DIR -name \"*.gz\" -mtime +7 -delete", "language": "bash"}
        ]),
        
        ("Configure Timeshift Snapshots", "System restore points", ["timeshift", "snapshots", "backup"], ["ubuntu", "linux"], "beginner", [
            {"title": "Install Timeshift", "description": "Install snapshot tool", "code": "sudo apt install timeshift -y", "language": "bash"},
            {"title": "Create Snapshot", "description": "Take system snapshot", "code": "sudo timeshift --create --comments \"Manual backup\"\nsudo timeshift --list", "language": "bash"}
        ]),
        
        ("Backup with Borgbackup", "Deduplicating backup program", ["borgbackup", "backup", "deduplication"], ["ubuntu", "debian"], "intermediate", [
            {"title": "Install Borgbackup", "description": "Install backup tool", "code": "sudo apt install borgbackup -y", "language": "bash"},
            {"title": "Initialize Repository", "description": "Create backup repository", "code": "borg init --encryption=repokey /path/to/repo\nborg create /path/to/repo::backup-$(date +%Y%m%d) /source/directory", "language": "bash"}
        ]),
        
        ("Configure Weekly Full Backups", "Schedule comprehensive backups", ["backup", "automation", "cron"], ["ubuntu", "centos", "linux"], "intermediate", [
            {"title": "Create Backup Script", "description": "Full system backup script", "code": "#!/bin/bash\ntar -czpf /backup/system-$(date +%Y%m%d).tar.gz --exclude=/backup --exclude=/proc --exclude=/tmp --exclude=/mnt --exclude=/dev --exclude=/sys /", "language": "bash"},
            {"title": "Schedule with Cron", "description": "Add to crontab", "code": "crontab -e\n# Add: 0 2 * * 0 /usr/local/bin/backup.sh", "language": "bash"}
        ]),
        
        ("Set Up Offsite Backup Sync", "Remote backup synchronization", ["offsite", "backup", "sync"], ["ubuntu", "centos", "linux"], "advanced", [
            {"title": "Configure SSH Keys", "description": "Set up passwordless SSH", "code": "ssh-keygen -t rsa\nssh-copy-id backup@remote-server", "language": "bash"},
            {"title": "Sync to Remote", "description": "Backup to remote server", "code": "rsync -avz --delete -e ssh /local/backup/ backup@remote-server:/remote/backup/", "language": "bash"}
        ]),
    ]
}

# Function to generate articles
async def generate_articles():
    print("Generating comprehensive article database...")
    
    all_snippets = []
    article_count = 0
    
    for category, articles in snippets_data.items():
        print(f"\n✅ Processing category: {category.upper()}")
        
        for article in articles:
            title, description, tags, os_list, difficulty, steps = article
            
            snippet = {
                'id': str(uuid.uuid4()),
                'title': title,
                'slug': create_slug(title),
                'description': description,
                'category': category,
                'os': os_list,
                'difficulty': difficulty,
                'views': random.randint(1000, 50000),
                'likes': random.randint(50, 1000),
                'author': 'Admin',
                'createdAt': datetime.utcnow(),
                'updatedAt': datetime.utcnow(),
                'tags': tags,
                'steps': steps,
            }
            
            all_snippets.append(snippet)
            article_count += 1
        
        print(f"   Generated {len(articles)} articles for {category}")
    
    # Clear existing snippets and insert new ones
    print(f"\n📊 Total articles generated: {article_count}")
    print("🔄 Clearing existing database...")
    await db.code_snippets.delete_many({})
    
    print("💾 Inserting articles into database...")
    result = await db.code_snippets.insert_many(all_snippets)
    
    print(f"\n✅ SUCCESS! Inserted {len(result.inserted_ids)} articles")
    print("\n📈 Summary by category:")
    for category in snippets_data.keys():
        count = len([s for s in all_snippets if s['category'] == category])
        print(f"   {category.capitalize()}: {count} articles")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(generate_articles())
