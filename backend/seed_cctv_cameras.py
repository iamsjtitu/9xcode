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

async def seed_cctv_articles():
    print("Seeding CCTV Camera articles...")
    
    cctv_articles = [
        # ========== CP PLUS Articles ==========
        {
            'id': str(uuid.uuid4()),
            'title': 'CP Plus DVR Factory Reset via Button',
            'slug': create_slug('CP Plus DVR Factory Reset via Button'),
            'description': 'Step-by-step guide to factory reset CP Plus DVR using physical reset button on the device.',
            'category': 'cctv-cameras',
            'subcategory': 'cpplus',
            'os': ['windows', 'mac'],
            'difficulty': 'beginner',
            'views': 4520,
            'likes': 89,
            'author': 'Admin',
            'createdAt': datetime.utcnow(),
            'updatedAt': datetime.utcnow(),
            'tags': ['cpplus', 'dvr', 'factory-reset', 'cctv', 'troubleshooting'],
            'steps': [
                {
                    'title': 'Power Off the DVR',
                    'description': 'Turn off the DVR by unplugging the power cable.',
                    'code': '1. Locate the power cable at back of DVR\n2. Unplug the power adapter\n3. Wait for 30 seconds',
                    'language': 'bash'
                },
                {
                    'title': 'Locate Reset Button',
                    'description': 'Find the small reset button on the back or bottom of DVR.',
                    'code': 'Reset button location:\n- Back panel (small hole)\n- Bottom of device\n- Near USB ports\n\nYou may need a pin or paperclip to press it.',
                    'language': 'bash'
                },
                {
                    'title': 'Press and Hold Reset Button',
                    'description': 'While holding the reset button, plug in the power cable.',
                    'code': '1. Press and HOLD the reset button with pin\n2. While holding, plug in power cable\n3. Keep holding for 15-20 seconds\n4. DVR will beep or LEDs will flash\n5. Release the button',
                    'language': 'bash'
                },
                {
                    'title': 'Wait for Reboot',
                    'description': 'DVR will restart with factory default settings.',
                    'code': 'Default credentials after reset:\n\nUsername: admin\nPassword: admin (or blank/empty)\n\nSome models:\nUsername: admin\nPassword: 123456',
                    'language': 'bash'
                }
            ],
            'postInstallation': {
                'title': 'After Factory Reset',
                'content': 'Reconfigure your DVR settings including date/time, recording schedule, camera settings, and network configuration. Change default password immediately for security.'
            }
        },
        {
            'id': str(uuid.uuid4()),
            'title': 'CP Plus DVR Password Reset using Config File',
            'slug': create_slug('CP Plus DVR Password Reset using Config File'),
            'description': 'Reset forgotten CP Plus DVR password by exporting and modifying configuration file.',
            'category': 'cctv-cameras',
            'subcategory': 'cpplus',
            'os': ['windows'],
            'difficulty': 'intermediate',
            'views': 6780,
            'likes': 156,
            'author': 'Admin',
            'createdAt': datetime.utcnow(),
            'updatedAt': datetime.utcnow(),
            'tags': ['cpplus', 'password-reset', 'dvr', 'configuration', 'cctv'],
            'steps': [
                {
                    'title': 'Connect USB Drive to DVR',
                    'description': 'Insert a FAT32 formatted USB drive into DVR.',
                    'code': 'USB Drive Requirements:\n- Format: FAT32\n- Size: 2GB to 32GB recommended\n- Empty drive preferred',
                    'language': 'bash'
                },
                {
                    'title': 'Export Configuration',
                    'description': 'Go to Main Menu > System > Config Backup > Export.',
                    'code': 'Navigation Path:\nMain Menu → System → Maintenance → Config Backup\n\nOR\n\nMain Menu → System → Default → Export Config\n\nSelect USB drive and click Export',
                    'language': 'bash'
                },
                {
                    'title': 'Edit Configuration File on PC',
                    'description': 'Open the exported .cfg or .bin file with Notepad++.',
                    'code': '1. Remove USB from DVR, insert in PC\n2. Open config file with Notepad++\n3. Search for "Password" or "PWD"\n4. Look for encoded password string\n5. Delete the password value or replace with:\n   - Empty string\n   - "admin" or "123456"',
                    'language': 'bash'
                },
                {
                    'title': 'Import Modified Config',
                    'description': 'Import the modified configuration back to DVR.',
                    'code': 'Navigation Path:\nMain Menu → System → Maintenance → Config Backup → Import\n\nSelect the modified config file\nDVR will restart automatically',
                    'language': 'bash'
                }
            ],
            'postInstallation': {
                'title': 'Important Notes',
                'content': 'This method works on most CP Plus DVR models. If config file is encrypted, contact CP Plus support with device serial number for password recovery.'
            }
        },
        {
            'id': str(uuid.uuid4()),
            'title': 'CP Plus DVR Remote View Setup - gCMOB App',
            'slug': create_slug('CP Plus DVR Remote View Setup gCMOB App'),
            'description': 'Configure CP Plus DVR for remote viewing using gCMOB mobile app on Android and iOS.',
            'category': 'cctv-cameras',
            'subcategory': 'cpplus',
            'os': ['windows', 'mac'],
            'difficulty': 'beginner',
            'views': 12450,
            'likes': 287,
            'author': 'Admin',
            'createdAt': datetime.utcnow(),
            'updatedAt': datetime.utcnow(),
            'tags': ['cpplus', 'gcmob', 'remote-view', 'mobile-app', 'cctv', 'p2p'],
            'steps': [
                {
                    'title': 'Enable P2P on DVR',
                    'description': 'Enable P2P (Peer to Peer) feature on your CP Plus DVR.',
                    'code': 'Navigation Path:\nMain Menu → Network → P2P\n\nSettings:\n- P2P Enable: ON\n- Note down the Serial Number/Device ID\n- Status should show: Online',
                    'language': 'bash'
                },
                {
                    'title': 'Download gCMOB App',
                    'description': 'Install gCMOB app on your smartphone.',
                    'code': 'Android: Google Play Store → Search "gCMOB"\niOS: App Store → Search "gCMOB"\n\nAlternative Apps:\n- KCMOB\n- iCMOB (for iOS)\n- CP Plus Indigo',
                    'language': 'bash'
                },
                {
                    'title': 'Add Device in gCMOB',
                    'description': 'Open gCMOB app and add your DVR device.',
                    'code': '1. Open gCMOB app\n2. Tap "+" or "Add Device"\n3. Select "P2P" or "Cloud"\n4. Scan QR code from DVR screen\n   OR manually enter:\n   - Device Name: My DVR\n   - Serial No: (from DVR P2P menu)\n   - Username: admin\n   - Password: (your DVR password)\n5. Tap "Save" or "Add"',
                    'language': 'bash'
                },
                {
                    'title': 'Configure Port Forwarding (Optional)',
                    'description': 'For direct IP access, configure port forwarding on router.',
                    'code': 'Default CP Plus Ports:\n- HTTP Port: 80\n- Server Port: 6036\n- RTSP Port: 554\n- Mobile Port: 8091\n\nRouter Port Forwarding:\nExternal Port → Internal Port → DVR IP Address\n80 → 80 → 192.168.1.108\n6036 → 6036 → 192.168.1.108',
                    'language': 'bash'
                }
            ],
            'postInstallation': {
                'title': 'Troubleshooting',
                'content': 'If device shows offline: 1) Check internet connection on DVR 2) Verify P2P is enabled 3) Restart DVR and app 4) Check if DVR firmware is updated.'
            }
        },
        {
            'id': str(uuid.uuid4()),
            'title': 'CP Plus DVR Hard Drive Format and Setup',
            'slug': create_slug('CP Plus DVR Hard Drive Format and Setup'),
            'description': 'How to format and initialize new hard drive in CP Plus DVR for recording.',
            'category': 'cctv-cameras',
            'subcategory': 'cpplus',
            'os': ['windows'],
            'difficulty': 'beginner',
            'views': 5670,
            'likes': 134,
            'author': 'Admin',
            'createdAt': datetime.utcnow(),
            'updatedAt': datetime.utcnow(),
            'tags': ['cpplus', 'hard-drive', 'hdd', 'format', 'storage', 'cctv'],
            'steps': [
                {
                    'title': 'Install Hard Drive in DVR',
                    'description': 'Physically install the HDD in your DVR.',
                    'code': 'Supported HDD:\n- Seagate SkyHawk (Recommended)\n- WD Purple (Recommended)\n- Any SATA HDD 500GB to 8TB\n\nInstallation:\n1. Power off DVR\n2. Open DVR cover\n3. Connect SATA data cable\n4. Connect SATA power cable\n5. Secure HDD with screws\n6. Close cover and power on',
                    'language': 'bash'
                },
                {
                    'title': 'Access HDD Management',
                    'description': 'Navigate to hard drive management menu.',
                    'code': 'Navigation Path:\nMain Menu → Storage → HDD Manage\n\nOR\n\nMain Menu → Settings → Storage → HDD',
                    'language': 'bash'
                },
                {
                    'title': 'Format Hard Drive',
                    'description': 'Select and format the new hard drive.',
                    'code': '1. Select the new HDD (usually shows as "Uninitialized")\n2. Click "Format" or "Initialize"\n3. Confirm the format action\n4. Wait for formatting (5-30 mins based on size)\n5. Status will change to "Normal"',
                    'language': 'bash'
                },
                {
                    'title': 'Configure Recording Settings',
                    'description': 'Set up recording schedule and quality.',
                    'code': 'Navigation: Main Menu → Record → Record Config\n\nRecommended Settings:\n- Record Mode: Auto/Schedule\n- Stream Type: Main Stream\n- Resolution: 1080P\n- Frame Rate: 15-25 fps\n- Bitrate: 2048-4096 kbps\n\nEnable Overwrite: YES (for continuous recording)',
                    'language': 'bash'
                }
            ],
            'postInstallation': {
                'title': 'Storage Calculation',
                'content': '1TB HDD ≈ 7-10 days recording for 4 cameras at 1080P. For 8 cameras, expect 3-5 days. Use "Record Estimate" feature in DVR to calculate exact storage requirements.'
            }
        },
        {
            'id': str(uuid.uuid4()),
            'title': 'CP Plus DVR Network Configuration Static IP',
            'slug': create_slug('CP Plus DVR Network Configuration Static IP'),
            'description': 'Configure static IP address on CP Plus DVR for stable network connectivity.',
            'category': 'cctv-cameras',
            'subcategory': 'cpplus',
            'os': ['windows'],
            'difficulty': 'intermediate',
            'views': 4230,
            'likes': 98,
            'author': 'Admin',
            'createdAt': datetime.utcnow(),
            'updatedAt': datetime.utcnow(),
            'tags': ['cpplus', 'network', 'static-ip', 'configuration', 'cctv'],
            'steps': [
                {
                    'title': 'Find Your Network Details',
                    'description': 'Get your network gateway and subnet information.',
                    'code': 'On Windows PC (same network):\nOpen CMD and run:\n\nipconfig\n\nNote down:\n- Default Gateway: 192.168.1.1\n- Subnet Mask: 255.255.255.0\n- Choose unused IP for DVR: 192.168.1.108',
                    'language': 'bash'
                },
                {
                    'title': 'Access Network Settings on DVR',
                    'description': 'Navigate to network configuration menu.',
                    'code': 'Navigation Path:\nMain Menu → Network → TCP/IP\n\nOR\n\nMain Menu → Settings → Network → Basic',
                    'language': 'bash'
                },
                {
                    'title': 'Configure Static IP',
                    'description': 'Enter static IP configuration.',
                    'code': 'Network Settings:\n- DHCP: Disable/OFF\n- IP Address: 192.168.1.108\n- Subnet Mask: 255.255.255.0\n- Gateway: 192.168.1.1\n- DNS1: 8.8.8.8\n- DNS2: 8.8.4.4\n\nClick "Apply" or "Save"',
                    'language': 'bash'
                },
                {
                    'title': 'Test Network Connection',
                    'description': 'Verify DVR is accessible on network.',
                    'code': 'From your PC, open CMD:\n\nping 192.168.1.108\n\nIf successful, access DVR web interface:\nOpen browser: http://192.168.1.108\n\nLogin with DVR credentials',
                    'language': 'bash'
                }
            ],
            'postInstallation': {
                'title': 'Router Configuration',
                'content': 'Reserve the IP address (192.168.1.108) in your router DHCP settings to prevent IP conflicts. This ensures DVR always gets the same IP even after restart.'
            }
        },
        
        # ========== TP-LINK VIGI Articles ==========
        {
            'id': str(uuid.uuid4()),
            'title': 'TP-Link VIGI NVR Initial Setup and Configuration',
            'slug': create_slug('TP-Link VIGI NVR Initial Setup and Configuration'),
            'description': 'Complete setup guide for TP-Link VIGI NVR including camera discovery and basic configuration.',
            'category': 'cctv-cameras',
            'subcategory': 'tplink-vigi',
            'os': ['windows', 'mac'],
            'difficulty': 'beginner',
            'views': 3450,
            'likes': 78,
            'author': 'Admin',
            'createdAt': datetime.utcnow(),
            'updatedAt': datetime.utcnow(),
            'tags': ['tplink', 'vigi', 'nvr', 'setup', 'cctv', 'poe'],
            'steps': [
                {
                    'title': 'Physical Setup',
                    'description': 'Connect NVR hardware components.',
                    'code': 'Connections:\n1. Connect Ethernet cable to NVR LAN port → Router\n2. Connect VIGI cameras to NVR PoE ports\n3. Connect mouse to USB port\n4. Connect monitor via HDMI/VGA\n5. Connect power adapter\n6. Power ON the NVR',
                    'language': 'bash'
                },
                {
                    'title': 'Initial Wizard Setup',
                    'description': 'Complete the setup wizard on first boot.',
                    'code': 'Setup Wizard Steps:\n1. Select Language: English\n2. Set Admin Password (min 8 characters)\n3. Set Date/Time and Timezone\n4. Configure Network:\n   - DHCP: Enable (recommended)\n   - Or set Static IP\n5. Initialize HDD when prompted',
                    'language': 'bash'
                },
                {
                    'title': 'Add VIGI Cameras',
                    'description': 'Discover and add cameras connected to NVR.',
                    'code': 'Navigation: Settings → Camera → Camera\n\n1. Click "+" or "Add"\n2. NVR will auto-discover VIGI cameras\n3. Select cameras to add\n4. Enter camera password (default: admin)\n5. Click "Add"\n\nNote: Cameras on PoE ports are auto-added',
                    'language': 'bash'
                },
                {
                    'title': 'Configure Recording',
                    'description': 'Set up continuous and motion recording.',
                    'code': 'Navigation: Settings → Storage → Schedule\n\n1. Select camera channel\n2. Set Recording Type:\n   - Continuous (Blue)\n   - Motion Detection (Yellow)\n   - Alarm (Red)\n3. Draw schedule on timeline\n4. Apply to all cameras if needed\n5. Click "Save"',
                    'language': 'bash'
                }
            ],
            'postInstallation': {
                'title': 'VIGI App Setup',
                'content': 'Download "VIGI" app from Play Store/App Store for remote viewing. Create TP-Link ID, add NVR using QR code scan or Cloud ID. Enable TP-Link Cloud in NVR settings for P2P access.'
            }
        },
        {
            'id': str(uuid.uuid4()),
            'title': 'TP-Link VIGI Camera Password Reset',
            'slug': create_slug('TP-Link VIGI Camera Password Reset'),
            'description': 'Reset forgotten password on TP-Link VIGI IP cameras using reset button or VIGI app.',
            'category': 'cctv-cameras',
            'subcategory': 'tplink-vigi',
            'os': ['windows', 'mac'],
            'difficulty': 'beginner',
            'views': 2890,
            'likes': 67,
            'author': 'Admin',
            'createdAt': datetime.utcnow(),
            'updatedAt': datetime.utcnow(),
            'tags': ['tplink', 'vigi', 'password-reset', 'camera', 'cctv'],
            'steps': [
                {
                    'title': 'Method 1: Physical Reset Button',
                    'description': 'Use the hardware reset button on camera.',
                    'code': 'Reset Button Location:\n- Usually on back or bottom of camera\n- Small pinhole button\n\nReset Process:\n1. Power ON the camera\n2. Wait for camera to fully boot (1-2 mins)\n3. Press and hold reset button for 10-15 seconds\n4. Camera will reboot\n5. Default password restored: "admin" or blank',
                    'language': 'bash'
                },
                {
                    'title': 'Method 2: Via VIGI Security Manager',
                    'description': 'Use VIGI Security Manager software on PC.',
                    'code': 'Download VIGI Security Manager:\nhttps://www.tp-link.com/support/download/vigi-security-manager/\n\nSteps:\n1. Install and open VIGI Security Manager\n2. Software will discover cameras\n3. Right-click on camera → "Reset Password"\n4. Follow on-screen instructions\n5. Camera resets to default',
                    'language': 'bash'
                },
                {
                    'title': 'Method 3: Via NVR (if connected)',
                    'description': 'Reset camera password through VIGI NVR.',
                    'code': 'On NVR:\n1. Go to Settings → Camera → Camera\n2. Find the locked camera\n3. Click "Edit" or gear icon\n4. Select "Reset Password"\n5. Confirm action\n6. Camera will use NVR-assigned password',
                    'language': 'bash'
                },
                {
                    'title': 'Reconfigure After Reset',
                    'description': 'Set new password and add camera back.',
                    'code': 'After Reset:\n1. Access camera via IP: http://camera-ip\n2. Login: admin / admin (or blank)\n3. Set new strong password immediately\n4. Reconfigure camera settings\n5. Re-add to NVR if needed',
                    'language': 'bash'
                }
            ],
            'postInstallation': {
                'title': 'Security Tip',
                'content': 'Always set a strong password after reset. Use combination of letters, numbers, and symbols. Store password securely. Enable HTTPS for camera access.'
            }
        },
        {
            'id': str(uuid.uuid4()),
            'title': 'TP-Link VIGI Remote Access Setup via TP-Link Cloud',
            'slug': create_slug('TP-Link VIGI Remote Access Setup via TP-Link Cloud'),
            'description': 'Configure TP-Link VIGI NVR for remote viewing using TP-Link Cloud and VIGI mobile app.',
            'category': 'cctv-cameras',
            'subcategory': 'tplink-vigi',
            'os': ['windows', 'mac'],
            'difficulty': 'beginner',
            'views': 5670,
            'likes': 134,
            'author': 'Admin',
            'createdAt': datetime.utcnow(),
            'updatedAt': datetime.utcnow(),
            'tags': ['tplink', 'vigi', 'remote-access', 'cloud', 'mobile-app', 'cctv'],
            'steps': [
                {
                    'title': 'Create TP-Link ID',
                    'description': 'Create a TP-Link account if you dont have one.',
                    'code': 'Via VIGI App:\n1. Download "VIGI" app (Android/iOS)\n2. Open app → Sign Up\n3. Enter email address\n4. Create password\n5. Verify email\n6. Login to app\n\nOR via website: https://www.tplinkcloud.com',
                    'language': 'bash'
                },
                {
                    'title': 'Enable TP-Link Cloud on NVR',
                    'description': 'Enable cloud service on your VIGI NVR.',
                    'code': 'On NVR:\n1. Go to Settings → Network → TP-Link Cloud\n2. Enable "Cloud Service"\n3. Login with your TP-Link ID\n4. Or scan QR code with VIGI app\n5. Cloud Status should show: "Connected"',
                    'language': 'bash'
                },
                {
                    'title': 'Add NVR to VIGI App',
                    'description': 'Add your NVR device in mobile app.',
                    'code': 'In VIGI App:\n1. Tap "+" to add device\n2. Select "NVR"\n3. Choose method:\n   a) Scan QR (from NVR screen)\n   b) Cloud ID (enter manually)\n   c) IP Address (local network only)\n4. Enter NVR admin password\n5. Tap "Add"',
                    'language': 'bash'
                },
                {
                    'title': 'View Cameras Remotely',
                    'description': 'Access your cameras from anywhere.',
                    'code': 'VIGI App Features:\n- Live View: See all cameras\n- Playback: View recordings\n- PTZ Control: Control pan-tilt-zoom cameras\n- Two-way Audio: Talk through camera\n- Notifications: Motion alerts\n- Snapshot: Save images\n\nEnsure NVR has internet access for remote viewing.',
                    'language': 'bash'
                }
            ],
            'postInstallation': {
                'title': 'Bandwidth Requirements',
                'content': 'For smooth remote viewing, ensure your NVR location has minimum 2Mbps upload speed per camera in sub-stream. Use Sub-Stream for mobile viewing to reduce bandwidth. Main-Stream recommended only on WiFi.'
            }
        },
        {
            'id': str(uuid.uuid4()),
            'title': 'TP-Link VIGI Camera Motion Detection Setup',
            'slug': create_slug('TP-Link VIGI Camera Motion Detection Setup'),
            'description': 'Configure motion detection zones and alerts on TP-Link VIGI cameras and NVR.',
            'category': 'cctv-cameras',
            'subcategory': 'tplink-vigi',
            'os': ['windows', 'mac'],
            'difficulty': 'intermediate',
            'views': 3120,
            'likes': 72,
            'author': 'Admin',
            'createdAt': datetime.utcnow(),
            'updatedAt': datetime.utcnow(),
            'tags': ['tplink', 'vigi', 'motion-detection', 'alerts', 'cctv', 'smart-detection'],
            'steps': [
                {
                    'title': 'Access Motion Detection Settings',
                    'description': 'Navigate to motion detection configuration.',
                    'code': 'On NVR:\nSettings → Event → Motion Detection\n\nOn Camera Web Interface:\nConfiguration → Event → Motion Detection',
                    'language': 'bash'
                },
                {
                    'title': 'Enable and Configure Detection Area',
                    'description': 'Set up motion detection zones.',
                    'code': 'Settings:\n1. Enable Motion Detection: ON\n2. Draw Detection Area:\n   - Click "Draw Area"\n   - Draw rectangles on video\n   - Red = Detection Zone\n   - Multiple zones supported\n3. Sensitivity: 50-70% (adjust as needed)\n4. Target Size: Medium\n5. Click "Save"',
                    'language': 'bash'
                },
                {
                    'title': 'Configure Recording Action',
                    'description': 'Set what happens when motion is detected.',
                    'code': 'Trigger Actions:\n1. Recording:\n   - Enable: YES\n   - Pre-record: 5 seconds\n   - Post-record: 30 seconds\n   \n2. Snapshot:\n   - Enable: YES\n   - Interval: 2 seconds\n   \n3. Buzzer:\n   - Enable: Optional\n   - Duration: 10 seconds',
                    'language': 'bash'
                },
                {
                    'title': 'Setup Push Notifications',
                    'description': 'Get alerts on your phone when motion detected.',
                    'code': 'On NVR:\n1. Go to Settings → Event → Notification\n2. Enable "App Push"\n3. Select camera channels\n4. Set schedule (or 24/7)\n\nIn VIGI App:\n1. Device Settings → Notifications\n2. Enable notifications\n3. Select alert types:\n   - Motion Detection\n   - Line Crossing\n   - Intrusion Detection',
                    'language': 'bash'
                }
            ],
            'postInstallation': {
                'title': 'Reducing False Alerts',
                'content': 'To reduce false motion alerts: 1) Avoid pointing camera at trees/moving objects 2) Reduce sensitivity in windy areas 3) Use detection zones to exclude high-movement areas 4) Enable "Human Detection" if camera supports AI features.'
            }
        },
        {
            'id': str(uuid.uuid4()),
            'title': 'TP-Link VIGI NVR Firmware Update',
            'slug': create_slug('TP-Link VIGI NVR Firmware Update'),
            'description': 'Update TP-Link VIGI NVR firmware for new features and security patches.',
            'category': 'cctv-cameras',
            'subcategory': 'tplink-vigi',
            'os': ['windows', 'mac'],
            'difficulty': 'intermediate',
            'views': 2340,
            'likes': 54,
            'author': 'Admin',
            'createdAt': datetime.utcnow(),
            'updatedAt': datetime.utcnow(),
            'tags': ['tplink', 'vigi', 'firmware', 'update', 'nvr', 'cctv'],
            'steps': [
                {
                    'title': 'Check Current Firmware Version',
                    'description': 'Find your current NVR firmware version.',
                    'code': 'On NVR:\nSettings → System → Device Info\n\nNote down:\n- Model Number: VIGI NVR1008H\n- Firmware Version: 1.0.12\n- Hardware Version: 1.0',
                    'language': 'bash'
                },
                {
                    'title': 'Download Latest Firmware',
                    'description': 'Get firmware from TP-Link website.',
                    'code': 'Steps:\n1. Go to: https://www.tp-link.com/support/download/\n2. Search your NVR model\n3. Select "Firmware" tab\n4. Download latest version\n5. Extract ZIP file\n6. Copy .bin file to USB drive (FAT32)',
                    'language': 'bash'
                },
                {
                    'title': 'Method 1: Update via USB',
                    'description': 'Update firmware using USB drive.',
                    'code': 'On NVR:\n1. Insert USB with firmware file\n2. Go to Settings → System → Maintenance\n3. Select "Local Upgrade"\n4. Browse and select .bin file\n5. Click "Upgrade"\n6. Wait 5-10 minutes\n7. NVR will restart automatically\n\nDO NOT power off during update!',
                    'language': 'bash'
                },
                {
                    'title': 'Method 2: Online Update',
                    'description': 'Update directly via internet if available.',
                    'code': 'On NVR:\n1. Ensure NVR has internet connection\n2. Go to Settings → System → Maintenance\n3. Select "Online Upgrade"\n4. Click "Check for Updates"\n5. If available, click "Upgrade"\n6. Wait for download and installation\n7. NVR restarts when complete',
                    'language': 'bash'
                }
            ],
            'postInstallation': {
                'title': 'After Update',
                'content': 'Verify firmware version in Device Info. Check all cameras are connected. Review any new features in release notes. Settings are usually preserved but verify recording schedule and network config.'
            }
        },
        
        # ========== HIKVISION Articles ==========
        {
            'id': str(uuid.uuid4()),
            'title': 'Hikvision DVR/NVR Password Reset using SADP Tool',
            'slug': create_slug('Hikvision DVR NVR Password Reset using SADP Tool'),
            'description': 'Reset forgotten Hikvision DVR/NVR admin password using official SADP Tool software.',
            'category': 'cctv-cameras',
            'subcategory': 'hikvision',
            'os': ['windows'],
            'difficulty': 'intermediate',
            'views': 8920,
            'likes': 198,
            'author': 'Admin',
            'createdAt': datetime.utcnow(),
            'updatedAt': datetime.utcnow(),
            'tags': ['hikvision', 'password-reset', 'sadp', 'dvr', 'nvr', 'cctv'],
            'steps': [
                {
                    'title': 'Download SADP Tool',
                    'description': 'Download the official Hikvision SADP Tool.',
                    'code': 'Download Link:\nhttps://www.hikvision.com/en/support/tools/\n\nSearch for "SADP" or "Device Search"\n\nSupported OS:\n- Windows 7/8/10/11\n- macOS version also available',
                    'language': 'bash'
                },
                {
                    'title': 'Connect DVR/NVR to Network',
                    'description': 'Ensure device is on same network as PC.',
                    'code': 'Network Setup:\n1. Connect DVR/NVR to router via Ethernet\n2. Connect PC to same router/network\n3. Power ON the DVR/NVR\n4. Note: Both devices must be on same subnet',
                    'language': 'bash'
                },
                {
                    'title': 'Discover Device in SADP',
                    'description': 'Open SADP Tool and find your device.',
                    'code': '1. Run SADP Tool as Administrator\n2. Tool will auto-scan network\n3. Find your device in list\n4. Note down:\n   - Serial Number\n   - IP Address\n   - Device Type\n5. Select the device by clicking on it',
                    'language': 'bash'
                },
                {
                    'title': 'Generate Reset Password',
                    'description': 'Request password reset from Hikvision.',
                    'code': 'Method A - Security Code:\n1. Click "Forgot Password"\n2. Export device file (.xml)\n3. Email file to Hikvision support\n4. They will send reset code\n5. Enter code in SADP Tool\n\nMethod B - Security Questions:\n1. If configured, answer security questions\n2. Reset password directly\n\nMethod C - GUID File:\n1. If you saved GUID during initial setup\n2. Import GUID file to reset',
                    'language': 'bash'
                },
                {
                    'title': 'Set New Password',
                    'description': 'Create new admin password.',
                    'code': 'After verification:\n1. Enter new password\n2. Password requirements:\n   - Minimum 8 characters\n   - Mix of letters, numbers, symbols\n3. Confirm new password\n4. Click "Confirm" or "OK"\n5. Device will reset and reboot',
                    'language': 'bash'
                }
            ],
            'postInstallation': {
                'title': 'Important Security Steps',
                'content': 'After password reset: 1) Set up security questions 2) Export and save GUID file 3) Enable HTTPS 4) Create operator accounts with limited access 5) Keep SADP Tool for future use.'
            }
        },
        {
            'id': str(uuid.uuid4()),
            'title': 'Hikvision Remote View Setup - Hik-Connect App',
            'slug': create_slug('Hikvision Remote View Setup Hik-Connect App'),
            'description': 'Configure Hikvision DVR/NVR for remote viewing using Hik-Connect mobile app.',
            'category': 'cctv-cameras',
            'subcategory': 'hikvision',
            'os': ['windows', 'mac'],
            'difficulty': 'beginner',
            'views': 11230,
            'likes': 267,
            'author': 'Admin',
            'createdAt': datetime.utcnow(),
            'updatedAt': datetime.utcnow(),
            'tags': ['hikvision', 'hik-connect', 'remote-view', 'mobile-app', 'p2p', 'cctv'],
            'steps': [
                {
                    'title': 'Enable Hik-Connect on DVR/NVR',
                    'description': 'Enable cloud service on your Hikvision device.',
                    'code': 'On DVR/NVR:\n1. Menu → Configuration → Network → Platform Access\n2. Check "Enable Hik-Connect"\n3. Create verification code (6+ chars)\n4. Status should show: "Online"\n5. Note down the Serial Number\n\nOR via Web Interface:\nConfiguration → Network → Advanced → Platform Access',
                    'language': 'bash'
                },
                {
                    'title': 'Download Hik-Connect App',
                    'description': 'Install official Hikvision app on phone.',
                    'code': 'Download:\n- Android: Play Store → "Hik-Connect"\n- iOS: App Store → "Hik-Connect"\n\nAlternative Apps:\n- iVMS-4500 (Full featured)\n- Hik-Connect (Simplified)',
                    'language': 'bash'
                },
                {
                    'title': 'Create Hik-Connect Account',
                    'description': 'Register for Hik-Connect cloud service.',
                    'code': '1. Open Hik-Connect app\n2. Tap "Register"\n3. Select region (Important!)\n4. Enter email/phone number\n5. Create password\n6. Verify via email/SMS\n7. Login to account',
                    'language': 'bash'
                },
                {
                    'title': 'Add Device to App',
                    'description': 'Add your DVR/NVR to Hik-Connect app.',
                    'code': 'In Hik-Connect App:\n1. Tap "+" to add device\n2. Select "Scan QR Code"\n   - Scan QR from DVR screen\n   OR\n   "Manual Adding":\n   - Enter Serial Number\n   - Enter Verification Code\n3. Wait for device to connect\n4. All cameras will appear',
                    'language': 'bash'
                }
            ],
            'postInstallation': {
                'title': 'Troubleshooting Connection',
                'content': 'If device shows offline: 1) Check DVR internet connection 2) Verify Hik-Connect is enabled 3) Check verification code matches 4) Restart DVR 5) Re-add device in app. For persistent issues, try port forwarding as backup.'
            }
        },
        
        # ========== JK VISION Articles ==========
        {
            'id': str(uuid.uuid4()),
            'title': 'JK Vision DVR Initial Setup Guide',
            'slug': create_slug('JK Vision DVR Initial Setup Guide'),
            'description': 'Complete setup guide for JK Vision DVR including camera connection and basic configuration.',
            'category': 'cctv-cameras',
            'subcategory': 'jk-vision',
            'os': ['windows'],
            'difficulty': 'beginner',
            'views': 2340,
            'likes': 45,
            'author': 'Admin',
            'createdAt': datetime.utcnow(),
            'updatedAt': datetime.utcnow(),
            'tags': ['jkvision', 'dvr', 'setup', 'installation', 'cctv'],
            'steps': [
                {
                    'title': 'Hardware Connections',
                    'description': 'Connect all DVR components.',
                    'code': 'Connections:\n1. Connect BNC cables from cameras to DVR video inputs\n2. Connect power supply to cameras\n3. Connect mouse to DVR USB port\n4. Connect monitor via VGA/HDMI\n5. Connect network cable to DVR\n6. Connect DVR power adapter\n7. Power ON',
                    'language': 'bash'
                },
                {
                    'title': 'Initial Login',
                    'description': 'Login with default credentials.',
                    'code': 'Default Login:\nUsername: admin\nPassword: admin OR 123456 OR blank\n\nIf prompted to change password:\n- Set new strong password\n- Remember to save it securely',
                    'language': 'bash'
                },
                {
                    'title': 'Configure Date and Time',
                    'description': 'Set correct date, time and timezone.',
                    'code': 'Navigation:\nMain Menu → System → General\n\nSettings:\n- Date Format: DD-MM-YYYY\n- Time Format: 24 Hour\n- Timezone: GMT+5:30 (India)\n- Enable NTP: Yes\n- NTP Server: pool.ntp.org\n\nClick Apply/Save',
                    'language': 'bash'
                },
                {
                    'title': 'Configure Recording',
                    'description': 'Set up recording schedule.',
                    'code': 'Navigation:\nMain Menu → Record → Record Config\n\nSettings for each channel:\n- Record: Enable\n- Stream Type: Main Stream\n- Resolution: 1080P/720P\n- Frame Rate: 15 fps\n- Bitrate Type: Variable\n- Quality: Higher\n\nSchedule:\n- Set 24x7 recording or custom schedule',
                    'language': 'bash'
                }
            ],
            'postInstallation': {
                'title': 'Next Steps',
                'content': 'Configure network settings for remote access. Format HDD if new. Set up motion detection for each camera. Download XMEye app for remote viewing.'
            }
        },
        {
            'id': str(uuid.uuid4()),
            'title': 'JK Vision DVR Remote View using XMEye App',
            'slug': create_slug('JK Vision DVR Remote View using XMEye App'),
            'description': 'Setup remote viewing for JK Vision DVR using XMEye mobile application.',
            'category': 'cctv-cameras',
            'subcategory': 'jk-vision',
            'os': ['windows', 'mac'],
            'difficulty': 'beginner',
            'views': 4560,
            'likes': 89,
            'author': 'Admin',
            'createdAt': datetime.utcnow(),
            'updatedAt': datetime.utcnow(),
            'tags': ['jkvision', 'xmeye', 'remote-view', 'mobile-app', 'cctv', 'p2p'],
            'steps': [
                {
                    'title': 'Get Cloud ID from DVR',
                    'description': 'Find the Cloud ID/Serial Number on DVR.',
                    'code': 'On DVR:\nMain Menu → Info → Version\n\nOR\n\nMain Menu → System → Info\n\nNote down:\n- Cloud ID / Serial No (looks like: abc123def456)\n- This is unique to your DVR',
                    'language': 'bash'
                },
                {
                    'title': 'Enable Cloud/P2P Service',
                    'description': 'Enable cloud service on DVR.',
                    'code': 'Navigation:\nMain Menu → Network → Cloud/P2P\n\nSettings:\n- Cloud Enable: Yes/On\n- Status should show: Connected/Online\n\nIf offline:\n- Check internet connection\n- Check DNS settings (use 8.8.8.8)',
                    'language': 'bash'
                },
                {
                    'title': 'Download XMEye App',
                    'description': 'Install XMEye on your smartphone.',
                    'code': 'Download:\n- Android: Play Store → "XMEye"\n- iOS: App Store → "XMEye"\n\nNote: XMEye works with most Chinese DVRs\nincluding JK Vision, TVT, Dahua clones',
                    'language': 'bash'
                },
                {
                    'title': 'Add Device to XMEye',
                    'description': 'Add your DVR in XMEye app.',
                    'code': '1. Open XMEye app\n2. Register/Login (or use Local Login)\n3. Tap "+" to add device\n4. Select "Add by Cloud ID"\n5. Enter:\n   - Device Name: Home DVR\n   - Cloud ID: (from DVR)\n   - Username: admin\n   - Password: (DVR password)\n6. Tap "Save"\n7. Device will connect and show cameras',
                    'language': 'bash'
                }
            ],
            'postInstallation': {
                'title': 'XMEye Tips',
                'content': 'Use "Sub Stream" for mobile data viewing to save bandwidth. Enable push notifications for motion alerts. You can also access via xmeye.net website using Cloud ID.'
            }
        },
        {
            'id': str(uuid.uuid4()),
            'title': 'JK Vision DVR Password Reset',
            'slug': create_slug('JK Vision DVR Password Reset'),
            'description': 'Reset forgotten password on JK Vision DVR using multiple methods.',
            'category': 'cctv-cameras',
            'subcategory': 'jk-vision',
            'os': ['windows'],
            'difficulty': 'intermediate',
            'views': 3450,
            'likes': 67,
            'author': 'Admin',
            'createdAt': datetime.utcnow(),
            'updatedAt': datetime.utcnow(),
            'tags': ['jkvision', 'password-reset', 'dvr', 'security', 'cctv'],
            'steps': [
                {
                    'title': 'Method 1: Date-Based Super Password',
                    'description': 'Generate super password based on DVR date.',
                    'code': 'Steps:\n1. Note the date shown on DVR screen\n2. Go to: https://www.yourspares.co.uk/pages/dvr-password-reset\n   OR search "XMEye password generator"\n3. Enter the date from DVR\n4. Generate super password\n5. Use generated password to login\n\nNote: Set DVR date to current date first if needed',
                    'language': 'bash'
                },
                {
                    'title': 'Method 2: Contact Supplier',
                    'description': 'Get reset code from DVR supplier.',
                    'code': 'Information needed:\n- DVR Model Number\n- Serial Number (from sticker on DVR)\n- Date shown on DVR\n- Proof of purchase (if asked)\n\nContact:\n- Your local CCTV supplier\n- JK Vision support\n- They will provide reset code or file',
                    'language': 'bash'
                },
                {
                    'title': 'Method 3: Hardware Reset',
                    'description': 'Physical factory reset using jumper/button.',
                    'code': 'WARNING: This erases ALL settings!\n\n1. Power OFF DVR\n2. Open DVR cover\n3. Locate reset jumper/button on motherboard\n4. Move jumper to reset position\n   OR press and hold reset button\n5. Power ON DVR\n6. Wait 30 seconds\n7. Power OFF, restore jumper\n8. Power ON - password is now default',
                    'language': 'bash'
                },
                {
                    'title': 'Set New Password',
                    'description': 'Configure new password after reset.',
                    'code': 'After Reset:\n1. Login with:\n   - Username: admin\n   - Password: (blank) OR admin OR 123456\n2. Go to: Main Menu → System → Account\n3. Select admin user → Modify\n4. Set new strong password\n5. Save and remember password!',
                    'language': 'bash'
                }
            ],
            'postInstallation': {
                'title': 'Password Security',
                'content': 'Write down new password and store safely. Avoid simple passwords like 123456. Consider creating additional user accounts with limited access for daily use.'
            }
        },
        
        # ========== General CCTV Articles ==========
        {
            'id': str(uuid.uuid4()),
            'title': 'CCTV Camera Types and Choosing Guide',
            'slug': create_slug('CCTV Camera Types and Choosing Guide'),
            'description': 'Complete guide to different types of CCTV cameras and how to choose the right one for your needs.',
            'category': 'cctv-cameras',
            'subcategory': 'general',
            'os': ['windows', 'mac'],
            'difficulty': 'beginner',
            'views': 6780,
            'likes': 145,
            'author': 'Admin',
            'createdAt': datetime.utcnow(),
            'updatedAt': datetime.utcnow(),
            'tags': ['cctv', 'camera-types', 'guide', 'buying-guide', 'security'],
            'steps': [
                {
                    'title': 'Dome Cameras',
                    'description': 'Round dome-shaped cameras for indoor use.',
                    'code': 'Dome Camera Features:\n- Shape: Round/Dome\n- Best for: Indoor, offices, shops\n- Pros:\n  * Discreet appearance\n  * Vandal resistant\n  * Wide angle view\n  * Difficult to tell direction\n- Cons:\n  * Limited range\n  * IR reflection on dome\n\nBrands: CP Plus, Hikvision, Dahua',
                    'language': 'bash'
                },
                {
                    'title': 'Bullet Cameras',
                    'description': 'Cylindrical cameras for outdoor use.',
                    'code': 'Bullet Camera Features:\n- Shape: Cylindrical/Long\n- Best for: Outdoor, parking, gates\n- Pros:\n  * Long range\n  * Better IR night vision\n  * Weather resistant (IP66/67)\n  * Visible deterrent\n- Cons:\n  * More noticeable\n  * Can be redirected\n\nBrands: CP Plus, Hikvision, TP-Link VIGI',
                    'language': 'bash'
                },
                {
                    'title': 'PTZ Cameras',
                    'description': 'Pan-Tilt-Zoom cameras for large areas.',
                    'code': 'PTZ Camera Features:\n- Movement: Pan 360°, Tilt 90°, Zoom 20-30x\n- Best for: Large areas, parking lots, stadiums\n- Pros:\n  * Cover large areas\n  * Zoom for detail\n  * Auto tracking (some models)\n  * Preset positions\n- Cons:\n  * Expensive\n  * Complex setup\n  * Moving parts can fail\n\nBrands: Hikvision, Dahua, CP Plus',
                    'language': 'bash'
                },
                {
                    'title': 'Resolution Guide',
                    'description': 'Understanding camera resolutions.',
                    'code': 'Resolution Comparison:\n\n1MP (720P) - 1280x720\n- Basic identification\n- Budget option\n\n2MP (1080P) - 1920x1080\n- Good for most uses\n- Best value\n\n4MP (2K) - 2560x1440\n- Better detail\n- License plate readable\n\n5MP - 2592x1944\n- High detail\n- Larger storage needed\n\n8MP (4K) - 3840x2160\n- Maximum detail\n- High bandwidth/storage\n\nRecommended: 2MP-4MP for most installations',
                    'language': 'bash'
                }
            ],
            'postInstallation': {
                'title': 'Buying Tips',
                'content': 'Consider: 1) Location (indoor/outdoor) 2) Coverage area 3) Night vision range 4) Storage requirements 5) Remote viewing needs 6) Budget. For homes: 4-8 cameras with 2MP-4MP. For offices: 8-16 cameras with 2MP.'
            }
        },
        {
            'id': str(uuid.uuid4()),
            'title': 'CCTV Storage Calculation - HDD Size Guide',
            'slug': create_slug('CCTV Storage Calculation HDD Size Guide'),
            'description': 'Calculate required hard drive size for CCTV recording based on cameras, resolution and retention days.',
            'category': 'cctv-cameras',
            'subcategory': 'general',
            'os': ['windows', 'mac'],
            'difficulty': 'beginner',
            'views': 4560,
            'likes': 98,
            'author': 'Admin',
            'createdAt': datetime.utcnow(),
            'updatedAt': datetime.utcnow(),
            'tags': ['cctv', 'storage', 'hdd', 'calculation', 'hard-drive'],
            'steps': [
                {
                    'title': 'Storage Formula',
                    'description': 'Basic formula for calculating storage.',
                    'code': 'Storage Formula:\n\nStorage (GB) = Bitrate (Mbps) × 3600 × Hours × Days × Cameras\n                 ─────────────────────────────────────────────\n                              8 × 1024\n\nSimplified:\nStorage (GB) = Bitrate × 0.45 × Hours × Days × Cameras',
                    'language': 'bash'
                },
                {
                    'title': 'Bitrate by Resolution',
                    'description': 'Average bitrate for different resolutions.',
                    'code': 'Typical Bitrates (Variable Bitrate):\n\n720P (1MP):  1-2 Mbps\n1080P (2MP): 2-4 Mbps\n3MP:         3-5 Mbps\n4MP:         4-6 Mbps\n5MP:         5-8 Mbps\n4K (8MP):    8-12 Mbps\n\nNote: Motion increases bitrate\nStatic scenes use less bandwidth',
                    'language': 'bash'
                },
                {
                    'title': 'Quick Reference Table',
                    'description': 'Pre-calculated storage requirements.',
                    'code': 'Storage for 30 Days Recording (24/7):\n\n         │ 4 Cameras │ 8 Cameras │ 16 Cameras\n─────────┼───────────┼───────────┼────────────\n720P     │   1 TB    │   2 TB    │    4 TB\n1080P    │   2 TB    │   4 TB    │    8 TB\n4MP      │   3 TB    │   6 TB    │   12 TB\n4K       │   5 TB    │  10 TB    │   20 TB\n\n*Based on medium quality, variable bitrate',
                    'language': 'bash'
                },
                {
                    'title': 'Recommended HDD',
                    'description': 'Surveillance-grade hard drives.',
                    'code': 'Recommended HDDs for CCTV:\n\nSeagate SkyHawk:\n- 1TB to 18TB\n- 3 year warranty\n- 24/7 operation\n- Price: ₹3,500 - ₹35,000\n\nWD Purple:\n- 1TB to 18TB\n- 3 year warranty\n- AllFrame technology\n- Price: ₹3,800 - ₹38,000\n\nToshiba S300:\n- 1TB to 10TB\n- Budget friendly\n- Price: ₹3,000 - ₹20,000\n\nAvoid: Desktop HDDs (WD Blue, Seagate Barracuda)\nNot designed for 24/7 recording',
                    'language': 'bash'
                }
            ],
            'postInstallation': {
                'title': 'Storage Tips',
                'content': 'Enable motion-based recording to save 50-70% storage. Use sub-stream for continuous recording. Set recording quality based on importance. Keep minimum 7 days retention for security purposes.'
            }
        },
        {
            'id': str(uuid.uuid4()),
            'title': 'CCTV Cable Types and Maximum Distance',
            'slug': create_slug('CCTV Cable Types and Maximum Distance'),
            'description': 'Guide to different CCTV cable types, their maximum transmission distance and when to use each.',
            'category': 'cctv-cameras',
            'subcategory': 'general',
            'os': ['windows', 'mac'],
            'difficulty': 'intermediate',
            'views': 3890,
            'likes': 76,
            'author': 'Admin',
            'createdAt': datetime.utcnow(),
            'updatedAt': datetime.utcnow(),
            'tags': ['cctv', 'cable', 'installation', 'networking', 'distance'],
            'steps': [
                {
                    'title': 'Coaxial Cable (BNC)',
                    'description': 'Traditional analog CCTV cabling.',
                    'code': 'Coaxial Cable Types:\n\nRG59:\n- Max Distance: 200m (without booster)\n- Use: Short to medium runs\n- Cost: Budget friendly\n\nRG6:\n- Max Distance: 300m\n- Use: Longer runs\n- Better shielding\n\n3+1 Cable (Common in India):\n- 3 power wires + 1 coax\n- Max: 150-200m\n- Convenient single cable',
                    'language': 'bash'
                },
                {
                    'title': 'Ethernet Cable (CAT5e/CAT6)',
                    'description': 'Network cable for IP cameras.',
                    'code': 'Ethernet Cable:\n\nCAT5e:\n- Max Distance: 100m\n- Speed: Up to 1Gbps\n- Use: Standard IP cameras\n\nCAT6:\n- Max Distance: 100m\n- Speed: Up to 10Gbps\n- Better shielding\n- Recommended for 4K cameras\n\nPoE (Power over Ethernet):\n- Single cable for video + power\n- Max: 100m (standard PoE)\n- Extended: 250m (some switches)',
                    'language': 'bash'
                },
                {
                    'title': 'Extending Distance',
                    'description': 'Methods to extend cable distance.',
                    'code': 'Distance Extension Methods:\n\n1. PoE Extender:\n   - Adds 100m per extender\n   - Chain up to 4 extenders (500m)\n   - Cost: ₹1,500-3,000 each\n\n2. Fiber Optic:\n   - Single mode: Up to 20km\n   - Multi mode: Up to 2km\n   - Media converters needed\n   - Cost: Higher but reliable\n\n3. EoC (Ethernet over Coax):\n   - Use existing coax cables\n   - Distance: Up to 500m\n   - Converts coax to Ethernet',
                    'language': 'bash'
                },
                {
                    'title': 'Cable Selection Guide',
                    'description': 'Choose the right cable for your setup.',
                    'code': 'Recommendations:\n\nAnalog HD (AHD/TVI/CVI):\n- Use: 3+1 or RG59 coax\n- Distance: Up to 200m\n\nIP Cameras:\n- Use: CAT6 with PoE\n- Distance: Up to 100m\n- Use extender for longer\n\nLong Distance (>200m):\n- Use: Fiber optic\n- Or: Wireless bridge\n\nOutdoor:\n- Use: UV resistant cables\n- Conduit protection recommended',
                    'language': 'bash'
                }
            ],
            'postInstallation': {
                'title': 'Installation Tips',
                'content': 'Always use outdoor-rated cables for external runs. Keep power and video cables separate from electrical wiring. Use cable conduits for protection. Test cables before final installation. Keep spare cable length at camera end for future adjustment.'
            }
        }
    ]
    
    # Insert articles
    for article in cctv_articles:
        existing = await db.code_snippets.find_one({'slug': article['slug']})
        if not existing:
            await db.code_snippets.insert_one(article)
            print(f"Added: {article['title']}")
        else:
            print(f"Skipped (exists): {article['title']}")
    
    print(f"\nTotal CCTV articles added: {len(cctv_articles)}")
    
    # Show category count
    count = await db.code_snippets.count_documents({'category': 'cctv-cameras'})
    print(f"Total CCTV camera articles in database: {count}")

if __name__ == "__main__":
    asyncio.run(seed_cctv_articles())
