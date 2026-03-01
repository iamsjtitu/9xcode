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

# ============================================================
# MASTER SEEDER - ALL CATEGORIES
# ============================================================

ALL_ARTICLES = []

# ========== COMPUTERS - Windows Articles ==========
COMPUTERS_WINDOWS = [
    {
        'title': 'Windows 11 Clean Installation Guide',
        'description': 'Step-by-step guide to perform a clean installation of Windows 11 from USB bootable drive.',
        'category': 'computers',
        'subcategory': 'windows',
        'os': ['windows'],
        'difficulty': 'beginner',
        'tags': ['windows-11', 'installation', 'clean-install', 'usb-boot'],
        'steps': [
            {'title': 'Create Bootable USB', 'description': 'Download Windows 11 Media Creation Tool and create bootable USB.', 'code': '1. Download Media Creation Tool from microsoft.com\n2. Run the tool as Administrator\n3. Select "Create installation media"\n4. Choose USB flash drive (8GB minimum)\n5. Wait for download and creation to complete', 'language': 'bash'},
            {'title': 'Boot from USB', 'description': 'Configure BIOS to boot from USB drive.', 'code': '1. Insert USB and restart PC\n2. Press F2/F12/DEL to enter BIOS\n3. Go to Boot Menu\n4. Set USB as first boot device\n5. Save and Exit (F10)', 'language': 'bash'},
            {'title': 'Install Windows', 'description': 'Follow the installation wizard.', 'code': '1. Select Language, Time, Keyboard\n2. Click "Install Now"\n3. Enter product key or skip\n4. Select Windows 11 edition\n5. Accept license terms\n6. Choose "Custom: Install Windows only"\n7. Delete all partitions (for clean install)\n8. Select unallocated space → Next\n9. Wait for installation to complete', 'language': 'bash'},
            {'title': 'Initial Setup', 'description': 'Complete Windows 11 setup.', 'code': '1. Select your region\n2. Choose keyboard layout\n3. Connect to WiFi/Network\n4. Sign in with Microsoft account (or create local account)\n5. Set PIN\n6. Configure privacy settings\n7. Windows 11 is ready!', 'language': 'bash'}
        ],
        'postInstallation': {'title': 'Post Installation', 'content': 'Install latest Windows Updates, install drivers from manufacturer website, install essential software like browser, antivirus, and office suite.'}
    },
    {
        'title': 'Windows Defender Firewall Configuration',
        'description': 'Configure Windows Defender Firewall rules to allow or block specific applications and ports.',
        'category': 'computers',
        'subcategory': 'windows',
        'os': ['windows'],
        'difficulty': 'intermediate',
        'tags': ['windows', 'firewall', 'security', 'defender'],
        'steps': [
            {'title': 'Open Firewall Settings', 'description': 'Access Windows Defender Firewall.', 'code': '1. Press Windows + R\n2. Type: firewall.cpl\n3. Click OK\n\nOR\n\nSettings → Privacy & Security → Windows Security → Firewall', 'language': 'bash'},
            {'title': 'Allow App Through Firewall', 'description': 'Add application exception.', 'code': '1. Click "Allow an app or feature through Windows Defender Firewall"\n2. Click "Change settings"\n3. Click "Allow another app"\n4. Browse and select application\n5. Check Private and/or Public\n6. Click OK', 'language': 'bash'},
            {'title': 'Create Inbound Rule', 'description': 'Create custom inbound firewall rule.', 'code': '1. Click "Advanced settings"\n2. Select "Inbound Rules"\n3. Click "New Rule" (right panel)\n4. Select Rule Type:\n   - Program (for specific app)\n   - Port (for specific port)\n5. Specify program path or port number\n6. Allow or Block the connection\n7. Choose profile (Domain/Private/Public)\n8. Name the rule\n9. Click Finish', 'language': 'bash'},
            {'title': 'Block Specific Port', 'description': 'Create rule to block a port.', 'code': 'Example: Block Port 23 (Telnet)\n\n1. New Rule → Port\n2. TCP, Specific port: 23\n3. Block the connection\n4. Apply to all profiles\n5. Name: "Block Telnet Port 23"\n6. Finish', 'language': 'bash'}
        ],
        'postInstallation': {'title': 'Testing', 'content': 'Test firewall rules using telnet or PowerShell Test-NetConnection command. Monitor blocked connections in Windows Event Viewer.'}
    },
    {
        'title': 'Windows CMD Useful Commands Cheatsheet',
        'description': 'Essential Windows Command Prompt commands for system administration and troubleshooting.',
        'category': 'computers',
        'subcategory': 'windows',
        'os': ['windows'],
        'difficulty': 'beginner',
        'tags': ['windows', 'cmd', 'command-prompt', 'commands', 'cheatsheet'],
        'steps': [
            {'title': 'System Information Commands', 'description': 'Get system details.', 'code': '# System info\nsysteminfo\n\n# Computer name\nhostname\n\n# Current user\nwhoami\n\n# IP configuration\nipconfig /all\n\n# Check Windows version\nwinver', 'language': 'bash'},
            {'title': 'Network Commands', 'description': 'Network troubleshooting commands.', 'code': '# Ping a host\nping google.com\n\n# Trace route\ntracert google.com\n\n# DNS lookup\nnslookup google.com\n\n# Flush DNS cache\nipconfig /flushdns\n\n# Release IP\nipconfig /release\n\n# Renew IP\nipconfig /renew\n\n# Show network connections\nnetstat -an', 'language': 'bash'},
            {'title': 'File Operations', 'description': 'File and folder commands.', 'code': '# List files\ndir\n\n# Change directory\ncd foldername\n\n# Go to parent directory\ncd ..\n\n# Create folder\nmkdir newfolder\n\n# Copy file\ncopy source.txt destination.txt\n\n# Move file\nmove source.txt destination\\\n\n# Delete file\ndel filename.txt\n\n# Delete folder\nrmdir /s foldername', 'language': 'bash'},
            {'title': 'System Management', 'description': 'System administration commands.', 'code': '# Task list\ntasklist\n\n# Kill process\ntaskkill /IM processname.exe /F\n\n# Shutdown PC\nshutdown /s /t 0\n\n# Restart PC\nshutdown /r /t 0\n\n# Check disk\nchkdsk C: /f\n\n# System file checker\nsfc /scannow\n\n# Clear screen\ncls', 'language': 'bash'}
        ],
        'postInstallation': {'title': 'Pro Tip', 'content': 'Run Command Prompt as Administrator for system-level commands. Use Tab key for auto-completion. Use Up/Down arrows to navigate command history.'}
    },
    {
        'title': 'Windows Remote Desktop Setup and Configuration',
        'description': 'Enable and configure Remote Desktop Protocol (RDP) for remote access to Windows PC.',
        'category': 'computers',
        'subcategory': 'windows',
        'os': ['windows'],
        'difficulty': 'intermediate',
        'tags': ['windows', 'rdp', 'remote-desktop', 'remote-access'],
        'steps': [
            {'title': 'Enable Remote Desktop', 'description': 'Turn on Remote Desktop feature.', 'code': '1. Settings → System → Remote Desktop\n2. Toggle "Remote Desktop" to ON\n3. Click "Confirm"\n4. Note your PC name shown\n\nOR via System Properties:\n1. Right-click This PC → Properties\n2. Remote settings\n3. Check "Allow remote connections"', 'language': 'bash'},
            {'title': 'Configure Firewall', 'description': 'Ensure RDP port is allowed.', 'code': 'RDP uses port 3389\n\nCheck if allowed:\n1. Control Panel → Windows Defender Firewall\n2. Allow an app through firewall\n3. Ensure "Remote Desktop" is checked\n   for Private and/or Public networks', 'language': 'bash'},
            {'title': 'Add Remote Users', 'description': 'Allow specific users to connect remotely.', 'code': '1. Settings → System → Remote Desktop\n2. Click "Select users that can remotely access this PC"\n3. Click "Add"\n4. Enter username\n5. Click "Check Names" → OK\n\nNote: Administrators have access by default', 'language': 'bash'},
            {'title': 'Connect from Another PC', 'description': 'Use Remote Desktop Connection client.', 'code': 'On client PC:\n1. Press Windows + R\n2. Type: mstsc\n3. Enter computer name or IP address\n4. Click "Connect"\n5. Enter username and password\n6. Click OK\n\nFor better performance:\n- Show Options → Display → Lower resolution\n- Experience → Choose connection speed', 'language': 'bash'}
        ],
        'postInstallation': {'title': 'Security Tips', 'content': 'Change default RDP port (3389) for security. Use strong passwords. Enable Network Level Authentication (NLA). Consider using VPN for remote access over internet.'}
    },
    {
        'title': 'Windows Disk Partition Management',
        'description': 'Create, resize, and manage disk partitions using Windows Disk Management tool.',
        'category': 'computers',
        'subcategory': 'windows',
        'os': ['windows'],
        'difficulty': 'intermediate',
        'tags': ['windows', 'disk', 'partition', 'storage', 'management'],
        'steps': [
            {'title': 'Open Disk Management', 'description': 'Access the Disk Management tool.', 'code': 'Method 1:\n1. Right-click Start button\n2. Select "Disk Management"\n\nMethod 2:\n1. Press Windows + R\n2. Type: diskmgmt.msc\n3. Press Enter\n\nMethod 3:\n1. Search "Create and format hard disk partitions"', 'language': 'bash'},
            {'title': 'Shrink Partition', 'description': 'Reduce partition size to create free space.', 'code': '1. Right-click on partition to shrink\n2. Select "Shrink Volume"\n3. Enter amount to shrink (in MB)\n4. Click "Shrink"\n5. Unallocated space will appear\n\nNote: You cannot shrink beyond\nimmovable files location', 'language': 'bash'},
            {'title': 'Create New Partition', 'description': 'Create partition from unallocated space.', 'code': '1. Right-click on "Unallocated" space\n2. Select "New Simple Volume"\n3. Click Next\n4. Specify volume size → Next\n5. Assign drive letter → Next\n6. Format options:\n   - File System: NTFS\n   - Volume Label: Data\n   - Quick Format: Yes\n7. Click Next → Finish', 'language': 'bash'},
            {'title': 'Extend Partition', 'description': 'Increase partition size using adjacent unallocated space.', 'code': '1. Right-click partition to extend\n2. Select "Extend Volume"\n3. Click Next\n4. Select available space\n5. Specify amount to add\n6. Click Next → Finish\n\nNote: Unallocated space must be\nimmediately to the RIGHT of partition', 'language': 'bash'}
        ],
        'postInstallation': {'title': 'Important', 'content': 'Always backup important data before modifying partitions. System partition (C:) cannot be deleted while Windows is running. Use third-party tools like MiniTool Partition Wizard for advanced operations.'}
    }
]

