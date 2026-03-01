from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
from pathlib import Path
import asyncio
from datetime import datetime, timezone
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

# More Installation Articles
installation_articles = [
    {
        'title': 'Install Docker on Ubuntu 22.04',
        'description': 'Complete guide to install Docker Engine and Docker Compose on Ubuntu 22.04 LTS.',
        'category': 'installation',
        'os': ['ubuntu', 'linux'],
        'difficulty': 'beginner',
        'tags': ['docker', 'ubuntu', 'containers', 'installation'],
        'steps': [
            {'title': 'Update System', 'description': 'Update package index.', 'code': 'sudo apt update && sudo apt upgrade -y', 'language': 'bash'},
            {'title': 'Install Prerequisites', 'description': 'Install required packages.', 'code': 'sudo apt install apt-transport-https ca-certificates curl software-properties-common -y', 'language': 'bash'},
            {'title': 'Add Docker GPG Key', 'description': 'Add official Docker GPG key.', 'code': 'curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg', 'language': 'bash'},
            {'title': 'Add Docker Repository', 'description': 'Add Docker repository to sources.', 'code': 'echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null', 'language': 'bash'},
            {'title': 'Install Docker', 'description': 'Install Docker Engine.', 'code': 'sudo apt update\nsudo apt install docker-ce docker-ce-cli containerd.io docker-compose-plugin -y', 'language': 'bash'},
            {'title': 'Start Docker', 'description': 'Enable and start Docker service.', 'code': 'sudo systemctl enable docker\nsudo systemctl start docker\nsudo docker --version', 'language': 'bash'}
        ],
        'postInstallation': {'title': 'Post Installation', 'content': 'Add your user to docker group: sudo usermod -aG docker $USER. Log out and back in.'}
    },
    {
        'title': 'Install Kubernetes with kubeadm',
        'description': 'Set up a Kubernetes cluster using kubeadm on Ubuntu servers.',
        'category': 'installation',
        'os': ['ubuntu', 'linux'],
        'difficulty': 'advanced',
        'tags': ['kubernetes', 'k8s', 'kubeadm', 'cluster', 'containers'],
        'steps': [
            {'title': 'Disable Swap', 'description': 'Kubernetes requires swap to be disabled.', 'code': 'sudo swapoff -a\nsudo sed -i \'/ swap / s/^/#/\' /etc/fstab', 'language': 'bash'},
            {'title': 'Load Kernel Modules', 'description': 'Load required kernel modules.', 'code': 'cat <<EOF | sudo tee /etc/modules-load.d/k8s.conf\noverlay\nbr_netfilter\nEOF\nsudo modprobe overlay\nsudo modprobe br_netfilter', 'language': 'bash'},
            {'title': 'Configure Sysctl', 'description': 'Set up networking parameters.', 'code': 'cat <<EOF | sudo tee /etc/sysctl.d/k8s.conf\nnet.bridge.bridge-nf-call-iptables  = 1\nnet.bridge.bridge-nf-call-ip6tables = 1\nnet.ipv4.ip_forward                 = 1\nEOF\nsudo sysctl --system', 'language': 'bash'},
            {'title': 'Install containerd', 'description': 'Install container runtime.', 'code': 'sudo apt install containerd -y\nsudo mkdir -p /etc/containerd\ncontainerd config default | sudo tee /etc/containerd/config.toml\nsudo systemctl restart containerd', 'language': 'bash'},
            {'title': 'Add Kubernetes Repository', 'description': 'Add official K8s repository.', 'code': 'sudo apt install -y apt-transport-https ca-certificates curl\ncurl -fsSL https://pkgs.k8s.io/core:/stable:/v1.29/deb/Release.key | sudo gpg --dearmor -o /etc/apt/keyrings/kubernetes-apt-keyring.gpg\necho "deb [signed-by=/etc/apt/keyrings/kubernetes-apt-keyring.gpg] https://pkgs.k8s.io/core:/stable:/v1.29/deb/ /" | sudo tee /etc/apt/sources.list.d/kubernetes.list', 'language': 'bash'},
            {'title': 'Install Kubernetes Components', 'description': 'Install kubeadm, kubelet, kubectl.', 'code': 'sudo apt update\nsudo apt install -y kubelet kubeadm kubectl\nsudo apt-mark hold kubelet kubeadm kubectl', 'language': 'bash'},
            {'title': 'Initialize Cluster (Master)', 'description': 'Initialize the cluster on master node.', 'code': 'sudo kubeadm init --pod-network-cidr=10.244.0.0/16\nmkdir -p $HOME/.kube\nsudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config\nsudo chown $(id -u):$(id -g) $HOME/.kube/config', 'language': 'bash'}
        ],
        'postInstallation': {'title': 'Next Steps', 'content': 'Install a CNI plugin like Flannel or Calico. Join worker nodes using the kubeadm join command.'}
    },
    {
        'title': 'Install Jenkins CI/CD Server',
        'description': 'Set up Jenkins automation server for continuous integration and deployment.',
        'category': 'installation',
        'os': ['ubuntu', 'debian', 'linux'],
        'difficulty': 'intermediate',
        'tags': ['jenkins', 'cicd', 'automation', 'devops'],
        'steps': [
            {'title': 'Install Java', 'description': 'Jenkins requires Java 11 or 17.', 'code': 'sudo apt update\nsudo apt install openjdk-17-jdk -y\njava -version', 'language': 'bash'},
            {'title': 'Add Jenkins Repository', 'description': 'Add official Jenkins repo.', 'code': 'curl -fsSL https://pkg.jenkins.io/debian-stable/jenkins.io-2023.key | sudo tee /usr/share/keyrings/jenkins-keyring.asc > /dev/null\necho deb [signed-by=/usr/share/keyrings/jenkins-keyring.asc] https://pkg.jenkins.io/debian-stable binary/ | sudo tee /etc/apt/sources.list.d/jenkins.list > /dev/null', 'language': 'bash'},
            {'title': 'Install Jenkins', 'description': 'Install Jenkins package.', 'code': 'sudo apt update\nsudo apt install jenkins -y', 'language': 'bash'},
            {'title': 'Start Jenkins', 'description': 'Enable and start Jenkins service.', 'code': 'sudo systemctl enable jenkins\nsudo systemctl start jenkins\nsudo systemctl status jenkins', 'language': 'bash'},
            {'title': 'Get Initial Password', 'description': 'Retrieve admin password for setup.', 'code': 'sudo cat /var/lib/jenkins/secrets/initialAdminPassword', 'language': 'bash'},
            {'title': 'Access Jenkins', 'description': 'Open Jenkins in browser.', 'code': '# Open browser:\nhttp://your_server_ip:8080\n\n# Enter initial admin password\n# Install suggested plugins\n# Create admin user', 'language': 'text'}
        ],
        'postInstallation': {'title': 'Post Setup', 'content': 'Install recommended plugins. Configure security settings. Set up your first pipeline job.'}
    },
    {
        'title': 'Install GitLab CE on Ubuntu',
        'description': 'Deploy GitLab Community Edition for self-hosted Git repository management.',
        'category': 'installation',
        'os': ['ubuntu', 'linux'],
        'difficulty': 'intermediate',
        'tags': ['gitlab', 'git', 'devops', 'repository'],
        'steps': [
            {'title': 'Install Dependencies', 'description': 'Install required packages.', 'code': 'sudo apt update\nsudo apt install -y curl openssh-server ca-certificates tzdata perl', 'language': 'bash'},
            {'title': 'Add GitLab Repository', 'description': 'Add official GitLab repo.', 'code': 'curl https://packages.gitlab.com/install/repositories/gitlab/gitlab-ce/script.deb.sh | sudo bash', 'language': 'bash'},
            {'title': 'Install GitLab', 'description': 'Install GitLab CE with your domain.', 'code': 'sudo EXTERNAL_URL="https://gitlab.yourdomain.com" apt install gitlab-ce', 'language': 'bash'},
            {'title': 'Configure GitLab', 'description': 'Run initial configuration.', 'code': 'sudo gitlab-ctl reconfigure', 'language': 'bash'},
            {'title': 'Get Root Password', 'description': 'Retrieve initial root password.', 'code': 'sudo cat /etc/gitlab/initial_root_password', 'language': 'bash'}
        ],
        'postInstallation': {'title': 'Access GitLab', 'content': 'Open your domain in browser. Login as root with initial password. Change password immediately.'}
    },
    {
        'title': 'Install Ansible Automation Platform',
        'description': 'Set up Ansible for IT automation and configuration management.',
        'category': 'installation',
        'os': ['ubuntu', 'centos', 'linux'],
        'difficulty': 'beginner',
        'tags': ['ansible', 'automation', 'devops', 'configuration'],
        'steps': [
            {'title': 'Install Ansible (Ubuntu)', 'description': 'Install on Ubuntu/Debian.', 'code': 'sudo apt update\nsudo apt install software-properties-common -y\nsudo add-apt-repository --yes --update ppa:ansible/ansible\nsudo apt install ansible -y', 'language': 'bash'},
            {'title': 'Install Ansible (CentOS)', 'description': 'Install on CentOS/RHEL.', 'code': 'sudo dnf install epel-release -y\nsudo dnf install ansible -y', 'language': 'bash'},
            {'title': 'Verify Installation', 'description': 'Check Ansible version.', 'code': 'ansible --version', 'language': 'bash'},
            {'title': 'Configure Inventory', 'description': 'Set up hosts inventory file.', 'code': 'sudo nano /etc/ansible/hosts\n\n# Add your servers:\n[webservers]\nweb1.example.com\nweb2.example.com\n\n[dbservers]\ndb1.example.com', 'language': 'bash'},
            {'title': 'Test Connection', 'description': 'Test connectivity to hosts.', 'code': 'ansible all -m ping', 'language': 'bash'}
        ],
        'postInstallation': {'title': 'Getting Started', 'content': 'Set up SSH keys for passwordless authentication. Create your first playbook. Explore Ansible Galaxy for roles.'}
    },
    {
        'title': 'Install Terraform Infrastructure Tool',
        'description': 'Set up Terraform for infrastructure as code deployment.',
        'category': 'installation',
        'os': ['ubuntu', 'centos', 'linux'],
        'difficulty': 'intermediate',
        'tags': ['terraform', 'iac', 'devops', 'cloud'],
        'steps': [
            {'title': 'Install Dependencies', 'description': 'Install required packages.', 'code': 'sudo apt update\nsudo apt install -y gnupg software-properties-common', 'language': 'bash'},
            {'title': 'Add HashiCorp GPG Key', 'description': 'Add official HashiCorp key.', 'code': 'wget -O- https://apt.releases.hashicorp.com/gpg | gpg --dearmor | sudo tee /usr/share/keyrings/hashicorp-archive-keyring.gpg', 'language': 'bash'},
            {'title': 'Add Repository', 'description': 'Add HashiCorp repository.', 'code': 'echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/hashicorp.list', 'language': 'bash'},
            {'title': 'Install Terraform', 'description': 'Install Terraform package.', 'code': 'sudo apt update\nsudo apt install terraform -y\nterraform -version', 'language': 'bash'},
            {'title': 'Initialize Project', 'description': 'Create first Terraform config.', 'code': 'mkdir terraform-demo && cd terraform-demo\ncat > main.tf << EOF\nterraform {\n  required_version = ">= 1.0"\n}\n\nresource "local_file" "hello" {\n  content  = "Hello, Terraform!"\n  filename = "hello.txt"\n}\nEOF\nterraform init\nterraform plan\nterraform apply', 'language': 'bash'}
        ],
        'postInstallation': {'title': 'Next Steps', 'content': 'Configure cloud provider credentials. Learn HCL syntax. Explore Terraform modules and state management.'}
    },
    {
        'title': 'Install Prometheus Monitoring',
        'description': 'Deploy Prometheus for metrics collection and monitoring.',
        'category': 'installation',
        'os': ['ubuntu', 'linux'],
        'difficulty': 'intermediate',
        'tags': ['prometheus', 'monitoring', 'metrics', 'devops'],
        'steps': [
            {'title': 'Create User', 'description': 'Create Prometheus system user.', 'code': 'sudo useradd --no-create-home --shell /bin/false prometheus\nsudo mkdir /etc/prometheus\nsudo mkdir /var/lib/prometheus', 'language': 'bash'},
            {'title': 'Download Prometheus', 'description': 'Download latest release.', 'code': 'cd /tmp\nwget https://github.com/prometheus/prometheus/releases/download/v2.47.0/prometheus-2.47.0.linux-amd64.tar.gz\ntar xvfz prometheus-*.tar.gz\ncd prometheus-*', 'language': 'bash'},
            {'title': 'Install Binaries', 'description': 'Copy binaries and configs.', 'code': 'sudo cp prometheus promtool /usr/local/bin/\nsudo cp -r consoles/ console_libraries/ /etc/prometheus/\nsudo cp prometheus.yml /etc/prometheus/', 'language': 'bash'},
            {'title': 'Set Permissions', 'description': 'Configure ownership.', 'code': 'sudo chown -R prometheus:prometheus /etc/prometheus\nsudo chown -R prometheus:prometheus /var/lib/prometheus\nsudo chown prometheus:prometheus /usr/local/bin/prometheus\nsudo chown prometheus:prometheus /usr/local/bin/promtool', 'language': 'bash'},
            {'title': 'Create Service', 'description': 'Create systemd service file.', 'code': 'sudo tee /etc/systemd/system/prometheus.service << EOF\n[Unit]\nDescription=Prometheus\nWants=network-online.target\nAfter=network-online.target\n\n[Service]\nUser=prometheus\nGroup=prometheus\nType=simple\nExecStart=/usr/local/bin/prometheus \\\\\n  --config.file /etc/prometheus/prometheus.yml \\\\\n  --storage.tsdb.path /var/lib/prometheus/ \\\\\n  --web.console.templates=/etc/prometheus/consoles \\\\\n  --web.console.libraries=/etc/prometheus/console_libraries\n\n[Install]\nWantedBy=multi-user.target\nEOF', 'language': 'bash'},
            {'title': 'Start Prometheus', 'description': 'Enable and start service.', 'code': 'sudo systemctl daemon-reload\nsudo systemctl enable prometheus\nsudo systemctl start prometheus\nsudo systemctl status prometheus', 'language': 'bash'}
        ],
        'postInstallation': {'title': 'Access Prometheus', 'content': 'Open http://your_server:9090 in browser. Configure targets in prometheus.yml. Install Grafana for visualization.'}
    },
    {
        'title': 'Install Grafana Dashboard',
        'description': 'Set up Grafana for data visualization and dashboards.',
        'category': 'installation',
        'os': ['ubuntu', 'linux'],
        'difficulty': 'beginner',
        'tags': ['grafana', 'monitoring', 'dashboard', 'visualization'],
        'steps': [
            {'title': 'Add GPG Key', 'description': 'Add Grafana GPG key.', 'code': 'sudo apt install -y apt-transport-https software-properties-common\nwget -q -O - https://apt.grafana.com/gpg.key | gpg --dearmor | sudo tee /usr/share/keyrings/grafana.gpg > /dev/null', 'language': 'bash'},
            {'title': 'Add Repository', 'description': 'Add Grafana repository.', 'code': 'echo "deb [signed-by=/usr/share/keyrings/grafana.gpg] https://apt.grafana.com stable main" | sudo tee /etc/apt/sources.list.d/grafana.list', 'language': 'bash'},
            {'title': 'Install Grafana', 'description': 'Install Grafana package.', 'code': 'sudo apt update\nsudo apt install grafana -y', 'language': 'bash'},
            {'title': 'Start Grafana', 'description': 'Enable and start service.', 'code': 'sudo systemctl enable grafana-server\nsudo systemctl start grafana-server\nsudo systemctl status grafana-server', 'language': 'bash'},
            {'title': 'Access Grafana', 'description': 'Login to Grafana web UI.', 'code': '# Open browser:\nhttp://your_server:3000\n\n# Default credentials:\nUsername: admin\nPassword: admin\n\n# Change password on first login', 'language': 'text'}
        ],
        'postInstallation': {'title': 'Setup Datasources', 'content': 'Add Prometheus as a data source. Import community dashboards. Create custom dashboards for your needs.'}
    },
    {
        'title': 'Install Redis Cache Server',
        'description': 'Deploy Redis in-memory data store for caching and messaging.',
        'category': 'installation',
        'os': ['ubuntu', 'linux'],
        'difficulty': 'beginner',
        'tags': ['redis', 'cache', 'database', 'nosql'],
        'steps': [
            {'title': 'Install Redis', 'description': 'Install from Ubuntu repository.', 'code': 'sudo apt update\nsudo apt install redis-server -y', 'language': 'bash'},
            {'title': 'Configure Redis', 'description': 'Edit Redis configuration.', 'code': 'sudo nano /etc/redis/redis.conf\n\n# Change supervised to systemd:\nsupervised systemd\n\n# Optionally bind to specific IP:\nbind 127.0.0.1 ::1\n\n# Set password:\nrequirepass YourStrongPassword', 'language': 'bash'},
            {'title': 'Restart Redis', 'description': 'Apply configuration changes.', 'code': 'sudo systemctl restart redis-server\nsudo systemctl enable redis-server', 'language': 'bash'},
            {'title': 'Test Redis', 'description': 'Verify Redis is working.', 'code': 'redis-cli\n127.0.0.1:6379> AUTH YourStrongPassword\n127.0.0.1:6379> ping\nPONG\n127.0.0.1:6379> set test "Hello Redis"\n127.0.0.1:6379> get test\n"Hello Redis"', 'language': 'bash'}
        ],
        'postInstallation': {'title': 'Redis Tips', 'content': 'Configure persistence with RDB or AOF. Set up Redis Sentinel for HA. Monitor with redis-cli INFO command.'}
    },
    {
        'title': 'Install Elasticsearch Stack',
        'description': 'Deploy Elasticsearch for full-text search and analytics.',
        'category': 'installation',
        'os': ['ubuntu', 'linux'],
        'difficulty': 'intermediate',
        'tags': ['elasticsearch', 'elk', 'search', 'analytics'],
        'steps': [
            {'title': 'Install Java', 'description': 'Elasticsearch requires Java.', 'code': 'sudo apt update\nsudo apt install openjdk-17-jdk -y', 'language': 'bash'},
            {'title': 'Add Elasticsearch GPG Key', 'description': 'Add official GPG key.', 'code': 'wget -qO - https://artifacts.elastic.co/GPG-KEY-elasticsearch | sudo gpg --dearmor -o /usr/share/keyrings/elasticsearch-keyring.gpg', 'language': 'bash'},
            {'title': 'Add Repository', 'description': 'Add Elasticsearch repository.', 'code': 'echo "deb [signed-by=/usr/share/keyrings/elasticsearch-keyring.gpg] https://artifacts.elastic.co/packages/8.x/apt stable main" | sudo tee /etc/apt/sources.list.d/elastic-8.x.list', 'language': 'bash'},
            {'title': 'Install Elasticsearch', 'description': 'Install Elasticsearch package.', 'code': 'sudo apt update\nsudo apt install elasticsearch -y', 'language': 'bash'},
            {'title': 'Configure Elasticsearch', 'description': 'Edit configuration file.', 'code': 'sudo nano /etc/elasticsearch/elasticsearch.yml\n\n# Basic settings:\ncluster.name: my-cluster\nnode.name: node-1\nnetwork.host: localhost\nhttp.port: 9200', 'language': 'bash'},
            {'title': 'Start Elasticsearch', 'description': 'Enable and start service.', 'code': 'sudo systemctl daemon-reload\nsudo systemctl enable elasticsearch\nsudo systemctl start elasticsearch\ncurl -X GET "localhost:9200"', 'language': 'bash'}
        ],
        'postInstallation': {'title': 'ELK Stack', 'content': 'Install Kibana for visualization. Add Logstash for log processing. Configure Filebeat for log shipping.'}
    }
]

