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

# CCTV Camera Articles
cctv_articles = [
    ("Install CP Plus CCTV Camera", "Complete installation guide for CP Plus surveillance camera", ["cpplus", "cctv", "installation", "camera"], ["windows"], "intermediate", [
        {"title": "Unbox and Check Components", "description": "Verify camera package contents", "code": "Components checklist:\n✓ CP Plus camera unit\n✓ Power adapter (12V DC)\n✓ Mounting bracket and screws\n✓ BNC/Ethernet cable\n✓ User manual\n✓ Screwdriver", "language": "bash"},
        {"title": "Choose Installation Location", "description": "Select optimal camera placement", "code": "Best practices:\n1. Mount 8-10 feet high\n2. Cover entry/exit points\n3. Avoid direct sunlight\n4. Ensure power access\n5. Wide field of view\n6. Protected from weather", "language": "bash"},
        {"title": "Mount the Camera", "description": "Physically install camera", "code": "1. Mark drill holes using bracket\n2. Drill holes (use wall anchors)\n3. Secure bracket with screws\n4. Attach camera to bracket\n5. Adjust angle and tighten\n6. Connect cables", "language": "bash"},
        {"title": "Connect to DVR/NVR", "description": "Wire camera to recording device", "code": "Analog (BNC):\n1. Connect BNC cable to camera\n2. Connect to DVR input\n3. Connect power adapter\n\nIP Camera:\n1. Connect Ethernet cable\n2. Connect to NVR/PoE switch\n3. Power via PoE or adapter", "language": "bash"},
        {"title": "Configure Camera", "description": "Set up via CP Plus software", "code": "1. Download CP Plus CMS software\n2. Add device (enter IP)\n3. Login: admin/admin123\n4. Configure resolution\n5. Set motion detection\n6. Configure recording\n7. Set up mobile access", "language": "bash"}
    ]),
    
    ("Configure TP-Link VIGI Camera", "Setup TP-Link VIGI IP surveillance camera", ["tplink", "vigi", "ip-camera", "configuration"], ["windows"], "intermediate", [
        {"title": "Power On VIGI Camera", "description": "Initial camera setup", "code": "1. Connect to PoE switch or adapter\n2. Connect Ethernet to network\n3. Wait for LED to turn solid\n4. Note MAC address on label", "language": "bash"},
        {"title": "Find Camera IP", "description": "Locate camera on network", "code": "Method 1 - VIGI Security Manager:\n1. Download VIGI software\n2. Click 'Search Device'\n3. Note camera IP address\n\nMethod 2 - Router:\n1. Login to router\n2. Check DHCP client list\n3. Find device by MAC", "language": "bash"},
        {"title": "Access Web Interface", "description": "Configure via browser", "code": "1. Open browser\n2. Enter IP: http://192.168.1.x\n3. Create admin password\n4. Follow setup wizard\n5. Configure network\n6. Set recording parameters", "language": "bash"},
        {"title": "Install Mobile App", "description": "Remote camera access", "code": "1. Download 'TP-Link VIGI' app\n2. Create TP-Link account\n3. Tap '+' to add camera\n4. Scan QR code\n5. Enter password\n6. Configure notifications", "language": "bash"}
    ]),
    
    ("Set Up CP Plus DVR/NVR", "Configure CP Plus recording device", ["cpplus", "dvr", "nvr", "recording"], ["windows"], "intermediate", [
        {"title": "Connect DVR/NVR", "description": "Wire recording device", "code": "1. Connect cameras to DVR ports\n2. Connect HDMI to monitor\n3. Connect mouse to USB\n4. Connect Ethernet to router\n5. Power on DVR/NVR\n6. Wait 2-3 minutes", "language": "bash"},
        {"title": "Initial Setup", "description": "First-time configuration", "code": "1. Select language\n2. Accept terms\n3. Set admin password\n4. Configure date/time\n5. Set time zone\n6. Configure network\n7. Initialize hard drive", "language": "bash"}
    ]),
    
    ("Configure Motion Detection", "Set up motion alerts for cameras", ["motion-detection", "alerts", "cctv"], ["windows"], "intermediate", [
        {"title": "Access Settings", "description": "Open motion detection", "code": "1. Login to camera/NVR\n2. Go to Settings\n3. Select camera channel\n4. Click Motion Detection\n5. Enable toggle", "language": "bash"},
        {"title": "Configure Zones", "description": "Set active areas", "code": "1. Draw zones on preview\n2. Avoid moving objects\n3. Set sensitivity 50-70%\n4. Configure schedule\n5. Save settings", "language": "bash"}
    ]),
    
    ("VIGI Cloud Storage Setup", "Enable cloud recording", ["vigi", "cloud", "storage"], ["windows"], "beginner", [
        {"title": "Subscribe to Cloud", "description": "Get storage plan", "code": "1. Open VIGI app\n2. Select camera\n3. Tap Cloud Service\n4. Choose plan (7/30/90 days)\n5. Complete payment", "language": "bash"}
    ]),
    
    ("Connect CCTV to Mobile", "Remote access via smartphone", ["mobile", "remote-access", "cctv"], ["windows"], "beginner", [
        {"title": "CP Plus App", "description": "Mobile setup", "code": "1. Download gCMOB app\n2. Create account\n3. Tap '+' to add device\n4. Scan QR code\n5. Enter details\n6. View live feed", "language": "bash"}
    ]),
]

