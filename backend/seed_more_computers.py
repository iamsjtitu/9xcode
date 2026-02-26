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

# Comprehensive Windows Server Articles
windows_server_articles = [
    ("Install Windows Server 2008", "Step-by-step Windows Server 2008 installation", ["windows-server", "server-2008", "installation"], ["windows"], "intermediate", [
        {"title": "System Requirements", "description": "Check hardware requirements", "code": "Minimum Requirements:\n- 1 GHz processor\n- 512 MB RAM (2GB recommended)\n- 10 GB disk space\n- DVD drive\n- VGA monitor\n- Network adapter", "language": "bash"},
        {"title": "Boot from DVD", "description": "Start installation", "code": "1. Insert Windows Server 2008 DVD\n2. Boot from DVD\n3. Press any key when prompted\n4. Wait for setup to load", "language": "bash"},
        {"title": "Install Windows", "description": "Complete installation", "code": "1. Select language and region\n2. Click 'Install now'\n3. Select edition (Standard/Enterprise)\n4. Accept license\n5. Choose 'Custom' installation\n6. Select partition\n7. Wait 20-30 minutes", "language": "bash"},
        {"title": "Initial Configuration", "description": "Set up server", "code": "1. Set Administrator password\n2. Configure computer name\n3. Set time zone\n4. Configure network\n5. Enable Windows Update", "language": "bash"}
    ]),
    
    ("Install Windows Server 2012", "Windows Server 2012 R2 installation guide", ["windows-server", "server-2012", "installation"], ["windows"], "intermediate", [
        {"title": "System Requirements", "description": "Hardware prerequisites", "code": "Requirements:\n- 1.4 GHz 64-bit processor\n- 512 MB RAM minimum\n- 32 GB disk space\n- Network adapter\n- DVD drive or USB", "language": "bash"},
        {"title": "Installation Steps", "description": "Install Server 2012", "code": "1. Boot from installation media\n2. Select language preferences\n3. Click 'Install now'\n4. Enter product key\n5. Select edition (Standard/Datacenter)\n6. Choose installation type\n7. Select Server Core or GUI\n8. Configure partition\n9. Complete installation", "language": "bash"}
    ]),
    
    ("Install Windows Server 2016", "Complete Server 2016 installation", ["windows-server", "server-2016", "installation"], ["windows"], "intermediate", [
        {"title": "Prerequisites", "description": "Check requirements", "code": "Requirements:\n- 1.4 GHz processor\n- 512 MB RAM (2GB for Desktop Experience)\n- 32 GB disk minimum\n- TPM 2.0 recommended\n- Network adapter", "language": "bash"},
        {"title": "Installation Process", "description": "Install Server 2016", "code": "1. Boot from media\n2. Select language and keyboard\n3. Click 'Install now'\n4. Select edition\n5. Accept license terms\n6. Choose installation type:\n   - Upgrade\n   - Custom: Install only\n7. Select drive\n8. Wait for installation\n9. Set Administrator password", "language": "bash"}
    ]),
    
    ("Install Windows Server 2019", "Windows Server 2019 setup guide", ["windows-server", "server-2019", "installation"], ["windows"], "intermediate", [
        {"title": "System Requirements", "description": "Hardware specs", "code": "Requirements:\n- 1.4 GHz 64-bit processor\n- 512 MB RAM (2GB with Desktop Experience)\n- 32 GB disk space\n- Network adapter\n- UEFI 2.3.1c firmware", "language": "bash"},
        {"title": "Installation", "description": "Install Server 2019", "code": "1. Boot from installation media\n2. Select language\n3. Click 'Install now'\n4. Select Server edition:\n   - Standard\n   - Datacenter\n5. Choose Desktop Experience or Core\n6. Accept license\n7. Custom installation\n8. Select disk\n9. Complete setup", "language": "bash"}
    ]),
    
    ("Install Windows Server 2022", "Latest Windows Server 2022 installation", ["windows-server", "server-2022", "installation"], ["windows"], "intermediate", [
        {"title": "Hardware Requirements", "description": "Check compatibility", "code": "Requirements:\n- 1.4 GHz 64-bit processor\n- 512 MB RAM minimum\n- 32 GB disk space\n- TPM 2.0 chip\n- Secure Boot capable\n- Network adapter", "language": "bash"},
        {"title": "Installation Steps", "description": "Install Server 2022", "code": "1. Boot from USB/DVD\n2. Select language preferences\n3. Click 'Install now'\n4. Enter product key or skip\n5. Select edition\n6. Accept license\n7. Choose Custom installation\n8. Select partition\n9. Wait for installation\n10. Set strong Administrator password", "language": "bash"}
    ]),
    
    ("Install Windows Server 2025", "Windows Server 2025 installation guide", ["windows-server", "server-2025", "installation"], ["windows"], "beginner", [
        {"title": "System Requirements", "description": "Latest server requirements", "code": "Requirements:\n- 1.4 GHz 64-bit processor\n- 2 GB RAM minimum\n- 40 GB disk space\n- TPM 2.0 required\n- UEFI firmware\n- Secure Boot enabled", "language": "bash"},
        {"title": "Installation Process", "description": "Install Server 2025", "code": "1. Create bootable media\n2. Boot from installation media\n3. Select language and region\n4. Click 'Install now'\n5. Enter product key\n6. Select Server edition\n7. Choose Desktop Experience or Core\n8. Accept terms\n9. Custom installation\n10. Select drive\n11. Complete installation\n12. Configure Administrator account", "language": "bash"}
    ]),
    
    # Additional Computer Articles
    ("Configure Windows Firewall Advanced", "Advanced Windows Firewall configuration", ["windows", "firewall", "security"], ["windows"], "advanced", [
        {"title": "Open Advanced Firewall", "description": "Access advanced settings", "code": "1. Press Win + R\n2. Type: wf.msc\n3. Press Enter\n\nOr via PowerShell:\nStart-Process wf.msc", "language": "powershell"},
        {"title": "Create Advanced Rules", "description": "Configure detailed rules", "code": "# Create inbound rule:\nNew-NetFirewallRule -DisplayName 'Web Server' -Direction Inbound -LocalPort 80,443 -Protocol TCP -Action Allow\n\n# Create outbound rule:\nNew-NetFirewallRule -DisplayName 'Block Telemetry' -Direction Outbound -RemoteAddress 1.2.3.4 -Action Block", "language": "powershell"}
    ]),
    
    ("Windows Server Roles and Features", "Install and configure server roles", ["windows-server", "roles", "features"], ["windows"], "intermediate", [
        {"title": "Install Roles via GUI", "description": "Use Server Manager", "code": "1. Open Server Manager\n2. Click 'Add roles and features'\n3. Select installation type\n4. Select server\n5. Choose roles:\n   - Active Directory\n   - DNS Server\n   - DHCP Server\n   - File Services\n   - Web Server (IIS)\n6. Add features\n7. Confirm and install", "language": "bash"},
        {"title": "Install via PowerShell", "description": "Command-line installation", "code": "# Install AD Domain Services:\nInstall-WindowsFeature -Name AD-Domain-Services -IncludeManagementTools\n\n# Install DNS:\nInstall-WindowsFeature -Name DNS -IncludeManagementTools\n\n# Install IIS:\nInstall-WindowsFeature -Name Web-Server -IncludeManagementTools", "language": "powershell"}
    ]),
    
    ("Configure Windows Server Backup", "Set up automated server backups", ["windows-server", "backup", "recovery"], ["windows"], "intermediate", [
        {"title": "Install Backup Feature", "description": "Add Windows Server Backup", "code": "# Via PowerShell:\nInstall-WindowsFeature Windows-Server-Backup\n\n# Or via Server Manager:\nAdd Roles and Features > Features > Windows Server Backup", "language": "powershell"},
        {"title": "Configure Backup Schedule", "description": "Set up automated backups", "code": "1. Open Windows Server Backup\n2. Click 'Backup Schedule'\n3. Select 'Full server' or 'Custom'\n4. Choose backup time\n5. Select destination (External drive/Network)\n6. Confirm settings\n7. Finish wizard", "language": "bash"}
    ]),
    
    ("Windows Server Performance Monitoring", "Monitor server performance", ["windows-server", "monitoring", "performance"], ["windows"], "intermediate", [
        {"title": "Performance Monitor", "description": "Use built-in monitoring", "code": "1. Press Win + R\n2. Type: perfmon\n3. Press Enter\n\nOr PowerShell:\nStart-Process perfmon", "language": "powershell"},
        {"title": "Monitor Key Metrics", "description": "Track server performance", "code": "Key counters to monitor:\n- Processor: % Processor Time\n- Memory: Available MBytes\n- Disk: % Disk Time\n- Network: Bytes Total/sec\n\nCreate Data Collector Set:\n1. Performance Monitor > Data Collector Sets\n2. User Defined > New\n3. Add counters\n4. Set schedule\n5. Start collection", "language": "bash"}
    ]),
    
    ("macOS System Preferences Guide", "Configure Mac system settings", ["mac", "system-preferences", "configuration"], ["mac"], "beginner", [
        {"title": "System Settings Overview", "description": "Navigate system preferences", "code": "Access System Settings:\n1. Click Apple menu\n2. Select 'System Settings' (or 'System Preferences')\n\nMain categories:\n- Apple ID\n- Wi-Fi & Network\n- Notifications\n- Sound\n- Display\n- Desktop & Dock\n- Security & Privacy\n- Users & Groups", "language": "bash"},
        {"title": "Common Configurations", "description": "Essential settings", "code": "Trackpad:\n1. System Settings > Trackpad\n2. Enable 'Tap to click'\n3. Adjust tracking speed\n\nDock:\n1. System Settings > Desktop & Dock\n2. Adjust size and position\n3. Enable/disable magnification\n\nEnergy Saver:\n1. System Settings > Battery\n2. Adjust display sleep time\n3. Configure power adapter settings", "language": "bash"}
    ]),
    
    ("Windows Registry Backup and Restore", "Safely backup Windows Registry", ["windows", "registry", "backup"], ["windows"], "intermediate", [
        {"title": "Backup Registry", "description": "Create registry backup", "code": "Method 1 - Full Backup:\n1. Press Win + R\n2. Type: regedit\n3. File > Export\n4. Save location\n5. Select 'All' under Export range\n6. Save as .reg file\n\nMethod 2 - PowerShell:\nreg export HKLM C:\\backup\\hklm_backup.reg\nreg export HKCU C:\\backup\\hkcu_backup.reg", "language": "powershell"},
        {"title": "Restore Registry", "description": "Restore from backup", "code": "1. Double-click .reg file\n2. Click 'Yes' to confirm\n3. Or via Command Prompt:\n   reg import C:\\backup\\registry_backup.reg", "language": "bash"}
    ]),
    
    ("Windows Event Viewer Guide", "Monitor system logs and events", ["windows", "event-viewer", "troubleshooting"], ["windows"], "intermediate", [
        {"title": "Open Event Viewer", "description": "Access system logs", "code": "1. Press Win + X\n2. Select 'Event Viewer'\n\nOr:\n1. Press Win + R\n2. Type: eventvwr.msc\n\nOr PowerShell:\nStart-Process eventvwr.msc", "language": "powershell"},
        {"title": "Navigate Logs", "description": "View different log types", "code": "Main log categories:\n\n1. Application Logs:\n   - Application errors\n   - Software events\n\n2. Security Logs:\n   - Login attempts\n   - Permission changes\n\n3. System Logs:\n   - Hardware errors\n   - Driver issues\n   - Service failures\n\n4. Setup Logs:\n   - Installation events", "language": "bash"}
    ]),
]