# ========== COMPUTERS - Mac Articles ==========
COMPUTERS_MAC = [
    {
        'title': 'macOS Terminal Essential Commands',
        'description': 'Essential Terminal commands for macOS users for file management, system info, and administration.',
        'category': 'computers',
        'subcategory': 'mac',
        'os': ['mac'],
        'difficulty': 'beginner',
        'tags': ['macos', 'terminal', 'commands', 'bash', 'zsh'],
        'steps': [
            {'title': 'File Navigation', 'description': 'Navigate through files and folders.', 'code': '# Print working directory\npwd\n\n# List files\nls\nls -la  # detailed with hidden files\n\n# Change directory\ncd ~/Documents\ncd ..  # parent directory\ncd -   # previous directory\n\n# Open current folder in Finder\nopen .', 'language': 'bash'},
            {'title': 'File Operations', 'description': 'Create, copy, move, delete files.', 'code': '# Create file\ntouch filename.txt\n\n# Create directory\nmkdir newfolder\n\n# Copy file\ncp source.txt destination.txt\n\n# Move/rename\nmv oldname.txt newname.txt\n\n# Delete file\nrm filename.txt\n\n# Delete folder\nrm -rf foldername', 'language': 'bash'},
            {'title': 'System Information', 'description': 'Get system details.', 'code': '# macOS version\nsw_vers\n\n# System info\nsystem_profiler SPSoftwareDataType\n\n# Disk usage\ndf -h\n\n# Memory info\ntop -l 1 | head -n 10\n\n# CPU info\nsysctl -n machdep.cpu.brand_string', 'language': 'bash'},
            {'title': 'Network Commands', 'description': 'Network diagnostics and configuration.', 'code': '# IP address\nifconfig | grep inet\n\n# Ping\nping -c 4 google.com\n\n# DNS lookup\nnslookup google.com\n\n# Flush DNS cache\nsudo dscacheutil -flushcache\nsudo killall -HUP mDNSResponder\n\n# List network interfaces\nnetworksetup -listallhardwareports', 'language': 'bash'}
        ],
        'postInstallation': {'title': 'Tips', 'content': 'Use Tab for auto-completion. Use Up arrow for command history. Customize terminal with Oh My Zsh. Use Homebrew (brew) for package management.'}
    },
    {
        'title': 'Install Homebrew Package Manager on macOS',
        'description': 'Install and use Homebrew - the missing package manager for macOS.',
        'category': 'computers',
        'subcategory': 'mac',
        'os': ['mac'],
        'difficulty': 'beginner',
        'tags': ['macos', 'homebrew', 'brew', 'package-manager'],
        'steps': [
            {'title': 'Install Homebrew', 'description': 'Run the installation script.', 'code': '/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"\n\n# Follow the prompts\n# Enter your password when asked', 'language': 'bash'},
            {'title': 'Add to PATH (Apple Silicon)', 'description': 'For M1/M2/M3 Macs, add Homebrew to PATH.', 'code': '# Add to .zprofile\necho \'eval "$(/opt/homebrew/bin/brew shellenv)"\' >> ~/.zprofile\neval "$(/opt/homebrew/bin/brew shellenv)"\n\n# Verify installation\nbrew --version', 'language': 'bash'},
            {'title': 'Basic Homebrew Commands', 'description': 'Common brew commands.', 'code': '# Update Homebrew\nbrew update\n\n# Search for package\nbrew search wget\n\n# Install package\nbrew install wget\n\n# List installed packages\nbrew list\n\n# Uninstall package\nbrew uninstall wget\n\n# Upgrade all packages\nbrew upgrade', 'language': 'bash'},
            {'title': 'Install GUI Applications', 'description': 'Use brew cask for GUI apps.', 'code': '# Install GUI apps with --cask\nbrew install --cask google-chrome\nbrew install --cask visual-studio-code\nbrew install --cask vlc\nbrew install --cask slack\n\n# List installed casks\nbrew list --cask', 'language': 'bash'}
        ],
        'postInstallation': {'title': 'Popular Packages', 'content': 'Common packages: git, node, python, wget, htop, tree. Common casks: google-chrome, firefox, visual-studio-code, iterm2, rectangle.'}
    },
    {
        'title': 'macOS System Preferences Configuration',
        'description': 'Essential macOS System Preferences settings for productivity and customization.',
        'category': 'computers',
        'subcategory': 'mac',
        'os': ['mac'],
        'difficulty': 'beginner',
        'tags': ['macos', 'settings', 'preferences', 'customization'],
        'steps': [
            {'title': 'Trackpad Gestures', 'description': 'Configure trackpad gestures.', 'code': 'System Preferences → Trackpad\n\nPoint & Click:\n- Tap to click: Enable\n- Secondary click: Two finger tap\n- Look up: Three finger tap\n\nScroll & Zoom:\n- Scroll direction: Natural (or disable)\n- Zoom in/out: Pinch\n\nMore Gestures:\n- Swipe between pages\n- Mission Control: Swipe up with 4 fingers\n- App Expose: Swipe down with 4 fingers', 'language': 'bash'},
            {'title': 'Hot Corners', 'description': 'Set up hot corners for quick actions.', 'code': 'System Preferences → Desktop & Screen Saver\n→ Screen Saver → Hot Corners\n\nRecommended Setup:\n- Top Left: Mission Control\n- Top Right: Desktop\n- Bottom Left: Start Screen Saver\n- Bottom Right: Lock Screen\n\nHold modifier key to prevent accidental trigger', 'language': 'bash'},
            {'title': 'Dock Settings', 'description': 'Customize Dock appearance and behavior.', 'code': 'System Preferences → Dock & Menu Bar\n\n- Size: Adjust slider\n- Magnification: Enable/adjust\n- Position: Left/Bottom/Right\n- Minimize windows using: Scale effect\n- Automatically hide and show Dock: Enable\n- Show recent applications: Disable\n\nTerminal tweaks:\n# Add spacer to Dock\ndefaults write com.apple.dock persistent-apps -array-add \'{"tile-type"="spacer-tile";}\'\nkillall Dock', 'language': 'bash'},
            {'title': 'Keyboard Shortcuts', 'description': 'Customize keyboard shortcuts.', 'code': 'System Preferences → Keyboard → Shortcuts\n\nUseful shortcuts to customize:\n- Screenshots: Custom keys\n- Spotlight: Cmd + Space\n- Input Sources: Cmd + Space (or other)\n\nApp Shortcuts:\n- Add custom shortcuts for any menu item\n- Click + → Select app → Enter menu title\n- Assign keyboard shortcut', 'language': 'bash'}
        ],
        'postInstallation': {'title': 'Pro Tips', 'content': 'Use Cmd+Space for Spotlight search. Enable three-finger drag in Accessibility settings. Use Rectangle app for window management.'}
    }
]

