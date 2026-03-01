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

DEBIAN_ARTICLES = [
    {
        'title': 'Debian 12 Bookworm Server Installation',
        'description': 'Complete guide to install Debian 12 Bookworm as a server.',
        'category': 'installation',
        'subcategory': 'debian',
        'os': ['debian', 'linux'],
        'difficulty': 'beginner',
        'tags': ['debian', 'installation', 'server', 'linux', 'bookworm'],
        'steps': [
            {'title': 'Download Debian ISO', 'description': 'Get the installation image.', 'code': 'Download from:\nhttps://www.debian.org/distrib/\n\nOptions:\n- netinst ISO (~600MB) - recommended\n- DVD ISO (~4GB) - for offline install\n- Cloud images for VPS\n\nVerify:\nsha512sum debian-12.x.x-amd64-netinst.iso', 'language': 'bash'},
            {'title': 'Create Bootable USB', 'description': 'Prepare installation media.', 'code': '# Linux\nsudo dd if=debian-12-amd64-netinst.iso of=/dev/sdX bs=4M status=progress sync\n\n# Or use cp\nsudo cp debian-12-amd64-netinst.iso /dev/sdX\nsync', 'language': 'bash'},
            {'title': 'Install Debian', 'description': 'Follow Debian installer.', 'code': 'Installation Steps:\n1. Boot from USB\n2. Select "Install" or "Graphical Install"\n3. Language, Location, Keyboard\n4. Hostname and Domain\n5. Root password (or skip for sudo only)\n6. Create user account\n7. Partitioning:\n   - Guided - use entire disk (simple)\n   - Manual (advanced)\n8. Package manager mirror\n9. Software selection:\n   - SSH server (important)\n   - Standard system utilities\n10. Install GRUB bootloader\n11. Reboot', 'language': 'bash'},
            {'title': 'Post-Installation', 'description': 'Initial setup.', 'code': '# Login as root or user\n\n# Update system\nsudo apt update && sudo apt upgrade -y\n\n# Install essentials\nsudo apt install -y curl wget git vim htop net-tools sudo\n\n# Add user to sudo (if root password was set)\nsu -\nusermod -aG sudo username\nexit\n\n# Configure timezone\nsudo timedatectl set-timezone Asia/Kolkata\n\n# Install firewall\nsudo apt install -y ufw\nsudo ufw allow ssh\nsudo ufw enable', 'language': 'bash'}
        ],
        'postInstallation': {'title': 'Debian vs Ubuntu', 'content': 'Debian is more stable, slower updates. Uses same apt package manager. Default shell is dash (change to bash if needed). Minimal install by default - add packages as needed.'}
    },
    {
        'title': 'Debian APT Package Management',
        'description': 'Complete guide to APT package management on Debian systems.',
        'category': 'configuration',
        'subcategory': 'debian',
        'os': ['debian', 'linux'],
        'difficulty': 'beginner',
        'tags': ['debian', 'apt', 'package-manager', 'linux', 'dpkg'],
        'steps': [
            {'title': 'Update and Upgrade', 'description': 'Keep system updated.', 'code': '# Update package lists\nsudo apt update\n\n# Upgrade packages\nsudo apt upgrade -y\n\n# Full upgrade (may remove packages)\nsudo apt full-upgrade -y\n\n# Distribution upgrade\nsudo apt dist-upgrade -y', 'language': 'bash'},
            {'title': 'Install and Remove', 'description': 'Manage packages.', 'code': '# Install package\nsudo apt install nginx\n\n# Install without prompts\nsudo apt install -y nginx php mariadb-server\n\n# Install specific version\nsudo apt install nginx=1.22.0-1\n\n# Remove package\nsudo apt remove nginx\n\n# Remove with config\nsudo apt purge nginx\n\n# Remove unused dependencies\nsudo apt autoremove', 'language': 'bash'},
            {'title': 'Search and Information', 'description': 'Find packages.', 'code': '# Search packages\napt search nginx\napt-cache search nginx\n\n# Show package info\napt show nginx\napt-cache show nginx\n\n# List installed\napt list --installed\ndpkg -l\n\n# Check if installed\ndpkg -l | grep nginx\n\n# Show package files\ndpkg -L nginx', 'language': 'bash'},
            {'title': 'Repository Management', 'description': 'Add and manage repos.', 'code': '# View sources\ncat /etc/apt/sources.list\nls /etc/apt/sources.list.d/\n\n# Add repository\necho "deb http://repo.example.com/debian bookworm main" | sudo tee /etc/apt/sources.list.d/example.list\n\n# Add GPG key\ncurl -fsSL https://repo.example.com/key.gpg | sudo gpg --dearmor -o /etc/apt/keyrings/example.gpg\n\n# Enable contrib and non-free\nsudo apt-add-repository contrib\nsudo apt-add-repository non-free\n\nsudo apt update', 'language': 'bash'}
        ],
        'postInstallation': {'title': 'Cleanup', 'content': 'Clean cache: sudo apt clean. Remove old packages: sudo apt autoremove. Fix broken: sudo apt --fix-broken install. List upgradable: apt list --upgradable'}
    },
    {
        'title': 'Debian Backports and Third-Party Repos',
        'description': 'Use Debian backports to get newer software versions.',
        'category': 'configuration',
        'subcategory': 'debian',
        'os': ['debian', 'linux'],
        'difficulty': 'intermediate',
        'tags': ['debian', 'backports', 'repository', 'linux'],
        'steps': [
            {'title': 'Enable Backports', 'description': 'Add backports repository.', 'code': '# Add backports for Debian 12 (bookworm)\necho "deb http://deb.debian.org/debian bookworm-backports main contrib non-free" | sudo tee /etc/apt/sources.list.d/backports.list\n\nsudo apt update\n\n# List backports packages\napt -t bookworm-backports list', 'language': 'bash'},
            {'title': 'Install from Backports', 'description': 'Install newer versions.', 'code': '# Install from backports\nsudo apt -t bookworm-backports install package-name\n\n# Example: newer kernel\nsudo apt -t bookworm-backports install linux-image-amd64\n\n# Example: newer PHP\nsudo apt -t bookworm-backports install php', 'language': 'bash'},
            {'title': 'Add Docker Repository', 'description': 'Example of third-party repo.', 'code': '# Remove old versions\nsudo apt remove docker docker-engine docker.io containerd runc\n\n# Add Docker GPG key\nsudo install -m 0755 -d /etc/apt/keyrings\ncurl -fsSL https://download.docker.com/linux/debian/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg\n\n# Add repository\necho "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/debian $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list\n\n# Install\nsudo apt update\nsudo apt install docker-ce docker-ce-cli containerd.io', 'language': 'bash'},
            {'title': 'Pin Package Versions', 'description': 'Control package priorities.', 'code': '# Create pin file\nsudo nano /etc/apt/preferences.d/backports\n\n# Pin to prefer stable\nPackage: *\nPin: release a=bookworm-backports\nPin-Priority: 100\n\n# Pin specific package from backports\nPackage: nginx\nPin: release a=bookworm-backports\nPin-Priority: 500\n\n# Check policy\napt-cache policy nginx', 'language': 'bash'}
        ],
        'postInstallation': {'title': 'Warning', 'content': 'Backports are not security supported like stable. Mix stable and backports carefully. Always specify -t for backports install. Check package compatibility before upgrading.'}
    }
]