# More Security Articles
security_articles = [
    {
        'title': 'Configure Fail2Ban for SSH Protection',
        'description': 'Protect SSH from brute force attacks using Fail2Ban.',
        'category': 'security',
        'os': ['ubuntu', 'centos', 'linux'],
        'difficulty': 'beginner',
        'tags': ['fail2ban', 'ssh', 'security', 'firewall'],
        'steps': [
            {'title': 'Install Fail2Ban', 'description': 'Install Fail2Ban package.', 'code': '# Ubuntu/Debian\nsudo apt update\nsudo apt install fail2ban -y\n\n# CentOS\nsudo dnf install epel-release -y\nsudo dnf install fail2ban -y', 'language': 'bash'},
            {'title': 'Create Local Config', 'description': 'Create local configuration file.', 'code': 'sudo cp /etc/fail2ban/jail.conf /etc/fail2ban/jail.local\nsudo nano /etc/fail2ban/jail.local', 'language': 'bash'},
            {'title': 'Configure SSH Jail', 'description': 'Set up SSH protection rules.', 'code': '# In jail.local, add or modify:\n[sshd]\nenabled = true\nport = ssh\nfilter = sshd\nlogpath = /var/log/auth.log\nmaxretry = 3\nbantime = 3600\nfindtime = 600', 'language': 'bash'},
            {'title': 'Start Fail2Ban', 'description': 'Enable and start service.', 'code': 'sudo systemctl enable fail2ban\nsudo systemctl start fail2ban\nsudo systemctl status fail2ban', 'language': 'bash'},
            {'title': 'Check Status', 'description': 'View banned IPs and status.', 'code': 'sudo fail2ban-client status\nsudo fail2ban-client status sshd\nsudo fail2ban-client get sshd banip', 'language': 'bash'}
        ],
        'postInstallation': {'title': 'Fail2Ban Commands', 'content': 'Unban IP: sudo fail2ban-client set sshd unbanip IP_ADDRESS. Check logs: tail -f /var/log/fail2ban.log'}
    },
    {
        'title': 'Set Up Two-Factor Authentication for SSH',
        'description': 'Add 2FA to SSH login using Google Authenticator.',
        'category': 'security',
        'os': ['ubuntu', 'linux'],
        'difficulty': 'intermediate',
        'tags': ['2fa', 'ssh', 'security', 'authentication'],
        'steps': [
            {'title': 'Install Google Authenticator', 'description': 'Install PAM module.', 'code': 'sudo apt update\nsudo apt install libpam-google-authenticator -y', 'language': 'bash'},
            {'title': 'Configure Authenticator', 'description': 'Set up for your user.', 'code': 'google-authenticator\n\n# Answer questions:\n# Time-based tokens: y\n# Update .google_authenticator: y\n# Disallow multiple uses: y\n# Increase time skew window: n\n# Enable rate-limiting: y', 'language': 'bash'},
            {'title': 'Configure PAM', 'description': 'Edit PAM SSH configuration.', 'code': 'sudo nano /etc/pam.d/sshd\n\n# Add at the end:\nauth required pam_google_authenticator.so', 'language': 'bash'},
            {'title': 'Configure SSHD', 'description': 'Enable challenge-response.', 'code': 'sudo nano /etc/ssh/sshd_config\n\n# Set these options:\nChallengeResponseAuthentication yes\nUsePAM yes\n\n# For key + 2FA:\nAuthenticationMethods publickey,keyboard-interactive', 'language': 'bash'},
            {'title': 'Restart SSH', 'description': 'Apply changes.', 'code': 'sudo systemctl restart sshd', 'language': 'bash'}
        ],
        'postInstallation': {'title': 'Setup Complete', 'content': 'Scan QR code with Google Authenticator app on your phone. Save backup codes securely. Test in new terminal before closing current session.'}
    },
    {
        'title': 'Configure UFW Firewall Rules',
        'description': 'Set up Uncomplicated Firewall for server protection.',
        'category': 'security',
        'os': ['ubuntu', 'linux'],
        'difficulty': 'beginner',
        'tags': ['ufw', 'firewall', 'security', 'networking'],
        'steps': [
            {'title': 'Install UFW', 'description': 'Install UFW if not present.', 'code': 'sudo apt update\nsudo apt install ufw -y', 'language': 'bash'},
            {'title': 'Set Default Policies', 'description': 'Configure default rules.', 'code': 'sudo ufw default deny incoming\nsudo ufw default allow outgoing', 'language': 'bash'},
            {'title': 'Allow SSH', 'description': 'Allow SSH before enabling.', 'code': 'sudo ufw allow ssh\n# Or specific port:\nsudo ufw allow 22/tcp', 'language': 'bash'},
            {'title': 'Allow Web Traffic', 'description': 'Allow HTTP and HTTPS.', 'code': 'sudo ufw allow http\nsudo ufw allow https\n# Or:\nsudo ufw allow 80/tcp\nsudo ufw allow 443/tcp', 'language': 'bash'},
            {'title': 'Enable UFW', 'description': 'Activate the firewall.', 'code': 'sudo ufw enable\nsudo ufw status verbose', 'language': 'bash'},
            {'title': 'Advanced Rules', 'description': 'More specific rules.', 'code': '# Allow from specific IP:\nsudo ufw allow from 192.168.1.100\n\n# Allow port range:\nsudo ufw allow 6000:6007/tcp\n\n# Allow specific subnet:\nsudo ufw allow from 192.168.1.0/24 to any port 3306', 'language': 'bash'}
        ],
        'postInstallation': {'title': 'UFW Commands', 'content': 'Delete rule: sudo ufw delete allow 80. Disable: sudo ufw disable. Reset: sudo ufw reset.'}
    },
    {
        'title': 'SSL Certificate with Lets Encrypt',
        'description': 'Get free SSL certificates using Certbot and Lets Encrypt.',
        'category': 'security',
        'os': ['ubuntu', 'linux'],
        'difficulty': 'beginner',
        'tags': ['ssl', 'letsencrypt', 'certbot', 'https'],
        'steps': [
            {'title': 'Install Certbot', 'description': 'Install Certbot package.', 'code': 'sudo apt update\nsudo apt install certbot -y\n\n# For Nginx:\nsudo apt install python3-certbot-nginx -y\n\n# For Apache:\nsudo apt install python3-certbot-apache -y', 'language': 'bash'},
            {'title': 'Obtain Certificate (Nginx)', 'description': 'Get certificate for Nginx.', 'code': 'sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com', 'language': 'bash'},
            {'title': 'Obtain Certificate (Apache)', 'description': 'Get certificate for Apache.', 'code': 'sudo certbot --apache -d yourdomain.com -d www.yourdomain.com', 'language': 'bash'},
            {'title': 'Standalone Mode', 'description': 'Get certificate without web server.', 'code': 'sudo certbot certonly --standalone -d yourdomain.com', 'language': 'bash'},
            {'title': 'Test Auto-Renewal', 'description': 'Verify renewal works.', 'code': 'sudo certbot renew --dry-run', 'language': 'bash'},
            {'title': 'Check Certificate', 'description': 'View certificate details.', 'code': 'sudo certbot certificates', 'language': 'bash'}
        ],
        'postInstallation': {'title': 'Auto Renewal', 'content': 'Certbot adds auto-renewal cron job automatically. Certificates renew 30 days before expiry. Check /etc/cron.d/certbot.'}
    },
    {
        'title': 'Secure Nginx Configuration',
        'description': 'Harden Nginx web server with security best practices.',
        'category': 'security',
        'os': ['ubuntu', 'linux'],
        'difficulty': 'intermediate',
        'tags': ['nginx', 'security', 'hardening', 'webserver'],
        'steps': [
            {'title': 'Hide Nginx Version', 'description': 'Disable version disclosure.', 'code': '# In nginx.conf http block:\nserver_tokens off;', 'language': 'nginx'},
            {'title': 'Security Headers', 'description': 'Add security headers.', 'code': '# In server block:\nadd_header X-Frame-Options "SAMEORIGIN" always;\nadd_header X-Content-Type-Options "nosniff" always;\nadd_header X-XSS-Protection "1; mode=block" always;\nadd_header Referrer-Policy "strict-origin-when-cross-origin" always;\nadd_header Content-Security-Policy "default-src \'self\'" always;', 'language': 'nginx'},
            {'title': 'SSL Configuration', 'description': 'Configure strong SSL settings.', 'code': '# SSL settings:\nssl_protocols TLSv1.2 TLSv1.3;\nssl_prefer_server_ciphers on;\nssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256;\nssl_session_timeout 1d;\nssl_session_cache shared:SSL:50m;\nssl_stapling on;\nssl_stapling_verify on;', 'language': 'nginx'},
            {'title': 'Rate Limiting', 'description': 'Add rate limiting.', 'code': '# In http block:\nlimit_req_zone $binary_remote_addr zone=one:10m rate=10r/s;\n\n# In server/location:\nlimit_req zone=one burst=20 nodelay;', 'language': 'nginx'},
            {'title': 'Test and Reload', 'description': 'Verify and apply config.', 'code': 'sudo nginx -t\nsudo systemctl reload nginx', 'language': 'bash'}
        ],
        'postInstallation': {'title': 'Testing', 'content': 'Test with SSL Labs: ssllabs.com/ssltest. Check headers with securityheaders.com. Regular security audits recommended.'}
    },
    {
        'title': 'Configure CSF Firewall',
        'description': 'Install and configure ConfigServer Security & Firewall.',
        'category': 'security',
        'os': ['centos', 'ubuntu', 'linux'],
        'difficulty': 'intermediate',
        'tags': ['csf', 'firewall', 'security', 'iptables'],
        'steps': [
            {'title': 'Download CSF', 'description': 'Download latest CSF package.', 'code': 'cd /usr/src\nwget https://download.configserver.com/csf.tgz\ntar -xzf csf.tgz\ncd csf', 'language': 'bash'},
            {'title': 'Install CSF', 'description': 'Run installation script.', 'code': 'sh install.sh', 'language': 'bash'},
            {'title': 'Test iptables', 'description': 'Check iptables modules.', 'code': 'perl /usr/local/csf/bin/csftest.pl', 'language': 'bash'},
            {'title': 'Configure CSF', 'description': 'Edit CSF configuration.', 'code': 'nano /etc/csf/csf.conf\n\n# Key settings:\nTESTING = "0"  # Set to 0 to enable\nRESTRICT_SYSLOG = "3"\nSYSLOG_CHECK = "3600"\nTCP_IN = "20,21,22,25,53,80,110,143,443,465,587,993,995"\nTCP_OUT = "1:65535"\nUDP_IN = "20,21,53"\nUDP_OUT = "1:65535"', 'language': 'bash'},
            {'title': 'Start CSF', 'description': 'Restart CSF service.', 'code': 'csf -r\ncsf -e', 'language': 'bash'},
            {'title': 'Common Commands', 'description': 'Useful CSF commands.', 'code': '# Allow IP:\ncsf -a 192.168.1.100\n\n# Deny IP:\ncsf -d 192.168.1.100\n\n# Remove from deny:\ncsf -dr 192.168.1.100\n\n# Check status:\ncsf -l', 'language': 'bash'}
        ],
        'postInstallation': {'title': 'CSF Features', 'content': 'Enable Login Failure Daemon (LFD) for brute force protection. Configure alerts in csf.conf. Integrate with cPanel/WHM if applicable.'}
    }
]