# ========== LEARNING - Tally Articles ==========
LEARNING_TALLY = [
    {
        'title': 'Tally Prime Installation Guide',
        'description': 'Complete guide to download and install Tally Prime on Windows PC.',
        'category': 'learning',
        'subcategory': 'tally',
        'os': ['windows'],
        'difficulty': 'beginner',
        'tags': ['tally', 'tally-prime', 'installation', 'accounting'],
        'steps': [
            {'title': 'Download Tally Prime', 'description': 'Get Tally Prime from official website.', 'code': '1. Visit: https://tallysolutions.com/download/\n2. Click "Download Tally Prime"\n3. Fill registration form (optional)\n4. Download will start automatically\n5. File: TallyPrime_Setup.exe (approx 150MB)', 'language': 'bash'},
            {'title': 'System Requirements', 'description': 'Check minimum requirements.', 'code': 'Minimum Requirements:\n- OS: Windows 7/8/10/11\n- Processor: Dual Core or higher\n- RAM: 4 GB minimum (8GB recommended)\n- Storage: 150 MB free space\n- Screen: 1366 x 768 resolution\n- .NET Framework 4.5 or higher', 'language': 'bash'},
            {'title': 'Install Tally Prime', 'description': 'Run the installer.', 'code': '1. Right-click TallyPrime_Setup.exe\n2. Run as Administrator\n3. Click "Install"\n4. Choose installation path:\n   Default: C:\\TallyPrime\n5. Click "Install"\n6. Wait for installation\n7. Click "Finish"', 'language': 'bash'},
            {'title': 'Activate License', 'description': 'Activate Tally Prime license.', 'code': 'For Licensed Users:\n1. Open Tally Prime\n2. Press F12 (Configuration)\n3. Licensing → Activate License\n4. Enter Serial Number and Key\n5. Click "Activate"\n\nFor Educational/Trial:\n1. Select "Educational Mode"\n2. Or start 7-day trial', 'language': 'bash'}
        ],
        'postInstallation': {'title': 'Getting Started', 'content': 'Create your first company: Gateway → Create Company. Learn basic shortcuts: F1 (Select), F2 (Date), F4 (Contra), F5 (Payment), F6 (Receipt), F7 (Journal).'}
    },
    {
        'title': 'Tally Prime Create New Company',
        'description': 'Step-by-step guide to create a new company in Tally Prime with GST configuration.',
        'category': 'learning',
        'subcategory': 'tally',
        'os': ['windows'],
        'difficulty': 'beginner',
        'tags': ['tally', 'company-creation', 'gst', 'accounting'],
        'steps': [
            {'title': 'Start Company Creation', 'description': 'Navigate to create company option.', 'code': 'From Gateway of Tally:\n1. Press Alt + F3 (Company Info)\n2. Select "Create Company"\n\nOR\n\n1. Gateway → Company Info\n2. Create Company', 'language': 'bash'},
            {'title': 'Enter Company Details', 'description': 'Fill basic company information.', 'code': 'Company Details:\n- Name: Your Company Name\n- Mailing Name: Same or different\n- Address: Company address\n- Country: India\n- State: Your state\n- PIN Code: Your PIN\n- Phone: Contact number\n- Email: company@email.com\n- Website: www.company.com', 'language': 'bash'},
            {'title': 'Financial Year Settings', 'description': 'Set financial year and books date.', 'code': 'Financial Year:\n- Financial Year From: 1-Apr-2024\n- Books Beginning From: 1-Apr-2024\n\nSecurity:\n- Use Security Control: Yes (optional)\n- Tally Vault Password: Set if needed', 'language': 'bash'},
            {'title': 'Enable GST', 'description': 'Configure GST settings.', 'code': 'Statutory Compliance:\n- Enable GST: Yes\n- State: Your state\n- GST Registration Type: Regular\n- GSTIN: Your 15-digit GSTIN\n- Applicable From: Date\n\nOther Options:\n- Enable TDS: As required\n- Enable TCS: As required', 'language': 'bash'}
        ],
        'postInstallation': {'title': 'Next Steps', 'content': 'Create Ledgers (F12 → Accounts Info → Ledgers → Create). Set up inventory if needed. Configure voucher types as per requirement.'}
    },
    {
        'title': 'Tally Prime Keyboard Shortcuts',
        'description': 'Essential keyboard shortcuts for fast and efficient work in Tally Prime.',
        'category': 'learning',
        'subcategory': 'tally',
        'os': ['windows'],
        'difficulty': 'beginner',
        'tags': ['tally', 'shortcuts', 'keyboard', 'productivity'],
        'steps': [
            {'title': 'Navigation Shortcuts', 'description': 'Move around Tally quickly.', 'code': 'Navigation:\nEsc      - Go back / Exit\nEnter    - Accept / Select\nF1       - Select company\nF2       - Change date\nF3       - Change company\nF11      - Features\nF12      - Configuration\n\nAlt+F3   - Company Info\nCtrl+F3  - Shutdown company', 'language': 'bash'},
            {'title': 'Voucher Entry Shortcuts', 'description': 'Quick voucher creation.', 'code': 'Voucher Types:\nF4  - Contra\nF5  - Payment\nF6  - Receipt\nF7  - Journal\nF8  - Sales\nF9  - Purchase\n\nAlt+F5  - Payment with check mode\nAlt+F6  - Receipt with check mode\n\nCtrl+F8  - Credit Note\nCtrl+F9  - Debit Note', 'language': 'bash'},
            {'title': 'Report Shortcuts', 'description': 'Access reports quickly.', 'code': 'Reports:\nAlt+F1  - Detailed view\nAlt+F2  - Period change\nAlt+F5  - Sales Register\nAlt+F6  - Purchase Register\nAlt+F7  - Stock Summary\n\nB       - Balance Sheet\nP       - Profit & Loss\nD       - Day Book\nT       - Trial Balance', 'language': 'bash'},
            {'title': 'Data Entry Shortcuts', 'description': 'Speed up data entry.', 'code': 'Data Entry:\nCtrl+A     - Accept/Save\nCtrl+Q     - Quit without saving\nAlt+D      - Delete voucher\nAlt+2      - Duplicate entry\nAlt+C      - Create master\nAlt+S      - Alter master\n\nSpacebar   - Toggle Yes/No\nPage Up    - Previous voucher\nPage Down  - Next voucher', 'language': 'bash'}
        ],
        'postInstallation': {'title': 'Practice Tip', 'content': 'Practice using shortcuts daily. Start with F4-F9 for vouchers. Use Ctrl+A to save instead of mouse. Speed will improve with regular use.'}
    },
    {
        'title': 'Tally Prime GST Return Filing Preparation',
        'description': 'Prepare GSTR-1 and GSTR-3B reports in Tally Prime for GST return filing.',
        'category': 'learning',
        'subcategory': 'tally',
        'os': ['windows'],
        'difficulty': 'intermediate',
        'tags': ['tally', 'gst', 'gstr-1', 'gstr-3b', 'tax'],
        'steps': [
            {'title': 'Verify GST Configuration', 'description': 'Check GST is properly configured.', 'code': 'Gateway → F11 (Features) → F1 (Statutory)\n\nVerify:\n- Enable GST: Yes\n- Set/Alter GST Details: Yes\n\nCheck Company GST Details:\n- GSTIN: Correct 15-digit number\n- Registration Type: Regular\n- Applicable From: Correct date', 'language': 'bash'},
            {'title': 'Check Ledger GST Details', 'description': 'Ensure party ledgers have GST info.', 'code': 'Gateway → Masters → Accounts Info → Ledgers\n\nFor each Party Ledger:\n- Registration Type: Regular/Composition/Unregistered\n- GSTIN: Enter for registered parties\n- State: Mandatory for GST calculation\n\nFor Stock Items:\n- Set HSN/SAC code\n- Set GST Rate (5%, 12%, 18%, 28%)', 'language': 'bash'},
            {'title': 'View GSTR-1 Report', 'description': 'Generate GSTR-1 report.', 'code': 'Gateway → Display More Reports → \nStatutory Reports → GST Reports → GSTR-1\n\nSections in GSTR-1:\n- B2B Invoices (to registered dealers)\n- B2C Large (to consumers > ₹2.5L)\n- B2C Small (to consumers < ₹2.5L)\n- Credit/Debit Notes\n- HSN Summary\n- Document Summary', 'language': 'bash'},
            {'title': 'Export for Filing', 'description': 'Export GST reports for filing.', 'code': 'Export GSTR-1:\n1. Open GSTR-1 report\n2. Press E (Export)\n3. Select format: JSON / Excel\n4. Save file\n\nFor GSTR-3B:\nGateway → Display → Statutory Reports → \nGST Reports → GSTR-3B\n\nThis shows:\n- Outward supplies\n- Inward supplies (reverse charge)\n- ITC eligible\n- Tax payable', 'language': 'bash'}
        ],
        'postInstallation': {'title': 'Before Filing', 'content': 'Reconcile sales with GSTR-1. Match ITC with GSTR-2B. Verify tax calculations. Check for any error in reports (shown in red). Export and upload to GST portal.'}
    }
]

