export const categories = [
  { id: 1, name: 'Installation', slug: 'installation', icon: 'Download' },
  { id: 2, name: 'Configuration', slug: 'configuration', icon: 'Settings' },
  { id: 3, name: 'Security', slug: 'security', icon: 'Shield' },
  { id: 4, name: 'Networking', slug: 'networking', icon: 'Network' },
  { id: 5, name: 'Database', slug: 'database', icon: 'Database' },
  { id: 6, name: 'Web Server', slug: 'web-server', icon: 'Server' },
  { id: 7, name: 'Monitoring', slug: 'monitoring', icon: 'Activity' },
  { id: 8, name: 'Backup', slug: 'backup', icon: 'HardDrive' },
];

export const operatingSystems = [
  { id: 1, name: 'Ubuntu', slug: 'ubuntu', color: '#E95420' },
  { id: 2, name: 'CentOS', slug: 'centos', color: '#932279' },
  { id: 3, name: 'Debian', slug: 'debian', color: '#A80030' },
  { id: 4, name: 'RHEL', slug: 'rhel', color: '#EE0000' },
  { id: 5, name: 'Fedora', slug: 'fedora', color: '#294172' },
  { id: 6, name: 'Linux (Generic)', slug: 'linux', color: '#FCC624' },
];

export const difficultyLevels = [
  { id: 1, name: 'Beginner', slug: 'beginner', color: '#10B981' },
  { id: 2, name: 'Intermediate', slug: 'intermediate', color: '#F59E0B' },
  { id: 3, name: 'Advanced', slug: 'advanced', color: '#EF4444' },
];