# More Database Articles
database_articles = [
    {
        'title': 'MySQL Performance Tuning Guide',
        'description': 'Optimize MySQL database for better performance.',
        'category': 'database',
        'os': ['ubuntu', 'centos', 'linux'],
        'difficulty': 'advanced',
        'tags': ['mysql', 'performance', 'tuning', 'optimization'],
        'steps': [
            {'title': 'Check Current Status', 'description': 'View MySQL status variables.', 'code': 'mysql -u root -p\nSHOW GLOBAL STATUS;\nSHOW GLOBAL VARIABLES;', 'language': 'sql'},
            {'title': 'InnoDB Buffer Pool', 'description': 'Configure buffer pool size.', 'code': '# In my.cnf:\n[mysqld]\ninnodb_buffer_pool_size = 4G  # 70-80% of RAM for dedicated server\ninnodb_buffer_pool_instances = 4', 'language': 'bash'},
            {'title': 'Query Cache', 'description': 'Configure query cache (MySQL 5.7).', 'code': '# Note: Deprecated in MySQL 8.0\nquery_cache_type = 1\nquery_cache_size = 128M\nquery_cache_limit = 2M', 'language': 'bash'},
            {'title': 'Connection Settings', 'description': 'Optimize connections.', 'code': 'max_connections = 500\nwait_timeout = 600\ninteractive_timeout = 600\nthread_cache_size = 50', 'language': 'bash'},
            {'title': 'Logging', 'description': 'Enable slow query log.', 'code': 'slow_query_log = 1\nslow_query_log_file = /var/log/mysql/slow.log\nlong_query_time = 2\nlog_queries_not_using_indexes = 1', 'language': 'bash'},
            {'title': 'Apply Changes', 'description': 'Restart MySQL.', 'code': 'sudo systemctl restart mysql\n# Or dynamically:\nmysql> SET GLOBAL innodb_buffer_pool_size = 4294967296;', 'language': 'bash'}
        ],
        'postInstallation': {'title': 'Monitoring', 'content': 'Use MySQLTuner script for recommendations. Monitor with SHOW ENGINE INNODB STATUS. Regular ANALYZE TABLE for statistics.'}
    },
    {
        'title': 'PostgreSQL Backup and Recovery',
        'description': 'Implement backup strategies for PostgreSQL databases.',
        'category': 'database',
        'os': ['ubuntu', 'linux'],
        'difficulty': 'intermediate',
        'tags': ['postgresql', 'backup', 'recovery', 'database'],
        'steps': [
            {'title': 'pg_dump Single Database', 'description': 'Backup single database.', 'code': '# SQL format:\npg_dump -U postgres dbname > backup.sql\n\n# Custom format (recommended):\npg_dump -U postgres -Fc dbname > backup.dump\n\n# Compressed:\npg_dump -U postgres dbname | gzip > backup.sql.gz', 'language': 'bash'},
            {'title': 'pg_dumpall All Databases', 'description': 'Backup all databases.', 'code': 'pg_dumpall -U postgres > all_databases.sql', 'language': 'bash'},
            {'title': 'Restore Database', 'description': 'Restore from backup.', 'code': '# From SQL:\npsql -U postgres dbname < backup.sql\n\n# From custom format:\npg_restore -U postgres -d dbname backup.dump\n\n# Create database and restore:\ncreatedb -U postgres newdb\npg_restore -U postgres -d newdb backup.dump', 'language': 'bash'},
            {'title': 'Automated Backup Script', 'description': 'Create backup script.', 'code': '#!/bin/bash\nDATE=$(date +%Y%m%d_%H%M%S)\nBACKUP_DIR="/var/backups/postgresql"\nDBNAME="mydb"\n\nmkdir -p $BACKUP_DIR\npg_dump -U postgres -Fc $DBNAME > $BACKUP_DIR/${DBNAME}_${DATE}.dump\n\n# Keep last 7 days\nfind $BACKUP_DIR -name "*.dump" -mtime +7 -delete', 'language': 'bash'},
            {'title': 'Schedule with Cron', 'description': 'Add to crontab.', 'code': '# Daily backup at 2 AM:\n0 2 * * * /usr/local/bin/pg_backup.sh', 'language': 'bash'}
        ],
        'postInstallation': {'title': 'Best Practices', 'content': 'Test restores regularly. Store backups offsite. Use pg_basebackup for physical backups. Consider WAL archiving for point-in-time recovery.'}
    },
    {
        'title': 'MongoDB Replica Set Configuration',
        'description': 'Set up MongoDB replica set for high availability.',
        'category': 'database',
        'os': ['ubuntu', 'linux'],
        'difficulty': 'advanced',
        'tags': ['mongodb', 'replication', 'cluster', 'nosql'],
        'steps': [
            {'title': 'Configure Hosts', 'description': 'Edit hosts file on all nodes.', 'code': '# /etc/hosts on all servers:\n192.168.1.101 mongo1\n192.168.1.102 mongo2\n192.168.1.103 mongo3', 'language': 'bash'},
            {'title': 'Enable Replication', 'description': 'Edit MongoDB config on all nodes.', 'code': '# /etc/mongod.conf:\nreplication:\n  replSetName: "rs0"\n\nnet:\n  bindIp: 0.0.0.0\n  port: 27017', 'language': 'yaml'},
            {'title': 'Restart MongoDB', 'description': 'Restart on all nodes.', 'code': 'sudo systemctl restart mongod', 'language': 'bash'},
            {'title': 'Initialize Replica Set', 'description': 'Initialize from primary.', 'code': 'mongosh\n\nrs.initiate({\n  _id: "rs0",\n  members: [\n    { _id: 0, host: "mongo1:27017" },\n    { _id: 1, host: "mongo2:27017" },\n    { _id: 2, host: "mongo3:27017" }\n  ]\n})', 'language': 'javascript'},
            {'title': 'Check Status', 'description': 'Verify replica set status.', 'code': 'rs.status()\nrs.conf()', 'language': 'javascript'}
        ],
        'postInstallation': {'title': 'Connection String', 'content': 'Connect with: mongodb://mongo1:27017,mongo2:27017,mongo3:27017/?replicaSet=rs0. Use read preferences for load distribution.'}
    }
]