FEDORA_ARTICLES = [
    {
        'title': 'Fedora 39 Workstation Installation',
        'description': 'Install Fedora 39 Workstation with GNOME desktop.',
        'category': 'installation',
        'subcategory': 'fedora',
        'os': ['fedora', 'linux'],
        'difficulty': 'beginner',
        'tags': ['fedora', 'installation', 'desktop', 'gnome', 'linux'],
        'steps': [
            {'title': 'Download Fedora', 'description': 'Get Fedora ISO.', 'code': 'Download from:\nhttps://getfedora.org/\n\nOptions:\n- Fedora Workstation (GNOME)\n- Fedora KDE Spin\n- Fedora Server\n- Fedora Silverblue (immutable)\n\nUse Fedora Media Writer for easy USB creation', 'language': 'bash'},
            {'title': 'Create Bootable USB', 'description': 'Using Fedora Media Writer.', 'code': '# Download Fedora Media Writer\nhttps://getfedora.org/en/workstation/download/\n\n# Or on Linux:\nsudo dnf install mediawriter\nfedora-media-writer\n\n# Or dd method:\nsudo dd if=Fedora-Workstation-Live-x86_64-39.iso of=/dev/sdX bs=4M status=progress', 'language': 'bash'},
            {'title': 'Install Fedora', 'description': 'Follow Anaconda installer.', 'code': 'Installation Steps:\n1. Boot from USB\n2. Select "Start Fedora-Workstation"\n3. Click "Install to Hard Drive"\n4. Language selection\n5. Installation Summary:\n   - Keyboard layout\n   - Time & Date\n   - Installation Destination\n6. Begin Installation\n7. Reboot\n8. Complete setup wizard:\n   - Privacy settings\n   - Enable third-party repos\n   - Create user account', 'language': 'bash'},
            {'title': 'Post-Installation', 'description': 'Setup and customization.', 'code': '# Update system\nsudo dnf update -y\n\n# Enable RPM Fusion (free and nonfree)\nsudo dnf install https://download1.rpmfusion.org/free/fedora/rpmfusion-free-release-$(rpm -E %fedora).noarch.rpm\nsudo dnf install https://download1.rpmfusion.org/nonfree/fedora/rpmfusion-nonfree-release-$(rpm -E %fedora).noarch.rpm\n\n# Install media codecs\nsudo dnf group install Multimedia\n\n# Install GNOME Tweaks\nsudo dnf install gnome-tweaks\n\n# Install Flathub\nflatpak remote-add --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo', 'language': 'bash'}
        ],
        'postInstallation': {'title': 'Fedora Tips', 'content': 'Fedora uses DNF package manager. New version every 6 months. Upgrade with: sudo dnf system-upgrade. Consider Silverblue for atomic/immutable desktop.'}
    },
    {
        'title': 'Fedora DNF Package Management',
        'description': 'Master DNF commands on Fedora Linux.',
        'category': 'configuration',
        'subcategory': 'fedora',
        'os': ['fedora', 'linux'],
        'difficulty': 'beginner',
        'tags': ['fedora', 'dnf', 'package-manager', 'linux'],
        'steps': [
            {'title': 'Basic Commands', 'description': 'Common DNF operations.', 'code': '# Update system\nsudo dnf update -y\n\n# Install package\nsudo dnf install package-name -y\n\n# Remove package\nsudo dnf remove package-name\n\n# Search\ndnf search keyword\n\n# Info\ndnf info package-name\n\n# List installed\ndnf list installed', 'language': 'bash'},
            {'title': 'Group Management', 'description': 'Install package groups.', 'code': '# List available groups\ndnf group list\n\n# Install group\nsudo dnf group install "Development Tools"\nsudo dnf group install "Virtualization"\n\n# Remove group\nsudo dnf group remove "Development Tools"\n\n# Group info\ndnf group info "Development Tools"', 'language': 'bash'},
            {'title': 'Repository Management', 'description': 'Manage DNF repos.', 'code': '# List repos\ndnf repolist\ndnf repolist all\n\n# Enable/disable repo\nsudo dnf config-manager --enable repo-name\nsudo dnf config-manager --disable repo-name\n\n# Add repo\nsudo dnf config-manager --add-repo URL\n\n# Enable RPM Fusion\nsudo dnf install \\\n  https://download1.rpmfusion.org/free/fedora/rpmfusion-free-release-$(rpm -E %fedora).noarch.rpm \\\n  https://download1.rpmfusion.org/nonfree/fedora/rpmfusion-nonfree-release-$(rpm -E %fedora).noarch.rpm', 'language': 'bash'},
            {'title': 'History and Cleanup', 'description': 'Manage DNF history.', 'code': '# View history\ndnf history\n\n# Undo transaction\nsudo dnf history undo ID\n\n# Redo transaction\nsudo dnf history redo ID\n\n# Cleanup\nsudo dnf clean all\nsudo dnf autoremove\n\n# Remove old kernels (keep 2)\nsudo dnf remove --oldinstallonly --setopt installonly_limit=2 kernel', 'language': 'bash'}
        ],
        'postInstallation': {'title': 'DNF Config', 'content': 'Config file: /etc/dnf/dnf.conf. Add fastestmirror=1 and max_parallel_downloads=10 for faster downloads. Use dnf5 on Fedora 39+ for improved performance.'}
    }
]