# ========== LEARNING - MS Office Articles ==========
LEARNING_MSOFFICE = [
    {
        'title': 'Microsoft Excel Essential Formulas',
        'description': 'Most commonly used Excel formulas and functions with examples.',
        'category': 'learning',
        'subcategory': 'ms-office',
        'os': ['windows', 'mac'],
        'difficulty': 'beginner',
        'tags': ['excel', 'ms-office', 'formulas', 'functions'],
        'steps': [
            {'title': 'Basic Math Functions', 'description': 'SUM, AVERAGE, COUNT and more.', 'code': '=SUM(A1:A10)\nAdds all numbers in range A1 to A10\n\n=AVERAGE(A1:A10)\nCalculates average of numbers\n\n=COUNT(A1:A10)\nCounts cells with numbers\n\n=COUNTA(A1:A10)\nCounts non-empty cells\n\n=MAX(A1:A10)\nReturns highest value\n\n=MIN(A1:A10)\nReturns lowest value', 'language': 'bash'},
            {'title': 'IF and Logical Functions', 'description': 'Conditional formulas.', 'code': '=IF(A1>100, "High", "Low")\nIf A1 > 100, show "High", else "Low"\n\n=IF(A1>=90, "A", IF(A1>=80, "B", "C"))\nNested IF for grades\n\n=AND(A1>0, B1>0)\nReturns TRUE if both conditions met\n\n=OR(A1>100, B1>100)\nReturns TRUE if any condition met\n\n=IFS(A1>=90,"A", A1>=80,"B", A1>=70,"C", TRUE,"D")\nMultiple conditions (Excel 2019+)', 'language': 'bash'},
            {'title': 'Lookup Functions', 'description': 'VLOOKUP, HLOOKUP, INDEX-MATCH.', 'code': '=VLOOKUP(lookup_value, table, col_num, FALSE)\nExample: =VLOOKUP(A1, $D$1:$E$100, 2, FALSE)\n\n=HLOOKUP(lookup_value, table, row_num, FALSE)\nFor horizontal lookup\n\n=INDEX(B1:B100, MATCH(A1, A1:A100, 0))\nMore flexible than VLOOKUP\n\n=XLOOKUP(A1, D:D, E:E)\nModern replacement (Excel 365)', 'language': 'bash'},
            {'title': 'Text Functions', 'description': 'Manipulate text data.', 'code': '=CONCATENATE(A1, " ", B1)\nJoin text from cells\n\n=CONCAT(A1, " ", B1)\nModern version\n\n=LEFT(A1, 5)\nFirst 5 characters\n\n=RIGHT(A1, 5)\nLast 5 characters\n\n=MID(A1, 2, 5)\n5 characters starting from position 2\n\n=TRIM(A1)\nRemove extra spaces\n\n=UPPER(A1) / =LOWER(A1)\nChange case', 'language': 'bash'}
        ],
        'postInstallation': {'title': 'Pro Tip', 'content': 'Press F4 to toggle absolute references ($). Use Ctrl+` to show formulas. Use Formula Auditing to trace errors. Learn keyboard shortcuts for faster work.'}
    },
    {
        'title': 'Microsoft Word Formatting Tips',
        'description': 'Professional document formatting techniques in Microsoft Word.',
        'category': 'learning',
        'subcategory': 'ms-office',
        'os': ['windows', 'mac'],
        'difficulty': 'beginner',
        'tags': ['word', 'ms-office', 'formatting', 'document'],
        'steps': [
            {'title': 'Essential Keyboard Shortcuts', 'description': 'Format text quickly.', 'code': 'Text Formatting:\nCtrl + B    Bold\nCtrl + I    Italic\nCtrl + U    Underline\nCtrl + E    Center align\nCtrl + L    Left align\nCtrl + R    Right align\nCtrl + J    Justify\n\nParagraph:\nCtrl + 1    Single spacing\nCtrl + 2    Double spacing\nCtrl + 5    1.5 line spacing', 'language': 'bash'},
            {'title': 'Styles and Headings', 'description': 'Use styles for consistent formatting.', 'code': 'Apply Heading Styles:\n1. Select text\n2. Home → Styles group\n3. Choose Heading 1, 2, or 3\n\nBenefits of using Styles:\n- Automatic Table of Contents\n- Navigation Pane support\n- Consistent formatting\n- Easy global changes\n\nModify Style:\n- Right-click style → Modify\n- Change font, size, color\n- Apply to entire document', 'language': 'bash'},
            {'title': 'Page Setup', 'description': 'Configure page layout.', 'code': 'Layout Tab → Page Setup:\n\nMargins:\n- Normal: 1" all sides\n- Narrow: 0.5" all sides\n- Custom: Set your own\n\nOrientation:\n- Portrait (vertical)\n- Landscape (horizontal)\n\nSize:\n- A4 (most common)\n- Letter\n- Legal\n- Custom size\n\nColumns:\n- One, Two, Three columns\n- Custom column widths', 'language': 'bash'},
            {'title': 'Headers, Footers, Page Numbers', 'description': 'Add document headers and footers.', 'code': 'Insert → Header & Footer:\n\nHeader:\n1. Double-click top margin\n2. Type header text\n3. Use Quick Parts for auto-text\n\nPage Numbers:\n1. Insert → Page Number\n2. Choose position (Top/Bottom)\n3. Choose style\n\nDifferent First Page:\n- Check "Different First Page"\n- First page can be blank\n\nClose: Double-click document area', 'language': 'bash'}
        ],
        'postInstallation': {'title': 'Professional Tips', 'content': 'Always use Styles instead of manual formatting. Use Section Breaks for different layouts in same document. Enable Navigation Pane (View tab) for easy movement.'}
    },
    {
        'title': 'Microsoft PowerPoint Presentation Tips',
        'description': 'Create professional presentations with PowerPoint tips and tricks.',
        'category': 'learning',
        'subcategory': 'ms-office',
        'os': ['windows', 'mac'],
        'difficulty': 'beginner',
        'tags': ['powerpoint', 'ms-office', 'presentation', 'slides'],
        'steps': [
            {'title': 'Slide Master for Consistent Design', 'description': 'Set up master slides for uniform look.', 'code': 'View → Slide Master\n\nIn Slide Master View:\n1. Edit top master for global changes\n2. Edit layouts below for specific types\n3. Change fonts, colors, backgrounds\n4. Add logo to appear on all slides\n5. Click "Close Master View"\n\nBenefits:\n- One change updates all slides\n- Consistent branding\n- Professional look', 'language': 'bash'},
            {'title': 'Keyboard Shortcuts', 'description': 'Navigate and present efficiently.', 'code': 'Editing:\nCtrl + M         New slide\nCtrl + D         Duplicate slide\nCtrl + G         Group objects\nCtrl + Shift + G Ungroup\nF5               Start slideshow\nShift + F5       Start from current slide\n\nDuring Presentation:\nN or Enter       Next slide\nP or Backspace   Previous slide\nNumber + Enter   Go to slide number\nB                Black screen\nW                White screen\nEsc              End show', 'language': 'bash'},
            {'title': 'Animations and Transitions', 'description': 'Add subtle animations.', 'code': 'Transitions (between slides):\n1. Select slide\n2. Transitions tab\n3. Choose effect (Fade recommended)\n4. Duration: 0.5-1 second\n5. Apply to All (if uniform needed)\n\nAnimations (within slide):\n1. Select object\n2. Animations tab\n3. Choose effect:\n   - Entrance: Fade, Appear\n   - Emphasis: Pulse, Grow\n   - Exit: Fade, Disappear\n4. Use Animation Pane for order', 'language': 'bash'},
            {'title': 'Design Tips', 'description': 'Create visually appealing slides.', 'code': 'Design Principles:\n\n1. Less is More:\n   - Maximum 6 lines per slide\n   - Maximum 6 words per line\n   - One idea per slide\n\n2. Visual Hierarchy:\n   - Title: 28-36pt\n   - Body: 18-24pt\n   - Minimum: 18pt\n\n3. Color:\n   - Maximum 3-4 colors\n   - High contrast for readability\n   - Consistent palette\n\n4. Images:\n   - High resolution\n   - Relevant to content\n   - Avoid clipart', 'language': 'bash'}
        ],
        'postInstallation': {'title': 'Presenter Tips', 'content': 'Use Presenter View (shows notes on your screen). Rehearse timings with Rehearse Timings feature. Export to PDF for sharing. Use PowerPoint Designer for AI suggestions.'}
    }
]