# More Web Server Articles  
webserver_articles = [
    {
        'title': 'Nginx Load Balancer Configuration',
        'description': 'Set up Nginx as a load balancer for web applications.',
        'category': 'web-server',
        'os': ['ubuntu', 'linux'],
        'difficulty': 'intermediate',
        'tags': ['nginx', 'loadbalancer', 'haproxy', 'webserver'],
        'steps': [
            {'title': 'Define Upstream', 'description': 'Configure backend servers.', 'code': '# /etc/nginx/nginx.conf or sites-available:\nupstream backend {\n    least_conn;  # Load balancing method\n    server 192.168.1.101:80 weight=3;\n    server 192.168.1.102:80;\n    server 192.168.1.103:80 backup;\n}', 'language': 'nginx'},
            {'title': 'Configure Server Block', 'description': 'Set up proxy pass.', 'code': 'server {\n    listen 80;\n    server_name example.com;\n\n    location / {\n        proxy_pass http://backend;\n        proxy_set_header Host $host;\n        proxy_set_header X-Real-IP $remote_addr;\n        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;\n        proxy_set_header X-Forwarded-Proto $scheme;\n    }\n}', 'language': 'nginx'},
            {'title': 'Health Checks', 'description': 'Add health check configuration.', 'code': 'upstream backend {\n    least_conn;\n    server 192.168.1.101:80 max_fails=3 fail_timeout=30s;\n    server 192.168.1.102:80 max_fails=3 fail_timeout=30s;\n}', 'language': 'nginx'},
            {'title': 'Session Persistence', 'description': 'Enable sticky sessions.', 'code': 'upstream backend {\n    ip_hash;  # Sticky sessions based on client IP\n    server 192.168.1.101:80;\n    server 192.168.1.102:80;\n}', 'language': 'nginx'},
            {'title': 'Test and Reload', 'description': 'Apply configuration.', 'code': 'sudo nginx -t\nsudo systemctl reload nginx', 'language': 'bash'}
        ],
        'postInstallation': {'title': 'Load Balancing Methods', 'content': 'round-robin (default), least_conn, ip_hash, hash, random. Monitor with nginx stub_status module.'}
    },
    {
        'title': 'Apache Virtual Hosts Configuration',
        'description': 'Set up multiple websites on Apache with virtual hosts.',
        'category': 'web-server',
        'os': ['ubuntu', 'linux'],
        'difficulty': 'beginner',
        'tags': ['apache', 'virtualhost', 'webserver', 'hosting'],
        'steps': [
            {'title': 'Create Directory Structure', 'description': 'Create website directories.', 'code': 'sudo mkdir -p /var/www/site1.com/public_html\nsudo mkdir -p /var/www/site2.com/public_html\nsudo chown -R $USER:$USER /var/www/site1.com\nsudo chown -R $USER:$USER /var/www/site2.com', 'language': 'bash'},
            {'title': 'Create Virtual Host File', 'description': 'Configure first virtual host.', 'code': 'sudo nano /etc/apache2/sites-available/site1.com.conf\n\n<VirtualHost *:80>\n    ServerAdmin admin@site1.com\n    ServerName site1.com\n    ServerAlias www.site1.com\n    DocumentRoot /var/www/site1.com/public_html\n    ErrorLog ${APACHE_LOG_DIR}/site1_error.log\n    CustomLog ${APACHE_LOG_DIR}/site1_access.log combined\n</VirtualHost>', 'language': 'apache'},
            {'title': 'Enable Virtual Hosts', 'description': 'Enable sites.', 'code': 'sudo a2ensite site1.com.conf\nsudo a2ensite site2.com.conf\nsudo a2dissite 000-default.conf', 'language': 'bash'},
            {'title': 'Test and Restart', 'description': 'Apply changes.', 'code': 'sudo apache2ctl configtest\nsudo systemctl restart apache2', 'language': 'bash'}
        ],
        'postInstallation': {'title': 'Next Steps', 'content': 'Add SSL with Certbot. Configure .htaccess for URL rewriting. Enable mod_rewrite: sudo a2enmod rewrite.'}
    },
    {
        'title': 'Configure Nginx Reverse Proxy',
        'description': 'Set up Nginx as a reverse proxy for backend applications.',
        'category': 'web-server',
        'os': ['ubuntu', 'linux'],
        'difficulty': 'intermediate',
        'tags': ['nginx', 'reverseproxy', 'proxy', 'webserver'],
        'steps': [
            {'title': 'Basic Reverse Proxy', 'description': 'Simple proxy configuration.', 'code': 'server {\n    listen 80;\n    server_name app.example.com;\n\n    location / {\n        proxy_pass http://localhost:3000;\n        proxy_http_version 1.1;\n        proxy_set_header Upgrade $http_upgrade;\n        proxy_set_header Connection \'upgrade\';\n        proxy_set_header Host $host;\n        proxy_cache_bypass $http_upgrade;\n    }\n}', 'language': 'nginx'},
            {'title': 'WebSocket Support', 'description': 'Enable WebSocket proxying.', 'code': 'location /socket.io/ {\n    proxy_pass http://localhost:3000;\n    proxy_http_version 1.1;\n    proxy_set_header Upgrade $http_upgrade;\n    proxy_set_header Connection "upgrade";\n    proxy_set_header Host $host;\n    proxy_set_header X-Real-IP $remote_addr;\n}', 'language': 'nginx'},
            {'title': 'Proxy Headers', 'description': 'Pass important headers.', 'code': 'location / {\n    proxy_pass http://backend;\n    proxy_set_header Host $host;\n    proxy_set_header X-Real-IP $remote_addr;\n    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;\n    proxy_set_header X-Forwarded-Proto $scheme;\n    proxy_set_header X-Forwarded-Host $host;\n    proxy_set_header X-Forwarded-Port $server_port;\n}', 'language': 'nginx'},
            {'title': 'Buffering Settings', 'description': 'Configure proxy buffers.', 'code': 'location / {\n    proxy_pass http://backend;\n    proxy_buffering on;\n    proxy_buffer_size 4k;\n    proxy_buffers 8 4k;\n    proxy_busy_buffers_size 8k;\n    proxy_connect_timeout 60s;\n    proxy_send_timeout 60s;\n    proxy_read_timeout 60s;\n}', 'language': 'nginx'}
        ],
        'postInstallation': {'title': 'Testing', 'content': 'Check proxy is working with curl. Monitor proxy logs for errors. Use nginx -t before reloading configuration.'}
    }
]