# Computers Articles
computers_articles = [
    ("Install Windows 11", "Complete Windows 11 installation guide", ["windows", "installation", "windows11"], ["windows"], "beginner", [
        {"title": "Check Requirements", "description": "Verify system compatibility", "code": "Requirements:\n✓ 64-bit processor\n✓ 4GB RAM minimum\n✓ 64GB storage\n✓ TPM 2.0\n✓ Secure Boot capable\n✓ UEFI firmware", "language": "bash"},
        {"title": "Create Bootable USB", "description": "Make installation media", "code": "1. Download Media Creation Tool\n2. Run tool\n3. Accept license\n4. Select USB flash drive\n5. Wait for creation", "language": "bash"},
        {"title": "Install Windows", "description": "Complete installation", "code": "1. Boot from USB\n2. Select language\n3. Click Install now\n4. Enter product key\n5. Choose partition\n6. Wait 20-30 minutes", "language": "bash"}
    ]),
    
    ("Configure Remote Desktop", "Enable RDP on Windows", ["windows", "remote-desktop", "rdp"], ["windows"], "intermediate", [
        {"title": "Enable RDP", "description": "Turn on Remote Desktop", "code": "PowerShell (Admin):\nSet-ItemProperty -Path 'HKLM:\\System\\CurrentControlSet\\Control\\Terminal Server' -name 'fDenyTSConnections' -Value 0\n\nEnable-NetFirewallRule -DisplayGroup 'Remote Desktop'", "language": "powershell"},
        {"title": "Connect", "description": "Use Remote Desktop", "code": "1. Press Win + R\n2. Type mstsc\n3. Enter computer IP\n4. Click Connect\n5. Enter credentials", "language": "bash"}
    ]),
    
    ("Windows PC as Local Server", "Convert PC to web server", ["windows", "server", "iis"], ["windows"], "intermediate", [
        {"title": "Install IIS", "description": "Enable web server", "code": "PowerShell:\nEnable-WindowsOptionalFeature -Online -FeatureName IIS-WebServerRole -All", "language": "powershell"},
        {"title": "Configure IIS", "description": "Set up website", "code": "1. Open IIS Manager\n2. Add Website\n3. Set physical path\n4. Configure port 80\n5. Click OK", "language": "bash"}
    ]),
    
    ("Install Windows on Mac", "Dual-boot with Boot Camp", ["mac", "bootcamp", "windows"], ["mac"], "intermediate", [
        {"title": "Check Compatibility", "description": "Verify Intel Mac", "code": "1. Check Intel processor\n2. Need 64GB free space\n3. Update macOS\n4. Backup with Time Machine", "language": "bash"},
        {"title": "Run Boot Camp", "description": "Create Windows partition", "code": "1. Open Boot Camp Assistant\n2. Select Windows ISO\n3. Set partition size (64GB+)\n4. Click Install\n5. Mac restarts", "language": "bash"}
    ]),
    
    ("macOS Terminal Commands", "Essential Mac Terminal", ["mac", "terminal", "commands"], ["mac"], "beginner", [
        {"title": "Basic Commands", "description": "Navigate and manage files", "code": "pwd  # Current directory\nls -la  # List files\ncd /path  # Change directory\nmkdir folder  # Create folder\ncp file dest  # Copy\nmv old new  # Move/rename\nrm file  # Delete", "language": "bash"}
    ]),
]

