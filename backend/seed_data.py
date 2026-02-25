from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
from pathlib import Path
import asyncio
from datetime import datetime
import uuid

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

async def seed_database():
    # Check if data already exists
    existing = await db.code_snippets.count_documents({})
    if existing > 0:
        print(f"Database already has {existing} snippets. Skipping seed.")
        return
    
    snippets = [
        {
            'id': str(uuid.uuid4()),
            'title': 'Install cPanel on Ubuntu Server',
            'slug': 'install-cpanel-ubuntu',
            'description': 'Complete guide to install cPanel & WHM on Ubuntu Linux server with all prerequisites and post-installation steps.',
            'category': 'installation',
            'os': ['ubuntu', 'linux'],
            'difficulty': 'intermediate',
            'views': 15420,
            'likes': 342,
            'author': 'Admin',
            'createdAt': datetime.utcnow(),
            'updatedAt': datetime.utcnow(),
            'tags': ['cpanel', 'whm', 'hosting', 'web-panel'],
            'steps': [
                {
                    'title': 'Update System Packages',
                    'description': 'First, update all system packages to ensure you have the latest security patches.',
                    'code': 'apt update && apt upgrade -y\nreboot',
                    'language': 'bash'
                },
                {
                    'title': 'Set Hostname (FQDN Required)',
                    'description': 'cPanel requires a fully qualified domain name. Replace server.yourdomain.com with your actual domain.',
                    'code': 'hostnamectl set-hostname server.yourdomain.com\necho "your_server_IP server.yourdomain.com server" >> /etc/hosts\nhostname',
                    'language': 'bash'
                },
                {
                    'title': 'Install Screen (Optional but Recommended)',
                    'description': 'Screen helps maintain installation session if connection drops.',
                    'code': 'apt install screen -y\nscreen',
                    'language': 'bash'
                },
                {
                    'title': 'Download and Run cPanel Installer',
                    'description': 'This process takes 30-60 minutes. Do not interrupt the installation.',
                    'code': 'cd /home\ncurl -o latest -L https://securedownloads.cpanel.net/latest\nsh latest',
                    'language': 'bash'
                },
                {
                    'title': 'Configure Firewall Ports',
                    'description': 'Allow cPanel/WHM ports through firewall.',
                    'code': 'ufw allow 2087\nufw allow 2083\nufw allow 2082\nufw allow 2086\nufw enable\nufw status',
                    'language': 'bash'
                }
            ],
            'postInstallation': {
                'title': 'Post-Installation Steps',
                'content': 'Access WHM at https://your_server_IP:2087 using root credentials. Activate your license and create cPanel accounts.'
            }
        },
        {
            'id': str(uuid.uuid4()),
            'title': 'SSH Security Hardening Best Practices',
            'slug': 'ssh-security-hardening',
            'description': 'Secure your Linux server SSH access with key-based authentication, disable root login, and implement fail2ban protection.',
            'category': 'security',
            'os': ['ubuntu', 'centos', 'debian', 'linux'],
            'difficulty': 'intermediate',
            'views': 12850,
            'likes': 289,
            'author': 'Admin',
            'createdAt': datetime.utcnow(),
            'updatedAt': datetime.utcnow(),
            'tags': ['ssh', 'security', 'authentication', 'fail2ban'],
            'steps': [
                {
                    'title': 'Generate SSH Key Pair',
                    'description': 'Create SSH keys on your local machine (client).',
                    'code': 'ssh-keygen -t ed25519 -C "your_email@example.com"\n# Or for better compatibility:\nssh-keygen -t rsa -b 4096 -C "your_email@example.com"',
                    'language': 'bash'
                },
                {
                    'title': 'Copy Public Key to Server',
                    'description': 'Transfer your public key to the remote server.',
                    'code': 'ssh-copy-id user@server_ip',
                    'language': 'bash'
                },
                {
                    'title': 'Configure SSH Daemon',
                    'description': 'Edit SSH configuration for enhanced security.',
                    'code': 'sudo nano /etc/ssh/sshd_config\n\n# Add or modify these lines:\nPubkeyAuthentication yes\nPasswordAuthentication no\nPermitRootLogin no\nPort 2222\nAllowGroups sshgroup',
                    'language': 'bash'
                },
                {
                    'title': 'Restart SSH Service',
                    'description': 'Apply changes by restarting SSH daemon.',
                    'code': 'sudo systemctl restart sshd\nsudo systemctl status sshd',
                    'language': 'bash'
                }
            ]
        },
        {
            'id': str(uuid.uuid4()),
            'title': 'Configure UFW Firewall on Ubuntu',
            'slug': 'configure-ufw-firewall-ubuntu',
            'description': 'Step-by-step guide to set up and configure UFW (Uncomplicated Firewall) on Ubuntu Linux server.',
            'category': 'security',
            'os': ['ubuntu', 'debian'],
            'difficulty': 'beginner',
            'views': 9340,
            'likes': 178,
            'author': 'Admin',
            'createdAt': datetime.utcnow(),
            'updatedAt': datetime.utcnow(),
            'tags': ['ufw', 'firewall', 'security', 'networking'],
            'steps': [
                {
                    'title': 'Check UFW Status',
                    'description': 'Verify if UFW is installed and check its status.',
                    'code': 'sudo ufw status verbose',
                    'language': 'bash'
                },
                {
                    'title': 'Set Default Policies',
                    'description': 'Deny all incoming and allow all outgoing by default.',
                    'code': 'sudo ufw default deny incoming\nsudo ufw default allow outgoing',
                    'language': 'bash'
                },
                {
                    'title': 'Allow SSH (Important!)',
                    'description': 'Allow SSH before enabling firewall to prevent lockout.',
                    'code': 'sudo ufw allow ssh\n# Or specific port:\nsudo ufw allow 22/tcp',
                    'language': 'bash'
                },
                {
                    'title': 'Enable UFW',
                    'description': 'Activate the firewall with configured rules.',
                    'code': 'sudo ufw enable\nsudo ufw status numbered',
                    'language': 'bash'
                }
            ]
        },
        {
            'id': str(uuid.uuid4()),
            'title': 'Install NGINX Web Server',
            'slug': 'install-nginx-web-server',
            'description': 'Install and configure NGINX high-performance web server on Linux.',
            'category': 'web-server',
            'os': ['ubuntu', 'centos', 'debian'],
            'difficulty': 'beginner',
            'views': 18750,
            'likes': 425,
            'author': 'Admin',
            'createdAt': datetime.utcnow(),
            'updatedAt': datetime.utcnow(),
            'tags': ['nginx', 'web-server', 'installation'],
            'steps': [
                {
                    'title': 'Install NGINX (Ubuntu/Debian)',
                    'description': 'Install NGINX using apt package manager.',
                    'code': 'sudo apt update\nsudo apt install nginx -y',
                    'language': 'bash'
                },
                {
                    'title': 'Start and Enable NGINX',
                    'description': 'Start NGINX service and enable it to start on boot.',
                    'code': 'sudo systemctl start nginx\nsudo systemctl enable nginx\nsudo systemctl status nginx',
                    'language': 'bash'
                }
            ]
        },
        {
            'id': str(uuid.uuid4()),
            'title': 'Install MySQL Database Server',
            'slug': 'install-mysql-database',
            'description': 'Complete guide to install and secure MySQL database server on Linux.',
            'category': 'database',
            'os': ['ubuntu', 'centos', 'debian'],
            'difficulty': 'beginner',
            'views': 14230,
            'likes': 312,
            'author': 'Admin',
            'createdAt': datetime.utcnow(),
            'updatedAt': datetime.utcnow(),
            'tags': ['mysql', 'database', 'installation', 'mariadb'],
            'steps': [
                {
                    'title': 'Install MySQL (Ubuntu/Debian)',
                    'description': 'Install MySQL server using apt.',
                    'code': 'sudo apt update\nsudo apt install mysql-server -y',
                    'language': 'bash'
                },
                {
                    'title': 'Start MySQL Service',
                    'description': 'Start and enable MySQL service.',
                    'code': 'sudo systemctl start mysql\nsudo systemctl enable mysql\nsudo systemctl status mysql',
                    'language': 'bash'
                },
                {
                    'title': 'Secure MySQL Installation',
                    'description': 'Run security script to set root password and remove test databases.',
                    'code': 'sudo mysql_secure_installation',
                    'language': 'bash'
                }
            ]
        },
        {
            'id': str(uuid.uuid4()),
            'title': 'Essential Linux Commands for System Administration',
            'slug': 'essential-linux-commands',
            'description': 'Must-know Linux commands for file management, process monitoring, and system administration.',
            'category': 'configuration',
            'os': ['linux', 'ubuntu', 'centos', 'debian'],
            'difficulty': 'beginner',
            'views': 22340,
            'likes': 567,
            'author': 'Admin',
            'createdAt': datetime.utcnow(),
            'updatedAt': datetime.utcnow(),
            'tags': ['linux', 'commands', 'basics', 'cli'],
            'steps': [
                {
                    'title': 'File and Directory Operations',
                    'description': 'Basic file management commands.',
                    'code': 'ls -la          # List all files\npwd             # Print working directory\ncd /path        # Change directory\nmkdir newdir    # Create directory\ncp file1 file2  # Copy file\nmv old new      # Move/rename\nrm -rf dir      # Remove directory',
                    'language': 'bash'
                },
                {
                    'title': 'Process Management',
                    'description': 'Monitor and control processes.',
                    'code': 'ps aux          # List all processes\ntop             # Real-time monitoring\nkill -9 PID     # Force kill process\nsystemctl status nginx # Check service',
                    'language': 'bash'
                }
            ]
        },
        {
            'id': str(uuid.uuid4()),
            'title': 'Setup Automatic Security Updates',
            'slug': 'automatic-security-updates',
            'description': 'Configure automatic security updates for Ubuntu and CentOS servers.',
            'category': 'security',
            'os': ['ubuntu', 'centos', 'debian'],
            'difficulty': 'intermediate',
            'views': 8920,
            'likes': 201,
            'author': 'Admin',
            'createdAt': datetime.utcnow(),
            'updatedAt': datetime.utcnow(),
            'tags': ['updates', 'security', 'automation'],
            'steps': [
                {
                    'title': 'Install Unattended Upgrades (Ubuntu/Debian)',
                    'description': 'Enable automatic security updates.',
                    'code': 'sudo apt install unattended-upgrades -y\nsudo dpkg-reconfigure --priority=low unattended-upgrades',
                    'language': 'bash'
                }
            ]
        },
        {
            'id': str(uuid.uuid4()),
            'title': 'Install Docker and Docker Compose',
            'slug': 'install-docker-docker-compose',
            'description': 'Install Docker container platform and Docker Compose on Linux servers.',
            'category': 'installation',
            'os': ['ubuntu', 'centos', 'debian'],
            'difficulty': 'intermediate',
            'views': 19850,
            'likes': 478,
            'author': 'Admin',
            'createdAt': datetime.utcnow(),
            'updatedAt': datetime.utcnow(),
            'tags': ['docker', 'containers', 'docker-compose'],
            'steps': [
                {
                    'title': 'Install Docker (Ubuntu/Debian)',
                    'description': 'Install Docker using official repository.',
                    'code': 'sudo apt update\nsudo apt install ca-certificates curl gnupg -y\ncurl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg\nsudo apt update\nsudo apt install docker-ce docker-ce-cli containerd.io -y',
                    'language': 'bash'
                },
                {
                    'title': 'Start Docker Service',
                    'description': 'Enable and start Docker daemon.',
                    'code': 'sudo systemctl start docker\nsudo systemctl enable docker\nsudo systemctl status docker',
                    'language': 'bash'
                }
            ]
        }
    ]
    
    result = await db.code_snippets.insert_many(snippets)
    print(f"Seeded {len(result.inserted_ids)} code snippets successfully!")
    client.close()

if __name__ == "__main__":
    asyncio.run(seed_database())