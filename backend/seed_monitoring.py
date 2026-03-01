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

MONITORING_ARTICLES = [
    {
        'title': 'Install Zabbix Server on Ubuntu 22.04',
        'description': 'Complete guide to install and configure Zabbix monitoring server on Ubuntu 22.04 LTS.',
        'category': 'monitoring',
        'os': ['ubuntu', 'linux'],
        'difficulty': 'intermediate',
        'tags': ['zabbix', 'monitoring', 'server', 'ubuntu', 'alerting'],
        'steps': [
            {'title': 'Install Prerequisites', 'description': 'Install required packages.', 'code': 'sudo apt update\nsudo apt install -y apache2 mysql-server php php-mysql php-gd php-xml php-bcmath php-mbstring php-ldap libapache2-mod-php', 'language': 'bash'},
            {'title': 'Add Zabbix Repository', 'description': 'Add official Zabbix repository.', 'code': 'wget https://repo.zabbix.com/zabbix/6.4/ubuntu/pool/main/z/zabbix-release/zabbix-release_6.4-1+ubuntu22.04_all.deb\nsudo dpkg -i zabbix-release_6.4-1+ubuntu22.04_all.deb\nsudo apt update', 'language': 'bash'},
            {'title': 'Install Zabbix Components', 'description': 'Install Zabbix server, frontend, and agent.', 'code': 'sudo apt install -y zabbix-server-mysql zabbix-frontend-php zabbix-apache-conf zabbix-sql-scripts zabbix-agent', 'language': 'bash'},
            {'title': 'Create Database', 'description': 'Setup MySQL database for Zabbix.', 'code': 'sudo mysql -u root -p\n\nCREATE DATABASE zabbix CHARACTER SET utf8mb4 COLLATE utf8mb4_bin;\nCREATE USER \'zabbix\'@\'localhost\' IDENTIFIED BY \'YourStrongPassword\';\nGRANT ALL PRIVILEGES ON zabbix.* TO \'zabbix\'@\'localhost\';\nSET GLOBAL log_bin_trust_function_creators = 1;\nQUIT;\n\n# Import schema\nzcat /usr/share/zabbix-sql-scripts/mysql/server.sql.gz | mysql -u zabbix -p zabbix', 'language': 'bash'},
            {'title': 'Configure Zabbix Server', 'description': 'Edit Zabbix configuration file.', 'code': 'sudo nano /etc/zabbix/zabbix_server.conf\n\n# Set database password\nDBPassword=YourStrongPassword\n\n# Save and start services\nsudo systemctl restart zabbix-server zabbix-agent apache2\nsudo systemctl enable zabbix-server zabbix-agent apache2', 'language': 'bash'}
        ],
        'postInstallation': {'title': 'Access Web Interface', 'content': 'Open http://your-server-ip/zabbix in browser. Default login: Admin / zabbix. Complete setup wizard and change admin password immediately.'}
    },
    {
        'title': 'Install Nagios Core on CentOS/RHEL',
        'description': 'Install and configure Nagios Core monitoring system on CentOS or RHEL servers.',
        'category': 'monitoring',
        'os': ['centos', 'rhel', 'linux'],
        'difficulty': 'intermediate',
        'tags': ['nagios', 'monitoring', 'centos', 'alerting', 'infrastructure'],
        'steps': [
            {'title': 'Install Dependencies', 'description': 'Install required packages.', 'code': 'sudo yum install -y gcc glibc glibc-common wget unzip httpd php gd gd-devel perl postfix make gettext automake autoconf openssl-devel net-snmp net-snmp-utils', 'language': 'bash'},
            {'title': 'Create Nagios User', 'description': 'Create user and group for Nagios.', 'code': 'sudo useradd nagios\nsudo groupadd nagcmd\nsudo usermod -a -G nagcmd nagios\nsudo usermod -a -G nagcmd apache', 'language': 'bash'},
            {'title': 'Download and Compile Nagios', 'description': 'Build Nagios from source.', 'code': 'cd /tmp\nwget https://assets.nagios.com/downloads/nagioscore/releases/nagios-4.4.13.tar.gz\ntar xzf nagios-4.4.13.tar.gz\ncd nagios-4.4.13\n\n./configure --with-command-group=nagcmd\nmake all\nsudo make install\nsudo make install-init\nsudo make install-config\nsudo make install-commandmode\nsudo make install-webconf', 'language': 'bash'},
            {'title': 'Install Nagios Plugins', 'description': 'Download and install monitoring plugins.', 'code': 'cd /tmp\nwget https://nagios-plugins.org/download/nagios-plugins-2.4.6.tar.gz\ntar xzf nagios-plugins-2.4.6.tar.gz\ncd nagios-plugins-2.4.6\n\n./configure --with-nagios-user=nagios --with-nagios-group=nagios\nmake\nsudo make install', 'language': 'bash'},
            {'title': 'Configure and Start', 'description': 'Set admin password and start services.', 'code': '# Set admin password\nsudo htpasswd -c /usr/local/nagios/etc/htpasswd.users nagiosadmin\n\n# Verify configuration\nsudo /usr/local/nagios/bin/nagios -v /usr/local/nagios/etc/nagios.cfg\n\n# Start services\nsudo systemctl start nagios\nsudo systemctl start httpd\nsudo systemctl enable nagios httpd', 'language': 'bash'}
        ],
        'postInstallation': {'title': 'Access Nagios', 'content': 'Open http://your-server-ip/nagios. Login with nagiosadmin and password you set. Add hosts and services to monitor in /usr/local/nagios/etc/objects/ directory.'}
    },
    {
        'title': 'Install Prometheus and Grafana Stack',
        'description': 'Setup Prometheus for metrics collection and Grafana for visualization on Ubuntu.',
        'category': 'monitoring',
        'os': ['ubuntu', 'linux'],
        'difficulty': 'intermediate',
        'tags': ['prometheus', 'grafana', 'monitoring', 'metrics', 'visualization'],
        'steps': [
            {'title': 'Install Prometheus', 'description': 'Download and setup Prometheus.', 'code': '# Create user\nsudo useradd --no-create-home --shell /bin/false prometheus\n\n# Download Prometheus\ncd /tmp\nwget https://github.com/prometheus/prometheus/releases/download/v2.47.0/prometheus-2.47.0.linux-amd64.tar.gz\ntar xvfz prometheus-*.tar.gz\ncd prometheus-*\n\n# Copy files\nsudo cp prometheus promtool /usr/local/bin/\nsudo cp -r consoles console_libraries /etc/prometheus/\nsudo cp prometheus.yml /etc/prometheus/', 'language': 'bash'},
            {'title': 'Create Prometheus Service', 'description': 'Setup systemd service for Prometheus.', 'code': 'sudo nano /etc/systemd/system/prometheus.service\n\n[Unit]\nDescription=Prometheus\nWants=network-online.target\nAfter=network-online.target\n\n[Service]\nUser=prometheus\nGroup=prometheus\nType=simple\nExecStart=/usr/local/bin/prometheus \\\n    --config.file /etc/prometheus/prometheus.yml \\\n    --storage.tsdb.path /var/lib/prometheus/ \\\n    --web.console.templates=/etc/prometheus/consoles \\\n    --web.console.libraries=/etc/prometheus/console_libraries\n\n[Install]\nWantedBy=multi-user.target', 'language': 'bash'},
            {'title': 'Install Grafana', 'description': 'Add Grafana repository and install.', 'code': '# Add Grafana GPG key\nwget -q -O - https://packages.grafana.com/gpg.key | sudo apt-key add -\n\n# Add repository\necho "deb https://packages.grafana.com/oss/deb stable main" | sudo tee /etc/apt/sources.list.d/grafana.list\n\n# Install\nsudo apt update\nsudo apt install -y grafana\n\n# Start services\nsudo systemctl daemon-reload\nsudo systemctl start prometheus grafana-server\nsudo systemctl enable prometheus grafana-server', 'language': 'bash'},
            {'title': 'Configure Grafana Data Source', 'description': 'Add Prometheus as data source in Grafana.', 'code': 'Access Grafana:\n1. Open http://your-server-ip:3000\n2. Login: admin / admin\n3. Change password\n\nAdd Data Source:\n1. Configuration → Data Sources\n2. Add data source → Prometheus\n3. URL: http://localhost:9090\n4. Click "Save & Test"\n\nImport Dashboard:\n1. Create → Import\n2. Enter ID: 1860 (Node Exporter Full)\n3. Select Prometheus data source\n4. Import', 'language': 'bash'}
        ],
        'postInstallation': {'title': 'Next Steps', 'content': 'Install Node Exporter on servers to monitor. Add alerting rules in Prometheus. Setup Alertmanager for notifications. Create custom Grafana dashboards.'}
    },
    {
        'title': 'Install Netdata Real-time Monitoring',
        'description': 'Quick installation of Netdata for real-time server performance monitoring.',
        'category': 'monitoring',
        'os': ['ubuntu', 'centos', 'linux'],
        'difficulty': 'beginner',
        'tags': ['netdata', 'monitoring', 'real-time', 'performance', 'server'],
        'steps': [
            {'title': 'One-Line Installation', 'description': 'Install Netdata using official script.', 'code': '# Ubuntu/Debian\nbash <(curl -Ss https://my-netdata.io/kickstart.sh)\n\n# CentOS/RHEL\nbash <(curl -Ss https://my-netdata.io/kickstart.sh)\n\n# Follow prompts and wait for installation', 'language': 'bash'},
            {'title': 'Manual Installation (Ubuntu)', 'description': 'Step-by-step manual install.', 'code': '# Install dependencies\nsudo apt install -y zlib1g-dev uuid-dev libuv1-dev liblz4-dev libssl-dev libelf-dev libmnl-dev libprotobuf-dev protobuf-compiler gcc g++ make git autoconf autoconf-archive autogen automake pkg-config curl python3\n\n# Clone and install\ngit clone https://github.com/netdata/netdata.git --depth=100 --recursive\ncd netdata\nsudo ./netdata-installer.sh', 'language': 'bash'},
            {'title': 'Start and Enable Service', 'description': 'Ensure Netdata runs on boot.', 'code': '# Start Netdata\nsudo systemctl start netdata\nsudo systemctl enable netdata\n\n# Check status\nsudo systemctl status netdata\n\n# Netdata runs on port 19999 by default', 'language': 'bash'},
            {'title': 'Configure Firewall', 'description': 'Allow Netdata port through firewall.', 'code': '# UFW (Ubuntu)\nsudo ufw allow 19999/tcp\n\n# Firewalld (CentOS)\nsudo firewall-cmd --permanent --add-port=19999/tcp\nsudo firewall-cmd --reload\n\n# Access dashboard\nhttp://your-server-ip:19999', 'language': 'bash'}
        ],
        'postInstallation': {'title': 'Features', 'content': 'Netdata provides real-time metrics for CPU, memory, disk, network, and 200+ applications. Zero configuration needed. Add Netdata Cloud account for multi-server monitoring.'}
    },
    {
        'title': 'Install Uptime Kuma Self-Hosted Monitoring',
        'description': 'Setup Uptime Kuma for website and service uptime monitoring with notifications.',
        'category': 'monitoring',
        'os': ['ubuntu', 'linux'],
        'difficulty': 'beginner',
        'tags': ['uptime-kuma', 'monitoring', 'uptime', 'docker', 'alerting'],
        'steps': [
            {'title': 'Install Docker', 'description': 'Install Docker if not already installed.', 'code': '# Install Docker\ncurl -fsSL https://get.docker.com -o get-docker.sh\nsudo sh get-docker.sh\n\n# Add user to docker group\nsudo usermod -aG docker $USER\n\n# Start Docker\nsudo systemctl start docker\nsudo systemctl enable docker', 'language': 'bash'},
            {'title': 'Run Uptime Kuma Container', 'description': 'Deploy Uptime Kuma using Docker.', 'code': 'docker run -d \\\n  --name uptime-kuma \\\n  --restart=always \\\n  -p 3001:3001 \\\n  -v uptime-kuma:/app/data \\\n  louislam/uptime-kuma:1\n\n# Check container status\ndocker ps', 'language': 'bash'},
            {'title': 'Access and Setup', 'description': 'Configure Uptime Kuma.', 'code': '1. Open http://your-server-ip:3001\n2. Create admin account\n3. Add monitors:\n   - Click "Add New Monitor"\n   - Monitor Type: HTTP(s)\n   - Friendly Name: My Website\n   - URL: https://example.com\n   - Heartbeat Interval: 60 seconds\n   - Click "Save"', 'language': 'bash'},
            {'title': 'Setup Notifications', 'description': 'Configure alerting channels.', 'code': 'Settings → Notifications:\n\n1. Telegram:\n   - Create bot via @BotFather\n   - Get Chat ID\n   - Enter Bot Token and Chat ID\n\n2. Discord:\n   - Create Webhook in Discord channel\n   - Paste Webhook URL\n\n3. Email (SMTP):\n   - Enter SMTP server details\n   - From/To email addresses\n\n4. Slack, Teams, Pushover also supported', 'language': 'bash'}
        ],
        'postInstallation': {'title': 'Monitoring Types', 'content': 'Uptime Kuma supports HTTP(s), TCP, Ping, DNS, Docker containers, Steam servers, and more. Setup status pages for public display. Configure maintenance windows.'}
    },
    {
        'title': 'Linux Server Health Check Commands',
        'description': 'Essential Linux commands to monitor server health, CPU, memory, disk, and network.',
        'category': 'monitoring',
        'os': ['ubuntu', 'centos', 'linux'],
        'difficulty': 'beginner',
        'tags': ['linux', 'monitoring', 'commands', 'health-check', 'performance'],
        'steps': [
            {'title': 'CPU and Memory Monitoring', 'description': 'Check CPU and RAM usage.', 'code': '# Real-time process monitoring\ntop\nhtop  # More user-friendly (install: apt install htop)\n\n# CPU info\nlscpu\ncat /proc/cpuinfo\n\n# Memory usage\nfree -h\ncat /proc/meminfo\n\n# System load average\nuptime\ncat /proc/loadavg', 'language': 'bash'},
            {'title': 'Disk Space and I/O', 'description': 'Monitor storage and disk performance.', 'code': '# Disk space usage\ndf -h\n\n# Directory sizes\ndu -sh /var/*\ndu -h --max-depth=1 /\n\n# Disk I/O statistics\niostat -x 1  # (install: apt install sysstat)\n\n# Check for disk errors\nsudo dmesg | grep -i error\n\n# Disk health (SMART)\nsudo smartctl -a /dev/sda  # (install: apt install smartmontools)', 'language': 'bash'},
            {'title': 'Network Monitoring', 'description': 'Check network connections and bandwidth.', 'code': '# Active connections\nnetstat -tuln\nss -tuln  # Modern alternative\n\n# Network interface stats\nifconfig\nip addr\n\n# Bandwidth usage\niftop  # (install: apt install iftop)\nnethogs  # Per-process bandwidth\n\n# Check open ports\nsudo lsof -i -P -n | grep LISTEN\n\n# DNS resolution\ndig google.com\nnslookup google.com', 'language': 'bash'},
            {'title': 'Process and Service Monitoring', 'description': 'Monitor running processes and services.', 'code': '# List all processes\nps aux\nps aux | grep nginx\n\n# Process tree\npstree\n\n# Service status\nsystemctl status nginx\nsystemctl list-units --type=service --state=running\n\n# Failed services\nsystemctl --failed\n\n# System logs\njournalctl -xe\njournalctl -u nginx --since "1 hour ago"\ntail -f /var/log/syslog', 'language': 'bash'}
        ],
        'postInstallation': {'title': 'Automation', 'content': 'Create cron jobs to run health checks periodically. Use tools like Monit for automatic service restart. Setup logwatch for daily log summaries via email.'}
    },
    {
        'title': 'Setup Server Monitoring Alerts with Monit',
        'description': 'Install and configure Monit for automatic process monitoring and restart.',
        'category': 'monitoring',
        'os': ['ubuntu', 'centos', 'linux'],
        'difficulty': 'intermediate',
        'tags': ['monit', 'monitoring', 'alerting', 'automation', 'process-manager'],
        'steps': [
            {'title': 'Install Monit', 'description': 'Install Monit package.', 'code': '# Ubuntu/Debian\nsudo apt update\nsudo apt install -y monit\n\n# CentOS/RHEL\nsudo yum install -y epel-release\nsudo yum install -y monit\n\n# Start service\nsudo systemctl start monit\nsudo systemctl enable monit', 'language': 'bash'},
            {'title': 'Configure Monit', 'description': 'Edit main configuration file.', 'code': 'sudo nano /etc/monit/monitrc\n\n# Enable web interface\nset httpd port 2812 and\n    use address 0.0.0.0\n    allow admin:monit123\n\n# Set mail server for alerts\nset mailserver smtp.gmail.com port 587\n    username "your@gmail.com"\n    password "app-password"\n    using tlsv12\n\nset alert your@email.com\n\n# Check interval\nset daemon 60', 'language': 'bash'},
            {'title': 'Add Service Monitors', 'description': 'Create monitoring rules for services.', 'code': 'sudo nano /etc/monit/conf.d/services.conf\n\n# Monitor Nginx\ncheck process nginx with pidfile /var/run/nginx.pid\n    start program = "/usr/bin/systemctl start nginx"\n    stop program = "/usr/bin/systemctl stop nginx"\n    if failed host 127.0.0.1 port 80 then restart\n    if 3 restarts within 5 cycles then alert\n\n# Monitor MySQL\ncheck process mysql with pidfile /var/run/mysqld/mysqld.pid\n    start program = "/usr/bin/systemctl start mysql"\n    stop program = "/usr/bin/systemctl stop mysql"\n    if failed port 3306 then restart', 'language': 'bash'},
            {'title': 'Add Resource Monitors', 'description': 'Monitor system resources.', 'code': 'sudo nano /etc/monit/conf.d/system.conf\n\n# System resources\ncheck system $HOST\n    if loadavg (1min) > 4 then alert\n    if loadavg (5min) > 2 then alert\n    if memory usage > 80% then alert\n    if swap usage > 25% then alert\n    if cpu usage > 95% for 10 cycles then alert\n\n# Disk space\ncheck filesystem rootfs with path /\n    if space usage > 85% then alert\n    if inode usage > 85% then alert\n\n# Reload Monit\nsudo monit reload\nsudo monit status', 'language': 'bash'}
        ],
        'postInstallation': {'title': 'Access Monit', 'content': 'Web interface: http://your-server-ip:2812 (admin/monit123). Commands: monit status, monit summary, monit start nginx, monit stop nginx.'}
    },
    {
        'title': 'Configure CloudWatch Monitoring for AWS EC2',
        'description': 'Setup AWS CloudWatch for EC2 instance monitoring with custom metrics and alarms.',
        'category': 'monitoring',
        'os': ['ubuntu', 'linux'],
        'difficulty': 'intermediate',
        'tags': ['aws', 'cloudwatch', 'ec2', 'monitoring', 'cloud'],
        'steps': [
            {'title': 'Install CloudWatch Agent', 'description': 'Download and install CloudWatch agent.', 'code': '# Download agent\nwget https://s3.amazonaws.com/amazoncloudwatch-agent/ubuntu/amd64/latest/amazon-cloudwatch-agent.deb\n\n# Install\nsudo dpkg -i amazon-cloudwatch-agent.deb\n\n# Verify installation\namazon-cloudwatch-agent-ctl -h', 'language': 'bash'},
            {'title': 'Create IAM Role', 'description': 'Attach CloudWatch permissions to EC2.', 'code': 'In AWS Console:\n\n1. IAM → Roles → Create Role\n2. Select EC2\n3. Attach policies:\n   - CloudWatchAgentServerPolicy\n   - AmazonSSMManagedInstanceCore\n4. Name: EC2-CloudWatch-Role\n5. Create role\n\n6. EC2 → Select instance → Actions\n7. Security → Modify IAM role\n8. Attach EC2-CloudWatch-Role', 'language': 'bash'},
            {'title': 'Configure CloudWatch Agent', 'description': 'Run configuration wizard.', 'code': '# Run wizard\nsudo /opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent-config-wizard\n\nAnswers for basic setup:\n- OS: Linux\n- EC2 or On-premises: EC2\n- User: root\n- StatsD daemon: No\n- CollectD: No\n- Monitor metrics: Yes\n- Monitor CPU per core: Yes\n- Add EC2 dimensions: Yes\n- Aggregation interval: 60 seconds\n- Default metrics config: Basic\n- Monitor log files: Yes\n- Log file path: /var/log/syslog\n- Log group name: /ec2/syslog', 'language': 'bash'},
            {'title': 'Start Agent and Create Alarms', 'description': 'Start agent and setup CloudWatch alarms.', 'code': '# Start agent\nsudo /opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent-ctl \\\n    -a fetch-config \\\n    -m ec2 \\\n    -c file:/opt/aws/amazon-cloudwatch-agent/bin/config.json \\\n    -s\n\n# Check status\nsudo systemctl status amazon-cloudwatch-agent\n\n# Create Alarm in AWS Console:\n# CloudWatch → Alarms → Create Alarm\n# - Select metric: EC2 → Per-Instance\n# - CPU Utilization > 80% for 5 minutes\n# - Notification: Create SNS topic\n# - Add email for alerts', 'language': 'bash'}
        ],
        'postInstallation': {'title': 'Custom Metrics', 'content': 'CloudWatch agent can collect memory, disk, and custom application metrics. Create dashboards in CloudWatch for visualization. Setup billing alarms to monitor AWS costs.'}
    }
]

async def seed_monitoring():
    print("=" * 60)
    print("  SEEDING: Monitoring Articles")
    print("=" * 60)
    
    added = 0
    for article in MONITORING_ARTICLES:
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
    
    print(f"\n✓ Added {added} Monitoring articles")
    total = await db.code_snippets.count_documents({'category': 'monitoring'})
    print(f"Total Monitoring articles: {total}")

if __name__ == "__main__":
    asyncio.run(seed_monitoring())