# More Learning Articles
learning_articles = [
    {
        'title': 'Excel VLOOKUP Function Guide',
        'description': 'Master the VLOOKUP function in Microsoft Excel.',
        'category': 'learning',
        'os': ['windows'],
        'difficulty': 'beginner',
        'tags': ['excel', 'vlookup', 'formulas', 'microsoft'],
        'steps': [
            {'title': 'VLOOKUP Syntax', 'description': 'Understand the function structure.', 'code': '=VLOOKUP(lookup_value, table_array, col_index_num, [range_lookup])\n\n# Parameters:\n# lookup_value: The value to search for\n# table_array: The range containing data\n# col_index_num: Column number to return\n# range_lookup: TRUE (approximate) or FALSE (exact)', 'language': 'text'},
            {'title': 'Basic Example', 'description': 'Simple VLOOKUP usage.', 'code': '# Data in A1:C10 (ID, Name, Price)\n# Find price for ID "A001":\n\n=VLOOKUP("A001", A1:C10, 3, FALSE)\n\n# Returns the price from column 3 for ID A001', 'language': 'text'},
            {'title': 'With Cell Reference', 'description': 'Use cell reference for lookup.', 'code': '# If E1 contains the ID to search:\n=VLOOKUP(E1, A1:C10, 3, FALSE)\n\n# Now change E1 to search different IDs', 'language': 'text'},
            {'title': 'Approximate Match', 'description': 'Use for ranges/grades.', 'code': '# Grade table in A1:B5:\n# 0   F\n# 60  D\n# 70  C\n# 80  B\n# 90  A\n\n# Find grade for score 85:\n=VLOOKUP(85, A1:B5, 2, TRUE)\n# Returns "B" (closest match <= 85)', 'language': 'text'},
            {'title': 'Error Handling', 'description': 'Handle #N/A errors.', 'code': '# Wrap with IFERROR:\n=IFERROR(VLOOKUP(E1, A1:C10, 3, FALSE), "Not Found")\n\n# Or use IFNA (Excel 2013+):\n=IFNA(VLOOKUP(E1, A1:C10, 3, FALSE), "Not Found")', 'language': 'text'}
        ],
        'postInstallation': {'title': 'Tips', 'content': 'VLOOKUP only searches leftmost column. Consider INDEX/MATCH for more flexibility. Use absolute references ($A$1:$C$10) when copying formulas.'}
    },
    {
        'title': 'Excel Pivot Tables Tutorial',
        'description': 'Create and customize Pivot Tables for data analysis.',
        'category': 'learning',
        'os': ['windows'],
        'difficulty': 'intermediate',
        'tags': ['excel', 'pivottable', 'analysis', 'microsoft'],
        'steps': [
            {'title': 'Create Pivot Table', 'description': 'Steps to create pivot table.', 'code': '1. Select your data range\n2. Go to Insert > PivotTable\n3. Choose where to place it\n4. Click OK\n\n# Keyboard shortcut: Alt + N + V', 'language': 'text'},
            {'title': 'Add Fields', 'description': 'Configure pivot table fields.', 'code': '# Drag fields to areas:\n\n# Rows: Categories to group by (e.g., Region, Product)\n# Columns: Secondary grouping (e.g., Year, Quarter)\n# Values: Numbers to calculate (Sum, Count, Average)\n# Filters: Criteria to filter data', 'language': 'text'},
            {'title': 'Change Calculations', 'description': 'Modify value calculations.', 'code': '# Click on value field > Value Field Settings\n\n# Available calculations:\n- Sum (default for numbers)\n- Count (default for text)\n- Average\n- Max / Min\n- Product\n- Count Numbers\n- StdDev / Var', 'language': 'text'},
            {'title': 'Group Data', 'description': 'Group dates or numbers.', 'code': '# Right-click on row/column > Group\n\n# For Dates:\n- Days, Months, Quarters, Years\n\n# For Numbers:\n- Starting at: 0\n- Ending at: 100\n- By: 10 (creates ranges 0-10, 10-20, etc.)', 'language': 'text'},
            {'title': 'Refresh Data', 'description': 'Update pivot table.', 'code': '# Manual refresh:\n- Right-click > Refresh\n- Keyboard: Alt + F5\n\n# Refresh all pivot tables:\n- Data > Refresh All\n- Keyboard: Ctrl + Alt + F5', 'language': 'text'}
        ],
        'postInstallation': {'title': 'Advanced Features', 'content': 'Use Slicers for visual filtering. Create Pivot Charts for visualization. Enable calculated fields for custom formulas.'}
    },
    {
        'title': 'Tally GST Invoice Creation',
        'description': 'Create GST-compliant invoices in Tally Prime.',
        'category': 'learning',
        'os': ['windows'],
        'difficulty': 'beginner',
        'tags': ['tally', 'gst', 'invoice', 'accounting'],
        'steps': [
            {'title': 'Enable GST', 'description': 'Configure GST in company.', 'code': 'Gateway of Tally > F11 (Features)\n> Enable Goods and Services Tax (GST): Yes\n> Set/alter GST details: Yes\n\n# Enter:\n- State\n- GSTIN/UIN\n- Registration Type', 'language': 'text'},
            {'title': 'Create GST Ledgers', 'description': 'Set up tax ledgers.', 'code': 'Gateway > Create > Ledger\n\n# CGST:\nName: CGST\nUnder: Duties & Taxes\nType of Duty: GST\nTax Type: Central Tax\n\n# SGST:\nName: SGST  \nUnder: Duties & Taxes\nType of Duty: GST\nTax Type: State Tax\n\n# IGST:\nName: IGST\nUnder: Duties & Taxes\nType of Duty: GST\nTax Type: Integrated Tax', 'language': 'text'},
            {'title': 'Create Stock Item with GST', 'description': 'Add GST to products.', 'code': 'Gateway > Create > Stock Item\n\nName: Product A\nUnder: Primary\nUnits: Nos\nGST Applicable: Applicable\nSet/alter GST Details: Yes\n  - Description: Product A\n  - HSN/SAC: 1234\n  - Taxability: Taxable\n  - GST Rate: 18%', 'language': 'text'},
            {'title': 'Create Sales Voucher', 'description': 'Create GST invoice.', 'code': 'Gateway > Vouchers > F8 (Sales)\n\n# Press F2 to change date\n# Enter:\n- Party A/c name\n- Sales ledger\n- Stock items with quantity and rate\n\n# GST will auto-calculate based on:\n- Party state (CGST+SGST or IGST)\n- Item GST rate', 'language': 'text'},
            {'title': 'Print Invoice', 'description': 'Print GST invoice.', 'code': '# After saving voucher:\nPress P to Print\n\n# Or from Daybook:\nGateway > Display > Daybook\nSelect voucher > Alt+P (Print)', 'language': 'text'}
        ],
        'postInstallation': {'title': 'GST Reports', 'content': 'View GSTR-1 report: Gateway > Display > GST Reports > GSTR-1. Export to Excel or upload to GST portal.'}
    },
    {
        'title': 'Photoshop Layer Masking',
        'description': 'Master layer masks for non-destructive editing in Photoshop.',
        'category': 'learning',
        'os': ['windows'],
        'difficulty': 'intermediate',
        'tags': ['photoshop', 'layers', 'masking', 'adobe'],
        'steps': [
            {'title': 'Add Layer Mask', 'description': 'Create a layer mask.', 'code': '# Method 1: Button\n- Select layer\n- Click "Add Layer Mask" button (bottom of Layers panel)\n\n# Method 2: Menu\n- Layer > Layer Mask > Reveal All\n\n# Keyboard:\n- Alt + Click mask button = Hide All (black mask)', 'language': 'text'},
            {'title': 'Paint on Mask', 'description': 'Edit mask with brushes.', 'code': '# Click mask thumbnail to select\n\n# Brush colors:\n- Black = Hide (transparent)\n- White = Show (visible)\n- Gray = Semi-transparent\n\n# Press X to swap foreground/background\n# Press D for default black/white', 'language': 'text'},
            {'title': 'Selection to Mask', 'description': 'Create mask from selection.', 'code': '# Make selection first (Lasso, Magic Wand, etc.)\n# Then add layer mask\n# Selection becomes white, rest is black\n\n# Refine mask:\n- Select mask\n- Select > Select and Mask\n- Adjust edge detection', 'language': 'text'},
            {'title': 'Gradient Mask', 'description': 'Create smooth transitions.', 'code': '# Select mask\n# Choose Gradient Tool (G)\n# Set black to white gradient\n# Draw gradient on mask\n\n# Result: Smooth fade from visible to hidden', 'language': 'text'},
            {'title': 'Mask Shortcuts', 'description': 'Useful keyboard shortcuts.', 'code': '# View mask:\n- Alt + Click mask = View mask only\n- Shift + Click mask = Disable mask\n- Ctrl + Click mask = Load as selection\n\n# Invert mask:\n- Select mask\n- Ctrl + I (Invert)', 'language': 'text'}
        ],
        'postInstallation': {'title': 'Pro Tips', 'content': 'Use Brush hardness 0% for soft edges. Apply adjustment layers with masks. Link/unlink layer and mask as needed.'}
    },
    {
        'title': 'Word Mail Merge Tutorial',
        'description': 'Create personalized documents using Mail Merge in Word.',
        'category': 'learning',
        'os': ['windows'],
        'difficulty': 'beginner',
        'tags': ['word', 'mailmerge', 'microsoft', 'documents'],
        'steps': [
            {'title': 'Prepare Data Source', 'description': 'Create recipient list.', 'code': '# Excel file with columns:\n# Name | Email | Address | City | Amount\n\n# Or use:\n- Word table\n- Outlook contacts\n- Access database', 'language': 'text'},
            {'title': 'Start Mail Merge', 'description': 'Begin merge wizard.', 'code': '# Mailings tab > Start Mail Merge\n\n# Choose document type:\n- Letters\n- Email Messages\n- Envelopes\n- Labels\n- Directory', 'language': 'text'},
            {'title': 'Select Recipients', 'description': 'Connect to data source.', 'code': '# Mailings > Select Recipients\n\n# Options:\n- Type New List (create in Word)\n- Use Existing List (Excel, etc.)\n- Choose from Outlook Contacts\n\n# Browse to your Excel file\n# Select sheet containing data', 'language': 'text'},
            {'title': 'Insert Merge Fields', 'description': 'Add placeholders.', 'code': '# Position cursor where field should appear\n# Mailings > Insert Merge Field\n# Select field (Name, Email, etc.)\n\n# Example letter:\nDear <<Name>>,\n\nYour balance is <<Amount>>.\n\n# Address block:\nMailings > Address Block', 'language': 'text'},
            {'title': 'Preview and Finish', 'description': 'Complete the merge.', 'code': '# Preview Results:\n- Mailings > Preview Results\n- Use arrows to navigate records\n\n# Finish Merge:\n- Mailings > Finish & Merge\n- Edit Individual Documents\n- Print Documents\n- Send Email Messages', 'language': 'text'}
        ],
        'postInstallation': {'title': 'Tips', 'content': 'Filter recipients before merge. Use IF fields for conditional content. Save main document for future merges.'}
    }
]