async def seed_more_computers():
    print("💻 Adding More Computer Articles...\n")
    
    articles_to_add = []
    
    for article in windows_server_articles:
        title, description, tags, os_list, difficulty, steps = article
        snippet = {
            'id': str(uuid.uuid4()),
            'title': title,
            'slug': create_slug(title),
            'description': description,
            'category': 'computers',
            'os': os_list,
            'difficulty': difficulty,
            'views': random.randint(500, 20000),
            'likes': random.randint(20, 500),
            'author': 'Admin',
            'createdAt': datetime.utcnow(),
            'updatedAt': datetime.utcnow(),
            'tags': tags,
            'steps': steps,
        }
        articles_to_add.append(snippet)
    
    result = await db.code_snippets.insert_many(articles_to_add)
    print(f"✅ Added {len(result.inserted_ids)} Computer articles!\n")
    
    # Count by subcategory
    server_count = len([a for a in windows_server_articles if 'windows-server' in a[2]])
    windows_count = len([a for a in windows_server_articles if 'windows' in a[2] and 'windows-server' not in a[2]])
    mac_count = len([a for a in windows_server_articles if 'mac' in a[2]])
    
    print(f"📊 Breakdown:")
    print(f"   Windows Server: {server_count} articles")
    print(f"   Windows: {windows_count} articles")
    print(f"   macOS: {mac_count} articles")
    
    total = await db.code_snippets.count_documents({})
    total_computers = await db.code_snippets.count_documents({'category': 'computers'})
    print(f"\n📈 Total Computers articles: {total_computers}")
    print(f"🎯 Grand Total: {total} articles")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(seed_more_computers())