# Router/Networking Articles
router_articles = [
    ("Configure TP-Link Router", "Setup TP-Link wireless router", ["router", "tplink", "wifi", "networking"], ["windows"], "beginner", [
        {"title": "Connect Router", "description": "Physical setup", "code": "1. Connect modem to WAN port\n2. Connect PC to LAN port\n3. Or connect via WiFi\n4. Power on router\n5. Wait 2 minutes", "language": "bash"},
        {"title": "Access Admin", "description": "Login to interface", "code": "1. Open browser\n2. Go to: 192.168.0.1\n   or tplinkwifi.net\n3. Login: admin/admin\n4. Create new password", "language": "bash"},
        {"title": "Configure WiFi", "description": "Setup wireless", "code": "1. Go to Wireless Settings\n2. Set Network Name (SSID)\n3. Choose WPA2/WPA3\n4. Set WiFi password\n5. Save settings", "language": "bash"}
    ]),
    
    ("Set Up Home LAN Network", "Configure home network", ["router", "lan", "home-network", "networking"], ["windows"], "intermediate", [
        {"title": "Plan Network", "description": "Design layout", "code": "Network design:\n1. ISP Modem\n2. Main Router\n3. Switch (wired devices)\n4. Access Points (WiFi)\n5. Devices\n\nIP Scheme:\nRouter: 192.168.1.1\nStatic: .2-.50\nDHCP: .100-.250", "language": "bash"},
        {"title": "Configure DHCP", "description": "Auto IP assignment", "code": "1. Login to router\n2. Go to DHCP Settings\n3. Enable DHCP\n4. Set range: .100-.250\n5. Set DNS: 8.8.8.8\n6. Save", "language": "bash"}
    ]),
    
    ("Router Port Forwarding", "Open ports for services", ["port-forwarding", "router", "nat", "networking"], ["windows"], "intermediate", [
        {"title": "Find Local IP", "description": "Get device IP", "code": "Windows:\nipconfig | findstr IPv4\n\nmacOS:\nifconfig | grep inet", "language": "bash"},
        {"title": "Set Up Forward", "description": "Configure port", "code": "1. Login to router\n2. Go to Port Forwarding\n3. Add New\n4. Service Port: 80\n5. Internal Port: 80\n6. IP: 192.168.1.100\n7. Protocol: TCP\n8. Enable and Save", "language": "bash"}
    ]),
    
    ("Configure Router QoS", "Prioritize network traffic", ["qos", "router", "bandwidth", "networking"], ["windows"], "intermediate", [
        {"title": "Enable QoS", "description": "Turn on Quality of Service", "code": "1. Login to router\n2. Go to QoS/Bandwidth Control\n3. Enable QoS\n4. Enter WAN speeds\n5. Save", "language": "bash"},
        {"title": "Set Priorities", "description": "Configure rules", "code": "Priority levels:\n1. Highest: Video calls\n2. High: Gaming\n3. Medium: Browsing\n4. Low: Downloads", "language": "bash"}
    ]),
    
    ("Set Up Guest WiFi", "Create isolated guest network", ["guest-wifi", "router", "security", "networking"], ["windows"], "beginner", [
        {"title": "Enable Guest Network", "description": "Activate guest WiFi", "code": "1. Login to router\n2. Go to Guest Network\n3. Enable\n4. Set SSID: Home-Guest\n5. Set Password\n6. Enable isolation\n7. Save", "language": "bash"}
    ]),
    
    ("Configure Mesh WiFi", "Setup mesh system", ["mesh-wifi", "router", "coverage", "networking"], ["windows"], "intermediate", [
        {"title": "Setup Main Node", "description": "Configure primary unit", "code": "1. Connect to modem\n2. Download mesh app\n3. Create account\n4. Follow wizard\n5. Set network name\n6. Complete setup", "language": "bash"}
    ]),
]

async def seed_missing():
    print("🚀 Adding Missing Categories...\n")
    
    all_articles = []
    
    # Add CCTV articles
    print("📹 Adding CCTV Camera articles...")
    for article in cctv_articles:
        title, description, tags, os_list, difficulty, steps = article
        snippet = {
            'id': str(uuid.uuid4()),
            'title': title,
            'slug': create_slug(title),
            'description': description,
            'category': 'cctv-cameras',
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
        all_articles.append(snippet)
    print(f"   ✅ {len(cctv_articles)} CCTV articles prepared\n")
    
    # Add Computers articles
    print("💻 Adding Computers articles...")
    for article in computers_articles:
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
        all_articles.append(snippet)
    print(f"   ✅ {len(computers_articles)} Computers articles prepared\n")
    
    # Add Router/Networking articles
    print("🌐 Adding Router/Networking articles...")
    for article in router_articles:
        title, description, tags, os_list, difficulty, steps = article
        snippet = {
            'id': str(uuid.uuid4()),
            'title': title,
            'slug': create_slug(title),
            'description': description,
            'category': 'networking',
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
        all_articles.append(snippet)
    print(f"   ✅ {len(router_articles)} Router articles prepared\n")
    
    # Insert all
    if all_articles:
        result = await db.code_snippets.insert_many(all_articles)
        print(f"💾 Inserted {len(result.inserted_ids)} articles!\n")
    
    # Get totals
    print("=" * 60)
    print("📊 DATABASE SUMMARY")
    print("=" * 60)
    categories = await db.code_snippets.distinct('category')
    for cat in sorted(categories):
        count = await db.code_snippets.count_documents({'category': cat})
        print(f"   {cat.upper()}: {count} articles")
    
    total = await db.code_snippets.count_documents({})
    print(f"\n🎯 GRAND TOTAL: {total} articles\n")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(seed_missing())