# ========== LEARNING - Busy Software ==========
LEARNING_BUSY = [
    {
        'title': 'Busy Accounting Software Installation',
        'description': 'Install and setup Busy accounting software on Windows.',
        'category': 'learning',
        'subcategory': 'busy',
        'os': ['windows'],
        'difficulty': 'beginner',
        'tags': ['busy', 'accounting', 'installation', 'software'],
        'steps': [
            {'title': 'Download Busy Software', 'description': 'Get Busy from official website.', 'code': '1. Visit: https://busy.in/download\n2. Select version:\n   - Busy 21 (Latest)\n   - Basic / Standard / Enterprise\n3. Click Download\n4. File size: ~100MB', 'language': 'bash'},
            {'title': 'Install Busy', 'description': 'Run installation wizard.', 'code': '1. Run BusySetup.exe as Administrator\n2. Accept License Agreement\n3. Choose installation path\n   Default: C:\\Busy21\n4. Select components:\n   - Busy Application\n   - Sample Company\n   - Help Files\n5. Click Install\n6. Wait for completion\n7. Finish', 'language': 'bash'},
            {'title': 'First Time Setup', 'description': 'Configure Busy on first launch.', 'code': '1. Launch Busy 21\n2. Enter your details:\n   - Name\n   - Company Name\n   - Email\n   - Phone\n3. Choose Data Directory:\n   Default: C:\\BusyWin\\Data\n4. Click OK', 'language': 'bash'},
            {'title': 'Activate License', 'description': 'Activate your Busy license.', 'code': 'For Licensed Users:\n1. Administration → Company Setup\n2. Enter License Key\n3. Click Activate\n\nFor Trial:\n1. Select "Trial Version"\n2. 30-day trial with full features\n\nOnline Activation:\n1. Help → Activate License\n2. Enter Serial Number\n3. Click "Online Activation"', 'language': 'bash'}
        ],
        'postInstallation': {'title': 'Next Steps', 'content': 'Create company: Administration → Company → New. Configure GST: Administration → Configuration → Statutory. Set financial year and start entering transactions.'}
    },
    {
        'title': 'Busy Software Create Company and Masters',
        'description': 'Create new company and set up account masters in Busy software.',
        'category': 'learning',
        'subcategory': 'busy',
        'os': ['windows'],
        'difficulty': 'beginner',
        'tags': ['busy', 'company-setup', 'masters', 'accounting'],
        'steps': [
            {'title': 'Create New Company', 'description': 'Set up a new company.', 'code': 'Administration → Company → New\n\nCompany Details:\n- Company Name: Your Company Ltd\n- Short Name: YCL (for quick access)\n- Address: Full address\n- City, State, PIN\n- Phone, Email\n\nFinancial Year:\n- From: 01-Apr-2024\n- To: 31-Mar-2025\n- Books Beginning: 01-Apr-2024', 'language': 'bash'},
            {'title': 'Configure GST', 'description': 'Enable and configure GST.', 'code': 'Administration → Configuration → Statutory\n\nGST Configuration:\n- Enable GST: Yes\n- GSTIN: Your 15-digit GSTIN\n- Registration Type: Regular\n- State: Your state\n- HSN/SAC: Enable\n\nTax Rates:\n- Configure GST rates (5%, 12%, 18%, 28%)\n- Set default tax category', 'language': 'bash'},
            {'title': 'Create Account Masters', 'description': 'Set up ledger accounts.', 'code': 'Administration → Masters → Accounts\n\nCreate Accounts:\n1. Click "Add" or press F3\n2. Enter Account Name\n3. Select Group:\n   - Sundry Debtors (Customers)\n   - Sundry Creditors (Suppliers)\n   - Bank Accounts\n   - Cash\n   - Expenses\n   - Income\n4. Enter Opening Balance (if any)\n5. For Parties: Enter GSTIN, State\n6. Save (Ctrl+S)', 'language': 'bash'},
            {'title': 'Create Item Masters', 'description': 'Set up inventory items.', 'code': 'Administration → Masters → Items\n\n1. Click Add (F3)\n2. Enter Item Details:\n   - Item Name\n   - Item Code\n   - Unit of Measure\n   - Item Group/Category\n3. Tax Details:\n   - HSN Code\n   - GST Rate\n4. Stock Details:\n   - Opening Qty\n   - Opening Rate\n5. Save (Ctrl+S)', 'language': 'bash'}
        ],
        'postInstallation': {'title': 'Important', 'content': 'Create all masters before starting transactions. Set up account groups for better organization. Configure default tax rates to speed up entry.'}
    }
]