export const codeSnippets = [
  {
    id: 1,
    title: 'Install cPanel on Ubuntu Server',
    slug: 'install-cpanel-ubuntu',
    description: 'Complete guide to install cPanel & WHM on Ubuntu Linux server with all prerequisites and post-installation steps.',
    category: 'installation',
    os: ['ubuntu', 'linux'],
    difficulty: 'intermediate',
    views: 15420,
    likes: 342,
    comments: 28,
    author: 'Admin',
    createdAt: '2025-01-15',
    tags: ['cpanel', 'whm', 'hosting', 'web-panel'],
    steps: [
      {
        title: 'Update System Packages',
        description: 'First, update all system packages to ensure you have the latest security patches.',
        code: 'apt update && apt upgrade -y\nreboot',
        language: 'bash'
      },
      {
        title: 'Set Hostname (FQDN Required)',
        description: 'cPanel requires a fully qualified domain name. Replace server.yourdomain.com with your actual domain.',
        code: 'hostnamectl set-hostname server.yourdomain.com\necho "your_server_IP server.yourdomain.com server" >> /etc/hosts\nhostname',
        language: 'bash'
      },
      {
        title: 'Install Screen (Optional but Recommended)',
        description: 'Screen helps maintain installation session if connection drops.',
        code: 'apt install screen -y\nscreen',
        language: 'bash'
      },
      {
        title: 'Download and Run cPanel Installer',
        description: 'This process takes 30-60 minutes. Do not interrupt the installation.',
        code: 'cd /home\ncurl -o latest -L https://securedownloads.cpanel.net/latest\nsh latest',
        language: 'bash'
      },
      {
        title: 'Configure Firewall Ports',
        description: 'Allow cPanel/WHM ports through firewall.',
        code: 'ufw allow 2087\nufw allow 2083\nufw allow 2082\nufw allow 2086\nufw enable\nufw status',
        language: 'bash'
      }
    ],
    postInstallation: {
      title: 'Post-Installation Steps',
      content: 'Access WHM at https://your_server_IP:2087 using root credentials. Activate your license and create cPanel accounts.'
    }
  },
  {
    id: 2,
    title: 'SSH Security Hardening Best Practices',
    slug: 'ssh-security-hardening',
    description: 'Secure your Linux server SSH access with key-based authentication, disable root login, and implement fail2ban protection.',
    category: 'security',
    os: ['ubuntu', 'centos', 'debian', 'linux'],
    difficulty: 'intermediate',
    views: 12850,
    likes: 289,
    comments: 45,
    author: 'Admin',
    createdAt: '2025-01-20',
    tags: ['ssh', 'security', 'authentication', 'fail2ban'],
    steps: [
      {
        title: 'Generate SSH Key Pair',
        description: 'Create SSH keys on your local machine (client).',
        code: 'ssh-keygen -t ed25519 -C "your_email@example.com"\n# Or for better compatibility:\nssh-keygen -t rsa -b 4096 -C "your_email@example.com"',
        language: 'bash'
      },
      {
        title: 'Copy Public Key to Server',
        description: 'Transfer your public key to the remote server.',
        code: 'ssh-copy-id user@server_ip\n# Or manually:\ncat ~/.ssh/id_ed25519.pub | ssh user@server_ip "mkdir -p ~/.ssh && cat >> ~/.ssh/authorized_keys"',
        language: 'bash'
      },
      {
        title: 'Configure SSH Daemon',
        description: 'Edit SSH configuration for enhanced security.',
        code: 'sudo nano /etc/ssh/sshd_config\n\n# Add or modify these lines:\nPubkeyAuthentication yes\nPasswordAuthentication no\nPermitRootLogin no\nPort 2222  # Change default port\nAllowGroups sshgroup\nClientAliveInterval 300\nClientAliveCountMax 2',
        language: 'bash'
      },
      {
        title: 'Create SSH User Group',
        description: 'Restrict SSH access to specific user group.',
        code: 'sudo groupadd sshgroup\nsudo usermod -aG sshgroup your_username',
        language: 'bash'
      },
      {
        title: 'Restart SSH Service',
        description: 'Apply changes by restarting SSH daemon.',
        code: 'sudo systemctl restart sshd\nsudo systemctl status sshd',
        language: 'bash'
      },
      {
        title: 'Install and Configure Fail2ban',
        description: 'Protect against brute-force attacks.',
        code: '# Ubuntu/Debian\nsudo apt install fail2ban -y\n\n# CentOS/RHEL\nsudo yum install fail2ban -y\n\nsudo systemctl enable fail2ban\nsudo systemctl start fail2ban\nsudo systemctl status fail2ban',
        language: 'bash'
      }
    ]
  },
  {
    id: 3,
    title: 'Configure UFW Firewall on Ubuntu',
    slug: 'configure-ufw-firewall-ubuntu',
    description: 'Step-by-step guide to set up and configure UFW (Uncomplicated Firewall) on Ubuntu Linux server.',
    category: 'security',
    os: ['ubuntu', 'debian'],
    difficulty: 'beginner',
    views: 9340,
    likes: 178,
    comments: 22,
    author: 'Admin',
    createdAt: '2025-01-22',
    tags: ['ufw', 'firewall', 'security', 'networking'],
    steps: [
      {
        title: 'Check UFW Status',
        description: 'Verify if UFW is installed and check its status.',
        code: 'sudo ufw status verbose',
        language: 'bash'
      },
      {
        title: 'Set Default Policies',
        description: 'Deny all incoming and allow all outgoing by default.',
        code: 'sudo ufw default deny incoming\nsudo ufw default allow outgoing',
        language: 'bash'
      },
      {
        title: 'Allow SSH (Important!)',
        description: 'Allow SSH before enabling firewall to prevent lockout.',
        code: 'sudo ufw allow ssh\n# Or specific port:\nsudo ufw allow 22/tcp',
        language: 'bash'
      },
      {
        title: 'Allow Common Services',
        description: 'Open ports for web server and other services.',
        code: 'sudo ufw allow 80/tcp   # HTTP\nsudo ufw allow 443/tcp  # HTTPS\nsudo ufw allow 3306/tcp # MySQL\nsudo ufw allow 25/tcp   # SMTP',
        language: 'bash'
      },
      {
        title: 'Enable UFW',
        description: 'Activate the firewall with configured rules.',
        code: 'sudo ufw enable\nsudo ufw status numbered',
        language: 'bash'
      },
      {
        title: 'Delete Rules (If Needed)',
        description: 'Remove specific firewall rules by number.',
        code: 'sudo ufw status numbered\nsudo ufw delete [rule_number]',
        language: 'bash'
      }
    ]
  },
  {
    id: 4,
    title: 'Install NGINX Web Server',
    slug: 'install-nginx-web-server',
    description: 'Install and configure NGINX high-performance web server on Linux.',
    category: 'web-server',
    os: ['ubuntu', 'centos', 'debian'],
    difficulty: 'beginner',
    views: 18750,
    likes: 425,
    comments: 67,
    author: 'Admin',
    createdAt: '2025-01-18',
    tags: ['nginx', 'web-server', 'installation'],
    steps: [
      {
        title: 'Install NGINX (Ubuntu/Debian)',
        description: 'Install NGINX using apt package manager.',
        code: 'sudo apt update\nsudo apt install nginx -y',
        language: 'bash'
      },
      {
        title: 'Install NGINX (CentOS/RHEL)',
        description: 'Install NGINX using yum/dnf package manager.',
        code: 'sudo yum install epel-release -y\nsudo yum install nginx -y\n# Or with dnf:\nsudo dnf install nginx -y',
        language: 'bash'
      },
      {
        title: 'Start and Enable NGINX',
        description: 'Start NGINX service and enable it to start on boot.',
        code: 'sudo systemctl start nginx\nsudo systemctl enable nginx\nsudo systemctl status nginx',
        language: 'bash'
      },
      {
        title: 'Configure Firewall',
        description: 'Allow HTTP and HTTPS traffic through firewall.',
        code: '# Ubuntu (UFW)\nsudo ufw allow \'Nginx Full\'\n\n# CentOS (firewalld)\nsudo firewall-cmd --permanent --add-service=http\nsudo firewall-cmd --permanent --add-service=https\nsudo firewall-cmd --reload',
        language: 'bash'
      },
      {
        title: 'Test NGINX Configuration',
        description: 'Verify NGINX configuration syntax.',
        code: 'sudo nginx -t\nsudo systemctl reload nginx',
        language: 'bash'
      }
    ]
  },
  {
    id: 5,
    title: 'Install MySQL Database Server',
    slug: 'install-mysql-database',
    description: 'Complete guide to install and secure MySQL database server on Linux.',
    category: 'database',
    os: ['ubuntu', 'centos', 'debian'],
    difficulty: 'beginner',
    views: 14230,
    likes: 312,
    comments: 54,
    author: 'Admin',
    createdAt: '2025-01-16',
    tags: ['mysql', 'database', 'installation', 'mariadb'],
    steps: [
      {
        title: 'Install MySQL (Ubuntu/Debian)',
        description: 'Install MySQL server using apt.',
        code: 'sudo apt update\nsudo apt install mysql-server -y',
        language: 'bash'
      },
      {
        title: 'Install MySQL (CentOS/RHEL)',
        description: 'Install MySQL server using yum/dnf.',
        code: 'sudo yum install mysql-server -y\n# Or MariaDB:\nsudo yum install mariadb-server -y',
        language: 'bash'
      },
      {
        title: 'Start MySQL Service',
        description: 'Start and enable MySQL service.',
        code: 'sudo systemctl start mysql\nsudo systemctl enable mysql\nsudo systemctl status mysql',
        language: 'bash'
      },
      {
        title: 'Secure MySQL Installation',
        description: 'Run security script to set root password and remove test databases.',
        code: 'sudo mysql_secure_installation',
        language: 'bash'
      },
      {
        title: 'Login to MySQL',
        description: 'Access MySQL command line interface.',
        code: 'sudo mysql -u root -p',
        language: 'bash'
      },
      {
        title: 'Create Database and User',
        description: 'Create a new database and grant privileges.',
        code: 'CREATE DATABASE mydatabase;\nCREATE USER \'myuser\'@\'localhost\' IDENTIFIED BY \'strong_password\';\nGRANT ALL PRIVILEGES ON mydatabase.* TO \'myuser\'@\'localhost\';\nFLUSH PRIVILEGES;\nEXIT;',
        language: 'sql'
      }
    ]
  },
  {
    id: 6,
    title: 'Essential Linux Commands for System Administration',
    slug: 'essential-linux-commands',
    description: 'Must-know Linux commands for file management, process monitoring, and system administration.',
    category: 'configuration',
    os: ['linux', 'ubuntu', 'centos', 'debian'],
    difficulty: 'beginner',
    views: 22340,
    likes: 567,
    comments: 89,
    author: 'Admin',
    createdAt: '2025-01-10',
    tags: ['linux', 'commands', 'basics', 'cli'],
    steps: [
      {
        title: 'File and Directory Operations',
        description: 'Basic file management commands.',
        code: 'ls -la          # List all files with details\npwd             # Print working directory\ncd /path/to/dir # Change directory\nmkdir newdir    # Create directory\ncp file1 file2  # Copy file\nmv old new      # Move/rename\nrm -rf dir      # Remove directory\ntouch file.txt  # Create empty file',
        language: 'bash'
      },
      {
        title: 'File Content and Search',
        description: 'View and search file contents.',
        code: 'cat file.txt           # Display file content\nless file.txt          # View file with pagination\nhead -n 20 file.txt    # First 20 lines\ntail -f /var/log/syslog # Follow log file\ngrep "error" file.txt  # Search in file\nfind / -name "*.conf"  # Find files by name',
        language: 'bash'
      },
      {
        title: 'Process Management',
        description: 'Monitor and control processes.',
        code: 'ps aux              # List all processes\ntop                 # Real-time process monitoring\nhtop                # Interactive process viewer\nkill -9 PID         # Force kill process\npkill process_name  # Kill by name\nsystemctl status nginx # Check service status',
        language: 'bash'
      },
      {
        title: 'Network Commands',
        description: 'Network troubleshooting and monitoring.',
        code: 'ping google.com        # Test connectivity\nss -tuln               # List listening ports\nnetstat -tuln          # Network statistics\nip addr show           # Show IP addresses\ncurl https://api.com   # HTTP request\nwget https://file.com  # Download file',
        language: 'bash'
      },
      {
        title: 'User and Permission Management',
        description: 'Manage users and file permissions.',
        code: 'sudo command          # Run as superuser\nuseradd newuser       # Create user\npasswd username       # Change password\nchmod 755 file        # Change permissions\nchown user:group file # Change ownership\nls -l file            # View permissions',
        language: 'bash'
      },
      {
        title: 'Disk Usage and Monitoring',
        description: 'Check disk space and usage.',
        code: 'df -h              # Disk space usage\ndu -sh /var/*      # Directory sizes\nfree -h            # Memory usage\nuptime             # System uptime\ndate               # Current date/time',
        language: 'bash'
      }
    ]
  },
  {
    id: 7,
    title: 'Setup Automatic Security Updates',
    slug: 'automatic-security-updates',
    description: 'Configure automatic security updates for Ubuntu and CentOS servers.',
    category: 'security',
    os: ['ubuntu', 'centos', 'debian'],
    difficulty: 'intermediate',
    views: 8920,
    likes: 201,
    comments: 31,
    author: 'Admin',
    createdAt: '2025-01-25',
    tags: ['updates', 'security', 'automation'],
    steps: [
      {
        title: 'Install Unattended Upgrades (Ubuntu/Debian)',
        description: 'Enable automatic security updates.',
        code: 'sudo apt install unattended-upgrades -y\nsudo dpkg-reconfigure --priority=low unattended-upgrades',
        language: 'bash'
      },
      {
        title: 'Configure Auto Updates (Ubuntu)',
        description: 'Edit configuration file for automatic updates.',
        code: 'sudo nano /etc/apt/apt.conf.d/50unattended-upgrades\n\n# Uncomment security updates line:\nUnattended-Upgrade::Allowed-Origins {\n    "${distro_id}:${distro_codename}-security";\n};',
        language: 'bash'
      },
      {
        title: 'Enable Automatic Updates (CentOS/RHEL)',
        description: 'Install and configure yum-cron.',
        code: 'sudo yum install yum-cron -y\nsudo systemctl enable yum-cron\nsudo systemctl start yum-cron',
        language: 'bash'
      },
      {
        title: 'Configure Yum-Cron (CentOS)',
        description: 'Set to apply security updates automatically.',
        code: 'sudo nano /etc/yum/yum-cron.conf\n\n# Change these lines:\napply_updates = yes\nupdate_cmd = security',
        language: 'bash'
      }
    ]
  },
  {
    id: 8,
    title: 'Install Docker and Docker Compose',
    slug: 'install-docker-docker-compose',
    description: 'Install Docker container platform and Docker Compose on Linux servers.',
    category: 'installation',
    os: ['ubuntu', 'centos', 'debian'],
    difficulty: 'intermediate',
    views: 19850,
    likes: 478,
    comments: 92,
    author: 'Admin',
    createdAt: '2025-01-12',
    tags: ['docker', 'containers', 'docker-compose'],
    steps: [
      {
        title: 'Install Docker (Ubuntu/Debian)',
        description: 'Install Docker using official repository.',
        code: 'sudo apt update\nsudo apt install ca-certificates curl gnupg -y\nsudo install -m 0755 -d /etc/apt/keyrings\ncurl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg\nsudo chmod a+r /etc/apt/keyrings/docker.gpg\n\necho "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null\n\nsudo apt update\nsudo apt install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin -y',
        language: 'bash'
      },
      {
        title: 'Install Docker (CentOS/RHEL)',
        description: 'Install Docker on CentOS.',
        code: 'sudo yum install -y yum-utils\nsudo yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo\nsudo yum install docker-ce docker-ce-cli containerd.io docker-compose-plugin -y',
        language: 'bash'
      },
      {
        title: 'Start Docker Service',
        description: 'Enable and start Docker daemon.',
        code: 'sudo systemctl start docker\nsudo systemctl enable docker\nsudo systemctl status docker',
        language: 'bash'
      },
      {
        title: 'Add User to Docker Group',
        description: 'Run Docker without sudo.',
        code: 'sudo usermod -aG docker $USER\nnewgrp docker',
        language: 'bash'
      },
      {
        title: 'Verify Docker Installation',
        description: 'Test Docker with hello-world container.',
        code: 'docker --version\ndocker compose version\ndocker run hello-world',
        language: 'bash'
      }
    ]
  }
];

export const recentActivity = [
  { user: 'JohnDev', action: 'liked', snippet: 'Install cPanel on Ubuntu Server', time: '5 minutes ago' },
  { user: 'SarahAdmin', action: 'commented on', snippet: 'SSH Security Hardening', time: '12 minutes ago' },
  { user: 'MikeOps', action: 'viewed', snippet: 'Configure UFW Firewall', time: '23 minutes ago' },
  { user: 'EmilyTech', action: 'liked', snippet: 'Essential Linux Commands', time: '45 minutes ago' },
];