# More CCTV Articles
cctv_articles = [
    {
        'title': 'Hikvision DVR Initial Setup',
        'description': 'Configure Hikvision DVR for first-time use.',
        'category': 'cctv-cameras',
        'os': ['linux'],
        'difficulty': 'beginner',
        'tags': ['hikvision', 'dvr', 'cctv', 'setup'],
        'steps': [
            {'title': 'Connect Hardware', 'description': 'Physical setup.', 'code': '# Connections:\n1. Connect cameras to BNC ports\n2. Connect monitor via VGA/HDMI\n3. Connect network cable (optional)\n4. Connect mouse to USB\n5. Power on DVR', 'language': 'text'},
            {'title': 'Initial Wizard', 'description': 'Complete setup wizard.', 'code': '# On first boot:\n1. Select language\n2. Set admin password (8-16 characters)\n3. Set unlock pattern (optional)\n4. Configure date/time\n5. Set timezone', 'language': 'text'},
            {'title': 'Configure HDD', 'description': 'Initialize hard drive.', 'code': '# Menu > HDD > General\n\n# If HDD shows "Uninitialized":\n1. Select the HDD\n2. Click "Init"\n3. Wait for initialization\n4. Status should show "Normal"', 'language': 'text'},
            {'title': 'Network Settings', 'description': 'Configure IP address.', 'code': '# Menu > Configuration > Network > General\n\n# DHCP or Static:\nIPv4 Address: 192.168.1.64\nSubnet Mask: 255.255.255.0\nGateway: 192.168.1.1\nDNS: 8.8.8.8', 'language': 'text'},
            {'title': 'Camera Settings', 'description': 'Configure recording.', 'code': '# Menu > Configuration > Record\n\n# For each camera:\n- Enable recording\n- Set resolution (1080P, 720P)\n- Set frame rate (25fps)\n- Set bitrate type (Variable)\n- Set video quality (Medium/High)', 'language': 'text'}
        ],
        'postInstallation': {'title': 'Remote Access', 'content': 'Enable Hik-Connect for remote viewing. Download iVMS-4500 app for mobile access. Port forward 8000 and 554 for external access.'}
    },
    {
        'title': 'Dahua NVR Network Configuration',
        'description': 'Set up Dahua NVR for IP camera recording.',
        'category': 'cctv-cameras',
        'os': ['linux'],
        'difficulty': 'intermediate',
        'tags': ['dahua', 'nvr', 'cctv', 'ipcamera'],
        'steps': [
            {'title': 'Access NVR Menu', 'description': 'Login to NVR.', 'code': '# Right-click > Main Menu\n# Default credentials:\nUsername: admin\nPassword: admin (or set during wizard)\n\n# Change password immediately!', 'language': 'text'},
            {'title': 'Network Settings', 'description': 'Configure NVR IP.', 'code': '# Main Menu > Network > TCP/IP\n\n# Settings:\nIP Address: 192.168.1.108\nSubnet Mask: 255.255.255.0\nDefault Gateway: 192.168.1.1\nPreferred DNS: 8.8.8.8', 'language': 'text'},
            {'title': 'Add IP Cameras', 'description': 'Register cameras to NVR.', 'code': '# Main Menu > Camera > Registration\n\n# Device Search:\n1. Click "Device Search"\n2. Select cameras from list\n3. Enter camera username/password\n4. Click "Add"\n\n# Manual Add:\n1. Click "Manual Add"\n2. Enter camera IP, port, protocol\n3. Enter credentials', 'language': 'text'},
            {'title': 'Configure Recording', 'description': 'Set up recording schedule.', 'code': '# Main Menu > Storage > Schedule\n\n# For each channel:\n- Select day/time blocks\n- Set recording type:\n  * Continuous (green)\n  * Motion (yellow)\n  * Alarm (red)\n- Apply to all days if needed', 'language': 'text'},
            {'title': 'Enable P2P', 'description': 'Set up cloud access.', 'code': '# Main Menu > Network > P2P\n\n# Enable P2P: Yes\n# Note the QR code and SN\n\n# Mobile App:\n1. Download gDMSS Lite (iOS/Android)\n2. Add device > Scan QR\n3. Enter device password', 'language': 'text'}
        ],
        'postInstallation': {'title': 'Optimization', 'content': 'Set motion detection sensitivity. Configure email alerts. Enable smart search features. Regular firmware updates.'}
    }
]