# ========== LEARNING - Adobe Photoshop ==========
LEARNING_PHOTOSHOP = [
    {
        'title': 'Adobe Photoshop Keyboard Shortcuts',
        'description': 'Essential Photoshop keyboard shortcuts for faster editing workflow.',
        'category': 'learning',
        'subcategory': 'adobe-photoshop',
        'os': ['windows', 'mac'],
        'difficulty': 'beginner',
        'tags': ['photoshop', 'adobe', 'shortcuts', 'editing'],
        'steps': [
            {'title': 'Tool Shortcuts', 'description': 'Quick access to common tools.', 'code': 'Selection Tools:\nV - Move Tool\nM - Marquee Tool\nL - Lasso Tool\nW - Magic Wand / Quick Selection\n\nEditing Tools:\nC - Crop Tool\nB - Brush Tool\nE - Eraser Tool\nG - Gradient / Paint Bucket\nS - Clone Stamp\nJ - Healing Brush\nT - Type Tool\n\nNavigation:\nZ - Zoom Tool\nH - Hand Tool\nSpacebar - Temporary Hand Tool', 'language': 'bash'},
            {'title': 'File Operations', 'description': 'File and document shortcuts.', 'code': 'Windows / Mac:\nCtrl/Cmd + N     New Document\nCtrl/Cmd + O     Open File\nCtrl/Cmd + S     Save\nCtrl/Cmd + Shift + S  Save As\nCtrl/Cmd + Alt + S    Save for Web\nCtrl/Cmd + W     Close Document\nCtrl/Cmd + P     Print\n\nCtrl/Cmd + Z     Undo\nCtrl/Cmd + Shift + Z  Redo\nCtrl/Cmd + Alt + Z    Step Backward', 'language': 'bash'},
            {'title': 'Layer Operations', 'description': 'Work with layers efficiently.', 'code': 'Layers:\nCtrl/Cmd + J     Duplicate Layer\nCtrl/Cmd + Shift + N  New Layer\nCtrl/Cmd + E     Merge Down\nCtrl/Cmd + Shift + E  Merge Visible\nCtrl/Cmd + G     Group Layers\nCtrl/Cmd + [     Send Backward\nCtrl/Cmd + ]     Bring Forward\n\nLayer Visibility:\nClick Eye icon - Toggle visibility\nAlt + Click Eye  - Solo layer', 'language': 'bash'},
            {'title': 'Selection Shortcuts', 'description': 'Select and modify selections.', 'code': 'Selection:\nCtrl/Cmd + A     Select All\nCtrl/Cmd + D     Deselect\nCtrl/Cmd + Shift + I  Inverse Selection\nCtrl/Cmd + T     Free Transform\n\nWhile Selecting:\nShift + Drag     Add to selection\nAlt + Drag       Subtract from selection\nShift + Alt + Drag  Intersect selection\n\nFeather:\nShift + F6       Feather Selection', 'language': 'bash'}
        ],
        'postInstallation': {'title': 'Pro Tips', 'content': 'Use brackets [ ] to change brush size. Hold Shift while drawing for straight lines. Double-click Hand tool to fit screen. Press Tab to hide all panels.'}
    },
    {
        'title': 'Photoshop Remove Background - Multiple Methods',
        'description': 'Different ways to remove background from images in Photoshop.',
        'category': 'learning',
        'subcategory': 'adobe-photoshop',
        'os': ['windows', 'mac'],
        'difficulty': 'intermediate',
        'tags': ['photoshop', 'background-removal', 'editing', 'cutout'],
        'steps': [
            {'title': 'Method 1: Remove Background (AI)', 'description': 'One-click AI background removal.', 'code': 'Photoshop 2020 and later:\n\n1. Open image\n2. Window → Properties\n3. Under "Quick Actions"\n4. Click "Remove Background"\n5. AI automatically removes background\n6. Fine-tune with brush if needed\n\nThis creates a layer mask automatically', 'language': 'bash'},
            {'title': 'Method 2: Quick Selection Tool', 'description': 'Select subject and delete background.', 'code': '1. Select Quick Selection Tool (W)\n2. Click and drag over subject\n3. Hold Alt to subtract from selection\n4. Refine: Select → Select and Mask\n5. Adjust Edge Detection slider\n6. Output: New Layer with Mask\n\nTip: Use "Select Subject" button\nfor AI-assisted selection', 'language': 'bash'},
            {'title': 'Method 3: Pen Tool (Professional)', 'description': 'Precise path-based selection.', 'code': '1. Select Pen Tool (P)\n2. Create path around subject:\n   - Click to add anchor points\n   - Click + drag for curves\n3. Close the path\n4. Right-click → Make Selection\n5. Feather: 0-1px\n6. Inverse selection (Ctrl+Shift+I)\n7. Delete background\n\nBest for: Smooth edges, product photos', 'language': 'bash'},
            {'title': 'Method 4: Channels', 'description': 'Use channels for complex edges like hair.', 'code': '1. Window → Channels\n2. Find channel with best contrast\n3. Duplicate that channel\n4. Image → Adjustments → Levels\n5. Increase contrast (black/white)\n6. Paint to refine (black/white brush)\n7. Ctrl + Click channel = Selection\n8. Back to Layers, add mask\n\nBest for: Hair, fur, trees', 'language': 'bash'}
        ],
        'postInstallation': {'title': 'Best Practices', 'content': 'Always work on a duplicate layer. Use layer masks instead of deleting (non-destructive). For product photos, use Pen Tool. For portraits with hair, use Select and Mask with "Refine Hair" option.'}
    }
]