LINUX_GENERIC_ARTICLES = [
    {
        'title': 'Linux File Permissions Explained',
        'description': 'Complete guide to Linux file permissions, ownership, and chmod.',
        'category': 'security',
        'subcategory': 'linux',
        'os': ['ubuntu', 'centos', 'debian', 'linux'],
        'difficulty': 'beginner',
        'tags': ['linux', 'permissions', 'chmod', 'chown', 'security'],
        'steps': [
            {'title': 'Understanding Permissions', 'description': 'Read permission notation.', 'code': '# View permissions\nls -l\n\n# Output: -rwxr-xr-x 1 user group size date filename\n\n# Permission breakdown:\n# - | rwx | r-x | r-x\n# type|owner|group|others\n\n# Types:\n# - = file\n# d = directory\n# l = symbolic link\n\n# Permissions:\n# r = read (4)\n# w = write (2)\n# x = execute (1)', 'language': 'bash'},
            {'title': 'Change Permissions (chmod)', 'description': 'Modify file permissions.', 'code': '# Numeric method\nchmod 755 file.sh    # rwxr-xr-x\nchmod 644 file.txt   # rw-r--r--\nchmod 700 private    # rwx------\nchmod 777 public     # rwxrwxrwx (avoid!)\n\n# Symbolic method\nchmod u+x file.sh    # Add execute for owner\nchmod g-w file.txt   # Remove write for group\nchmod o=r file.txt   # Set others to read only\nchmod a+r file.txt   # Add read for all\n\n# Recursive\nchmod -R 755 directory/', 'language': 'bash'},
            {'title': 'Change Ownership (chown)', 'description': 'Modify file owner and group.', 'code': '# Change owner\nsudo chown newuser file.txt\n\n# Change owner and group\nsudo chown newuser:newgroup file.txt\n\n# Change group only\nsudo chown :newgroup file.txt\nsudo chgrp newgroup file.txt\n\n# Recursive\nsudo chown -R www-data:www-data /var/www/', 'language': 'bash'},
            {'title': 'Special Permissions', 'description': 'SUID, SGID, Sticky bit.', 'code': '# SUID (4) - Run as file owner\nchmod 4755 file.sh\nchmod u+s file.sh\n\n# SGID (2) - Run as group, inherit group in dirs\nchmod 2755 directory/\nchmod g+s directory/\n\n# Sticky bit (1) - Only owner can delete in dir\nchmod 1777 /tmp/shared/\nchmod +t /tmp/shared/\n\n# View special permissions\nls -l\n# s in owner = SUID\n# s in group = SGID\n# t in others = sticky', 'language': 'bash'}
        ],
        'postInstallation': {'title': 'Common Permissions', 'content': 'Directories: 755 (or 750 for restricted). Web files: 644. Scripts: 755. Private files: 600. Shared directory: 775 with SGID.'}
    },
    {
        'title': 'Linux Process Management',
        'description': 'Monitor and manage processes on Linux systems.',
        'category': 'monitoring',
        'subcategory': 'linux',
        'os': ['ubuntu', 'centos', 'debian', 'linux'],
        'difficulty': 'beginner',
        'tags': ['linux', 'processes', 'ps', 'top', 'kill'],
        'steps': [
            {'title': 'View Processes', 'description': 'List running processes.', 'code': '# List all processes\nps aux\nps -ef\n\n# Filter processes\nps aux | grep nginx\nps -ef | grep mysql\n\n# Process tree\npstree\npstree -p  # with PIDs\n\n# Top processes by CPU\nps aux --sort=-%cpu | head\n\n# Top processes by memory\nps aux --sort=-%mem | head', 'language': 'bash'},
            {'title': 'Interactive Monitoring', 'description': 'Real-time process monitoring.', 'code': '# top command\ntop\n\n# Useful top shortcuts:\n# P = sort by CPU\n# M = sort by memory\n# k = kill process\n# q = quit\n\n# htop (better UI)\nsudo apt install htop  # Debian/Ubuntu\nsudo dnf install htop  # Fedora/CentOS\nhtop\n\n# Filter in htop\n# F4 = filter\n# F5 = tree view\n# F9 = kill', 'language': 'bash'},
            {'title': 'Kill Processes', 'description': 'Terminate processes.', 'code': '# Kill by PID\nkill 1234\n\n# Force kill\nkill -9 1234\nkill -SIGKILL 1234\n\n# Kill by name\nkillall nginx\npkill nginx\n\n# Kill with pattern\npkill -f "python script.py"\n\n# Common signals:\n# SIGTERM (15) - Graceful shutdown (default)\n# SIGKILL (9) - Force kill\n# SIGHUP (1) - Reload config\n# SIGSTOP (19) - Pause process', 'language': 'bash'},
            {'title': 'Background Processes', 'description': 'Run and manage background jobs.', 'code': '# Run in background\ncommand &\nnohup command &\n\n# List background jobs\njobs\n\n# Bring to foreground\nfg %1\n\n# Send to background\nbg %1\n\n# Ctrl+Z = pause current process\n# Then: bg to continue in background\n\n# Detach from terminal\nnohup ./script.sh > output.log 2>&1 &\ndisown %1', 'language': 'bash'}
        ],
        'postInstallation': {'title': 'Tools', 'content': 'Use htop for better visualization. Use systemd for service management. Monitor with tools like glances, atop, or nmon for detailed analysis.'}
    },
    {
        'title': 'Linux Disk Management',
        'description': 'Manage disks, partitions, and filesystems on Linux.',
        'category': 'configuration',
        'subcategory': 'linux',
        'os': ['ubuntu', 'centos', 'debian', 'linux'],
        'difficulty': 'intermediate',
        'tags': ['linux', 'disk', 'partition', 'filesystem', 'fdisk'],
        'steps': [
            {'title': 'View Disk Information', 'description': 'Check disks and partitions.', 'code': '# List block devices\nlsblk\nlsblk -f  # with filesystem info\n\n# Disk usage\ndf -h\ndf -hT  # with filesystem type\n\n# Disk space by directory\ndu -sh /var/*\ndu -h --max-depth=1 /\n\n# Detailed disk info\nsudo fdisk -l\nsudo parted -l', 'language': 'bash'},
            {'title': 'Partition Disk', 'description': 'Create partitions with fdisk.', 'code': '# Start fdisk\nsudo fdisk /dev/sdb\n\n# Commands:\n# m = help\n# p = print partitions\n# n = new partition\n# d = delete partition\n# t = change type\n# w = write and exit\n# q = quit without saving\n\n# Create partition:\n# n → primary → partition number → first sector → size (+10G)\n# w\n\n# Or use parted for GPT\nsudo parted /dev/sdb\n(parted) mklabel gpt\n(parted) mkpart primary ext4 0% 100%\n(parted) quit', 'language': 'bash'},
            {'title': 'Format and Mount', 'description': 'Create filesystem and mount.', 'code': '# Format partition\nsudo mkfs.ext4 /dev/sdb1\nsudo mkfs.xfs /dev/sdb2\n\n# Create mount point\nsudo mkdir -p /mnt/data\n\n# Mount temporarily\nsudo mount /dev/sdb1 /mnt/data\n\n# Unmount\nsudo umount /mnt/data\n\n# Permanent mount (fstab)\nsudo nano /etc/fstab\n\n# Add line:\n/dev/sdb1  /mnt/data  ext4  defaults  0  2\n\n# Or use UUID (preferred)\nUUID=xxxxxxxx  /mnt/data  ext4  defaults  0  2\n\n# Get UUID\nsudo blkid /dev/sdb1\n\n# Mount all from fstab\nsudo mount -a', 'language': 'bash'},
            {'title': 'LVM Management', 'description': 'Logical Volume Management basics.', 'code': '# Create physical volume\nsudo pvcreate /dev/sdb1\n\n# Create volume group\nsudo vgcreate myvg /dev/sdb1\n\n# Create logical volume\nsudo lvcreate -L 10G -n mylv myvg\nsudo lvcreate -l 100%FREE -n mylv myvg  # Use all space\n\n# Format and mount\nsudo mkfs.ext4 /dev/myvg/mylv\nsudo mount /dev/myvg/mylv /mnt/data\n\n# Extend logical volume\nsudo lvextend -L +5G /dev/myvg/mylv\nsudo resize2fs /dev/myvg/mylv  # Extend filesystem\n\n# View LVM\nsudo pvs\nsudo vgs\nsudo lvs', 'language': 'bash'}
        ],
        'postInstallation': {'title': 'Best Practices', 'content': 'Use LVM for flexible storage. Use XFS for large files, ext4 for general use. Always backup before partitioning. Use UUID in fstab for reliability.'}
    },
    {
        'title': 'Linux SSH Key Authentication Setup',
        'description': 'Configure passwordless SSH login using key pairs.',
        'category': 'security',
        'subcategory': 'linux',
        'os': ['ubuntu', 'centos', 'debian', 'linux'],
        'difficulty': 'beginner',
        'tags': ['linux', 'ssh', 'security', 'authentication', 'keys'],
        'steps': [
            {'title': 'Generate SSH Key Pair', 'description': 'Create keys on client machine.', 'code': '# Generate RSA key (4096 bit)\nssh-keygen -t rsa -b 4096 -C "your@email.com"\n\n# Generate Ed25519 key (more secure)\nssh-keygen -t ed25519 -C "your@email.com"\n\n# Default location: ~/.ssh/id_rsa or id_ed25519\n# Enter passphrase (optional but recommended)\n\n# View public key\ncat ~/.ssh/id_rsa.pub\ncat ~/.ssh/id_ed25519.pub', 'language': 'bash'},
            {'title': 'Copy Key to Server', 'description': 'Transfer public key to remote server.', 'code': '# Method 1: ssh-copy-id (easiest)\nssh-copy-id user@server-ip\n\n# Method 2: Manual\ncat ~/.ssh/id_rsa.pub | ssh user@server "mkdir -p ~/.ssh && cat >> ~/.ssh/authorized_keys"\n\n# Method 3: If ssh-copy-id unavailable\nscp ~/.ssh/id_rsa.pub user@server:~/.ssh/authorized_keys\n\n# Test login\nssh user@server-ip', 'language': 'bash'},
            {'title': 'Set Permissions', 'description': 'Correct permissions for SSH to work.', 'code': '# On server - set correct permissions\nchmod 700 ~/.ssh\nchmod 600 ~/.ssh/authorized_keys\n\n# On client\nchmod 700 ~/.ssh\nchmod 600 ~/.ssh/id_rsa\nchmod 644 ~/.ssh/id_rsa.pub', 'language': 'bash'},
            {'title': 'SSH Config File', 'description': 'Create shortcuts for connections.', 'code': 'nano ~/.ssh/config\n\n# Add server configuration\nHost myserver\n    HostName 192.168.1.100\n    User admin\n    Port 22\n    IdentityFile ~/.ssh/id_rsa\n\nHost production\n    HostName prod.example.com\n    User deploy\n    Port 2222\n    IdentityFile ~/.ssh/id_ed25519\n\n# Now connect with:\nssh myserver\nssh production', 'language': 'bash'}
        ],
        'postInstallation': {'title': 'Security', 'content': 'After key setup, disable password authentication in /etc/ssh/sshd_config: PasswordAuthentication no. Use passphrase on private keys. Keep private key secure, never share it.'}
    }
]

async def seed_all_os():
    print("=" * 60)
    print("  SEEDING: Operating System Articles")
    print("=" * 60)
    
    all_articles = []
    all_articles.extend(DEBIAN_ARTICLES)
    all_articles.extend(FEDORA_ARTICLES)
    all_articles.extend(LINUX_GENERIC_ARTICLES)
    
    added = 0
    for article in all_articles:
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
    
    print(f"\n✓ Added {added} articles")
    print(f"  - Debian: {len(DEBIAN_ARTICLES)}")
    print(f"  - Fedora: {len(FEDORA_ARTICLES)}")
    print(f"  - Linux Generic: {len(LINUX_GENERIC_ARTICLES)}")

if __name__ == "__main__":
    asyncio.run(seed_all_os())