# More Computers Articles
computers_articles = [
    {
        'title': 'Windows Active Directory Setup',
        'description': 'Install and configure Active Directory Domain Services.',
        'category': 'computers',
        'os': ['windows'],
        'difficulty': 'advanced',
        'tags': ['windows-server', 'activedirectory', 'domain', 'ad'],
        'steps': [
            {'title': 'Prerequisites', 'description': 'Prepare server.', 'code': '# Requirements:\n- Windows Server 2016/2019/2022\n- Static IP address\n- Administrator access\n- Server name configured\n\n# Set static IP:\nControl Panel > Network > Adapter > Properties\nIPv4 > Use the following IP address', 'language': 'text'},
            {'title': 'Install AD DS Role', 'description': 'Add Active Directory role.', 'code': '# Server Manager > Add Roles and Features\n\n1. Role-based installation\n2. Select current server\n3. Select: Active Directory Domain Services\n4. Add required features\n5. Install', 'language': 'text'},
            {'title': 'Promote to DC', 'description': 'Configure domain controller.', 'code': '# After installation, click notification flag:\n"Promote this server to a domain controller"\n\n# Deployment Configuration:\n- Add a new forest\n- Root domain name: company.local\n\n# Domain Controller Options:\n- Forest/Domain functional level\n- DNS Server: checked\n- Global Catalog: checked\n- DSRM password: set strong password', 'language': 'text'},
            {'title': 'Verify Installation', 'description': 'Check AD is working.', 'code': '# After restart:\n\n# Open Active Directory Users and Computers:\nWindows + R > dsa.msc\n\n# Verify domain structure\n# Check DNS is working:\nnslookup company.local', 'language': 'powershell'},
            {'title': 'Create Users', 'description': 'Add domain users.', 'code': '# In AD Users and Computers:\n1. Expand domain > Users\n2. Right-click > New > User\n3. Enter user details\n4. Set password\n5. Configure account options', 'language': 'text'}
        ],
        'postInstallation': {'title': 'Next Steps', 'content': 'Create Organizational Units (OUs). Set up Group Policies. Join workstations to domain. Configure DNS forwarders.'}
    },
    {
        'title': 'Windows DHCP Server Configuration',
        'description': 'Set up DHCP server on Windows Server.',
        'category': 'computers',
        'os': ['windows'],
        'difficulty': 'intermediate',
        'tags': ['windows-server', 'dhcp', 'networking', 'server'],
        'steps': [
            {'title': 'Install DHCP Role', 'description': 'Add DHCP server role.', 'code': '# Server Manager > Add Roles and Features\n\n1. Select: DHCP Server\n2. Add required features\n3. Complete installation\n4. Click "Complete DHCP configuration"', 'language': 'text'},
            {'title': 'Authorize DHCP', 'description': 'Authorize in Active Directory.', 'code': '# If domain joined:\nDHCP console > Right-click server > Authorize\n\n# Or via PowerShell:\nAdd-DhcpServerInDC -DnsName "server.company.local"', 'language': 'powershell'},
            {'title': 'Create Scope', 'description': 'Configure IP address range.', 'code': '# DHCP Console > IPv4 > New Scope\n\n# Scope settings:\nName: LAN Scope\nStart IP: 192.168.1.100\nEnd IP: 192.168.1.200\nSubnet mask: 255.255.255.0\nLease duration: 8 days', 'language': 'text'},
            {'title': 'Configure Options', 'description': 'Set DHCP options.', 'code': '# During scope wizard or later:\n\n# Router (Gateway):\n003 Router: 192.168.1.1\n\n# DNS Servers:\n006 DNS Servers: 192.168.1.10, 8.8.8.8\n\n# Domain Name:\n015 DNS Domain Name: company.local', 'language': 'text'},
            {'title': 'Activate Scope', 'description': 'Enable the scope.', 'code': '# Right-click scope > Activate\n\n# Verify DHCP is working:\nGet-DhcpServerv4Scope\nGet-DhcpServerv4Lease -ScopeId 192.168.1.0', 'language': 'powershell'}
        ],
        'postInstallation': {'title': 'Advanced Features', 'content': 'Configure reservations for static devices. Set up failover with second DHCP server. Enable DHCP policies for specific clients.'}
    },
    {
        'title': 'Windows File Server Setup',
        'description': 'Configure Windows Server as a file server with shares.',
        'category': 'computers',
        'os': ['windows'],
        'difficulty': 'beginner',
        'tags': ['windows-server', 'fileserver', 'shares', 'storage'],
        'steps': [
            {'title': 'Install File Server Role', 'description': 'Add file server role.', 'code': '# Server Manager > Add Roles and Features\n\n# Select:\n- File and Storage Services\n  - File Server\n  - File Server Resource Manager (optional)', 'language': 'text'},
            {'title': 'Create Shared Folder', 'description': 'Set up network share.', 'code': '# Create folder:\nmkdir D:\\SharedData\n\n# Via Server Manager:\nFile and Storage Services > Shares > New Share\n\n# Or right-click folder:\nProperties > Sharing > Advanced Sharing\n> Share this folder', 'language': 'powershell'},
            {'title': 'Configure Permissions', 'description': 'Set share and NTFS permissions.', 'code': '# Share Permissions:\n- Everyone: Read (minimum)\n- Specific groups: Change/Full Control\n\n# NTFS Permissions (Security tab):\n- Disable inheritance\n- Remove Users\n- Add specific groups:\n  - HR: Read/Write\n  - IT: Full Control\n  - Finance: Read', 'language': 'text'},
            {'title': 'Map Network Drive', 'description': 'Connect from clients.', 'code': '# Command line:\nnet use Z: \\\\server\\SharedData /persistent:yes\n\n# PowerShell:\nNew-PSDrive -Name "Z" -PSProvider FileSystem -Root "\\\\server\\SharedData" -Persist\n\n# GUI:\nThis PC > Map network drive', 'language': 'powershell'},
            {'title': 'Enable Access-Based Enumeration', 'description': 'Hide folders user cannot access.', 'code': '# Server Manager > Shares\n# Right-click share > Properties\n# Settings > Enable access-based enumeration\n\n# PowerShell:\nSet-SmbShare -Name "SharedData" -FolderEnumerationMode AccessBased', 'language': 'powershell'}
        ],
        'postInstallation': {'title': 'Best Practices', 'content': 'Use DFS for multiple file servers. Enable shadow copies for recovery. Set up quotas to manage disk space. Regular backup of shared data.'}
    }
]