# ========== ROUTERS & NETWORKING ==========
ROUTERS_NETWORKING = [
    {
        'title': 'TP-Link Router Initial Setup',
        'description': 'Complete setup guide for TP-Link WiFi routers including basic configuration.',
        'category': 'networking',
        'subcategory': 'routers',
        'os': ['windows', 'mac'],
        'difficulty': 'beginner',
        'tags': ['tp-link', 'router', 'wifi', 'setup', 'networking'],
        'steps': [
            {'title': 'Physical Connection', 'description': 'Connect router hardware.', 'code': 'Connections:\n1. Connect WAN port to modem/ISP cable\n2. Power on the router\n3. Connect PC to router:\n   - Via Ethernet cable to LAN port\n   - Or connect to default WiFi\n\nDefault WiFi:\n- SSID: TP-Link_XXXX\n- Password: On router label', 'language': 'bash'},
            {'title': 'Access Router Panel', 'description': 'Login to router web interface.', 'code': 'Open browser and go to:\n- http://192.168.0.1\n- OR http://192.168.1.1\n- OR http://tplinkwifi.net\n\nFirst time setup:\n1. Create admin password\n2. Or use default:\n   - Username: admin\n   - Password: admin', 'language': 'bash'},
            {'title': 'Quick Setup Wizard', 'description': 'Configure internet connection.', 'code': 'Quick Setup:\n\n1. Time Zone: Select your zone\n\n2. Internet Connection Type:\n   - Dynamic IP (most common)\n   - Static IP (if ISP provided)\n   - PPPoE (if username/password needed)\n\n3. For PPPoE:\n   - Enter ISP username\n   - Enter ISP password\n\n4. WiFi Settings:\n   - Network Name (SSID)\n   - Password (min 8 characters)\n\n5. Click Save/Finish', 'language': 'bash'},
            {'title': 'Secure Your Router', 'description': 'Important security settings.', 'code': 'Security Settings:\n\n1. Change Admin Password:\n   Advanced → System Tools → Administration\n   Set strong password\n\n2. WiFi Security:\n   Wireless → Wireless Security\n   - Security: WPA2-PSK\n   - Encryption: AES\n   - Strong password\n\n3. Disable WPS (optional):\n   Wireless → WPS → Disable\n\n4. Update Firmware:\n   System Tools → Firmware Upgrade', 'language': 'bash'}
        ],
        'postInstallation': {'title': 'Recommended', 'content': 'Note down admin password securely. Set up guest network for visitors. Enable parental controls if needed. Check for firmware updates monthly.'}
    },
    {
        'title': 'Port Forwarding Setup on Router',
        'description': 'Configure port forwarding on router for servers, games, or remote access.',
        'category': 'networking',
        'subcategory': 'routers',
        'os': ['windows', 'mac'],
        'difficulty': 'intermediate',
        'tags': ['port-forwarding', 'router', 'nat', 'networking', 'server'],
        'steps': [
            {'title': 'Find Device IP Address', 'description': 'Get local IP of target device.', 'code': 'On Windows:\nipconfig\nNote: IPv4 Address (e.g., 192.168.1.100)\n\nOn Mac/Linux:\nifconfig | grep inet\n\nOn Phone:\nSettings → WiFi → Connected network → IP\n\nNote: Set static IP on device for\nport forwarding to work reliably', 'language': 'bash'},
            {'title': 'Access Router Settings', 'description': 'Login to router admin panel.', 'code': 'Common router addresses:\n- 192.168.0.1 (TP-Link, D-Link)\n- 192.168.1.1 (Linksys, Asus, Netgear)\n- 192.168.1.254 (Some ISP routers)\n\nFind your gateway:\nWindows: ipconfig | find "Gateway"\nMac: netstat -nr | grep default\n\nLogin with admin credentials', 'language': 'bash'},
            {'title': 'Create Port Forward Rule', 'description': 'Add port forwarding entry.', 'code': 'Navigate to:\n- Advanced → NAT Forwarding → Virtual Servers\n- OR Forwarding → Port Forwarding\n- OR NAT → Port Mapping\n\nAdd New Rule:\n- Service Name: Web Server (your name)\n- External Port: 80\n- Internal Port: 80\n- Internal IP: 192.168.1.100\n- Protocol: TCP (or Both)\n- Enable: Yes\n\nClick Save/Apply', 'language': 'bash'},
            {'title': 'Common Port Examples', 'description': 'Frequently forwarded ports.', 'code': 'Common Ports:\n\nWeb Server:\n- HTTP: 80 (TCP)\n- HTTPS: 443 (TCP)\n\nRemote Desktop:\n- RDP: 3389 (TCP)\n\nFile Sharing:\n- FTP: 21 (TCP)\n- SSH: 22 (TCP)\n\nGaming:\n- Minecraft: 25565 (TCP)\n- Xbox: 3074 (UDP/TCP)\n- PlayStation: 3478-3480 (TCP/UDP)\n\nCCTV/DVR:\n- HTTP: 80, 8080\n- RTSP: 554\n- Service: 37777, 6036', 'language': 'bash'}
        ],
        'postInstallation': {'title': 'Testing', 'content': 'Test port from outside network using: canyouseeme.org or yougetsignal.com. If not working: check firewall on device, verify IP is correct, ensure ISP allows port forwarding.'}
    },
    {
        'title': 'WiFi Speed Optimization Tips',
        'description': 'Improve WiFi speed and coverage with router optimization techniques.',
        'category': 'networking',
        'subcategory': 'routers',
        'os': ['windows', 'mac'],
        'difficulty': 'beginner',
        'tags': ['wifi', 'speed', 'optimization', 'router', 'networking'],
        'steps': [
            {'title': 'Optimal Router Placement', 'description': 'Position router for best coverage.', 'code': 'Router Placement Tips:\n\n✓ DO:\n- Place in central location\n- Elevate router (shelf, wall mount)\n- Keep antennas vertical\n- Away from walls if possible\n\n✗ AVOID:\n- Near microwave, cordless phones\n- Inside cabinets or closets\n- Near fish tanks (water blocks signal)\n- On floor or behind TV\n- Near mirrors (reflects signal)', 'language': 'bash'},
            {'title': 'Change WiFi Channel', 'description': 'Avoid interference from neighbors.', 'code': 'Find Best Channel:\n1. Download WiFi Analyzer app\n2. Scan for nearby networks\n3. Find least crowded channel\n\nChange Channel:\n1. Router admin → Wireless Settings\n2. Change Channel:\n   - 2.4GHz: Use 1, 6, or 11\n   - 5GHz: Usually auto works well\n3. Save and test speed\n\nTip: 5GHz band has more\nclear channels but shorter range', 'language': 'bash'},
            {'title': 'Enable QoS', 'description': 'Prioritize important traffic.', 'code': 'Quality of Service (QoS):\n\n1. Router admin → QoS / Bandwidth Control\n2. Enable QoS\n3. Set priorities:\n   - High: Video calls, gaming\n   - Medium: Streaming\n   - Low: Downloads\n\nDevice Priority:\n- Add your work PC/laptop as high priority\n- Gaming console as high priority\n- IoT devices as low priority', 'language': 'bash'},
            {'title': 'Update and Optimize Settings', 'description': 'Additional optimization tips.', 'code': 'Optimizations:\n\n1. Update Firmware:\n   System Tools → Firmware Upgrade\n   Always use latest version\n\n2. Use 5GHz band:\n   - Faster speeds\n   - Less interference\n   - Shorter range\n\n3. Set Channel Width:\n   - 2.4GHz: 20MHz (more stable)\n   - 5GHz: 40MHz or 80MHz (faster)\n\n4. Disable legacy modes:\n   - Use 802.11n/ac only\n   - Disable 802.11b if no old devices\n\n5. Reboot router weekly:\n   Clears memory, refreshes connections', 'language': 'bash'}
        ],
        'postInstallation': {'title': 'Speed Test', 'content': 'Test speed at speedtest.net before and after changes. Compare 2.4GHz vs 5GHz speeds. Consider mesh WiFi system for large homes.'}
    }
]

# Combine all articles
ALL_ARTICLES.extend(COMPUTERS_WINDOWS)
ALL_ARTICLES.extend(COMPUTERS_MAC)
ALL_ARTICLES.extend(LEARNING_TALLY)
ALL_ARTICLES.extend(LEARNING_MSOFFICE)
ALL_ARTICLES.extend(LEARNING_BUSY)
ALL_ARTICLES.extend(LEARNING_PHOTOSHOP)
ALL_ARTICLES.extend(ROUTERS_NETWORKING)

async def seed_all_articles():
    print("=" * 60)
    print("  MASTER SEEDER - All Categories")
    print("=" * 60)
    
    added = 0
    skipped = 0
    
    for article in ALL_ARTICLES:
        # Add common fields
        article['id'] = str(uuid.uuid4())
        article['slug'] = create_slug(article['title'])
        article['author'] = 'Admin'
        article['createdAt'] = datetime.utcnow()
        article['updatedAt'] = datetime.utcnow()
        article['views'] = article.get('views', 1000 + (hash(article['title']) % 5000))
        article['likes'] = article.get('likes', 50 + (hash(article['title']) % 200))
        
        # Check if exists
        existing = await db.code_snippets.find_one({'slug': article['slug']})
        if not existing:
            await db.code_snippets.insert_one(article)
            print(f"✓ Added: {article['title'][:50]}...")
            added += 1
        else:
            print(f"- Skipped: {article['title'][:50]}...")
            skipped += 1
    
    print("\n" + "=" * 60)
    print(f"  SUMMARY")
    print("=" * 60)
    print(f"  Added: {added} articles")
    print(f"  Skipped: {skipped} articles")
    
    # Category summary
    print("\n  Category Breakdown:")
    categories = await db.code_snippets.aggregate([
        {"$group": {"_id": "$category", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}}
    ]).to_list(50)
    
    for cat in categories:
        print(f"    - {cat['_id']}: {cat['count']} articles")
    
    total = await db.code_snippets.count_documents({})
    print(f"\n  TOTAL ARTICLES IN DATABASE: {total}")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(seed_all_articles())