async def seed_database():
    all_articles = (
        installation_articles + 
        security_articles + 
        database_articles + 
        webserver_articles + 
        learning_articles +
        cctv_articles +
        computers_articles
    )
    
    added_count = 0
    for article in all_articles:
        existing = await db.code_snippets.find_one({'slug': create_slug(article['title'])})
        if existing:
            print(f"Skipping existing: {article['title']}")
            continue
        
        snippet = {
            'id': str(uuid.uuid4()),
            'title': article['title'],
            'slug': create_slug(article['title']),
            'description': article['description'],
            'category': article['category'],
            'os': article['os'],
            'difficulty': article['difficulty'],
            'views': 1000 + (hash(article['title']) % 9000),
            'likes': 100 + (hash(article['title']) % 400),
            'author': 'Admin',
            'createdAt': datetime.now(timezone.utc),
            'updatedAt': datetime.now(timezone.utc),
            'tags': article['tags'],
            'steps': article['steps'],
            'postInstallation': article.get('postInstallation')
        }
        
        await db.code_snippets.insert_one(snippet)
        print(f"Added: {article['title']}")
        added_count += 1
    
    total = await db.code_snippets.count_documents({})
    print(f"\n--- Summary ---")
    print(f"New articles added: {added_count}")
    print(f"Total articles in database: {total}")

if __name__ == "__main__":
    asyncio.run(seed_database())
