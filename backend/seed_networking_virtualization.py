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

# Networking Articles
networking_articles = [
    {
        'title': 'Configure MikroTik Router Basic Setup',
        'description': 'Complete guide to set up MikroTik router from scratch including WAN, LAN, DHCP, and firewall configuration.',
        'category': 'networking',
        'os': ['linux'],
        'difficulty': 'intermediate',
        'tags': ['mikrotik', 'router', 'networking', 'dhcp', 'firewall'],
        'steps': [
            {
                'title': 'Access MikroTik via Winbox',
                'description': 'Download Winbox and connect to your MikroTik router.',
                'code': '# Download Winbox from MikroTik website\n# Or connect via SSH:\nssh admin@192.168.88.1',
                'language': 'bash'
            },
            {
                'title': 'Set Router Identity',
                'description': 'Give your router a meaningful name.',
                'code': '/system identity set name="Office-Router"',
                'language': 'bash'
            },
            {
                'title': 'Configure WAN Interface',
                'description': 'Set up the WAN interface with DHCP client or static IP.',
                'code': '# DHCP Client for WAN\n/ip dhcp-client add interface=ether1 disabled=no\n\n# Or Static IP\n/ip address add address=203.0.113.10/24 interface=ether1\n/ip route add gateway=203.0.113.1',
                'language': 'bash'
            },
            {
                'title': 'Configure LAN Interface',
                'description': 'Set up internal network interface.',
                'code': '/ip address add address=192.168.1.1/24 interface=ether2',
                'language': 'bash'
            },
            {
                'title': 'Setup DHCP Server',
                'description': 'Configure DHCP server for LAN clients.',
                'code': '/ip pool add name=dhcp-pool ranges=192.168.1.100-192.168.1.200\n/ip dhcp-server add name=dhcp1 interface=ether2 address-pool=dhcp-pool disabled=no\n/ip dhcp-server network add address=192.168.1.0/24 gateway=192.168.1.1 dns-server=8.8.8.8,8.8.4.4',
                'language': 'bash'
            },
            {
                'title': 'Configure NAT',
                'description': 'Enable NAT for internet access.',
                'code': '/ip firewall nat add chain=srcnat out-interface=ether1 action=masquerade',
                'language': 'bash'
            }
        ],
        'postInstallation': {
            'title': 'Verification',
            'content': 'Connect a device to LAN port, check if it receives IP via DHCP and can access internet.'
        }
    },
    {
        'title': 'TP-Link Router Setup and Configuration',
        'description': 'Step-by-step guide to configure TP-Link wireless router for home or office network.',
        'category': 'networking',
        'os': ['linux', 'windows'],
        'difficulty': 'beginner',
        'tags': ['tplink', 'router', 'wifi', 'networking', 'wireless'],
        'steps': [
            {
                'title': 'Access Router Admin Panel',
                'description': 'Connect to router and access web interface.',
                'code': '# Connect to router via ethernet or WiFi\n# Default SSID: TP-Link_XXXX\n# Open browser and go to:\nhttp://192.168.0.1\n# or\nhttp://tplinkwifi.net\n\n# Default credentials:\nUsername: admin\nPassword: admin',
                'language': 'bash'
            },
            {
                'title': 'Configure Internet Connection',
                'description': 'Set up WAN connection type based on your ISP.',
                'code': '# Navigate to: Network > WAN\n# Select Connection Type:\n# - Dynamic IP (most common)\n# - Static IP\n# - PPPoE (requires username/password from ISP)\n\n# For PPPoE:\nUsername: your_isp_username\nPassword: your_isp_password',
                'language': 'text'
            },
            {
                'title': 'Configure Wireless Settings',
                'description': 'Set up WiFi network name and security.',
                'code': '# Navigate to: Wireless > Wireless Settings\nNetwork Name (SSID): YourNetworkName\nRegion: Your Country\nChannel: Auto\nMode: 11bgn mixed\nChannel Width: Auto\n\n# Navigate to: Wireless > Wireless Security\nSecurity Type: WPA/WPA2-Personal\nPassword: YourStrongPassword123!',
                'language': 'text'
            },
            {
                'title': 'Change Admin Password',
                'description': 'Secure your router by changing default password.',
                'code': '# Navigate to: System Tools > Password\nOld Username: admin\nOld Password: admin\nNew Username: admin\nNew Password: YourNewAdminPassword!',
                'language': 'text'
            },
            {
                'title': 'Configure DHCP Settings',
                'description': 'Set up IP address range for clients.',
                'code': '# Navigate to: DHCP > DHCP Settings\nDHCP Server: Enable\nStart IP Address: 192.168.0.100\nEnd IP Address: 192.168.0.199\nLease Time: 120 minutes\nDefault Gateway: 192.168.0.1\nPrimary DNS: 8.8.8.8\nSecondary DNS: 8.8.4.4',
                'language': 'text'
            }
        ],
        'postInstallation': {
            'title': 'Final Steps',
            'content': 'Reboot the router. Connect devices to new WiFi network using the password you set.'
        }
    },
    {
        'title': 'Cisco Router Basic Configuration',
        'description': 'Learn essential Cisco IOS commands for router configuration including interfaces, routing, and security.',
        'category': 'networking',
        'os': ['linux'],
        'difficulty': 'advanced',
        'tags': ['cisco', 'router', 'networking', 'ios', 'enterprise'],
        'steps': [
            {
                'title': 'Enter Privileged Mode',
                'description': 'Access privileged EXEC mode for configuration.',
                'code': 'Router> enable\nRouter# configure terminal\nRouter(config)#',
                'language': 'bash'
            },
            {
                'title': 'Set Hostname and Domain',
                'description': 'Configure router identity.',
                'code': 'Router(config)# hostname Office-Router\nOffice-Router(config)# ip domain-name company.local',
                'language': 'bash'
            },
            {
                'title': 'Configure Interfaces',
                'description': 'Set up WAN and LAN interfaces.',
                'code': '! Configure WAN Interface\nOffice-Router(config)# interface GigabitEthernet0/0\nOffice-Router(config-if)# ip address 203.0.113.10 255.255.255.0\nOffice-Router(config-if)# no shutdown\nOffice-Router(config-if)# exit\n\n! Configure LAN Interface\nOffice-Router(config)# interface GigabitEthernet0/1\nOffice-Router(config-if)# ip address 192.168.1.1 255.255.255.0\nOffice-Router(config-if)# no shutdown\nOffice-Router(config-if)# exit',
                'language': 'bash'
            },
            {
                'title': 'Configure Default Route',
                'description': 'Set up default gateway for internet access.',
                'code': 'Office-Router(config)# ip route 0.0.0.0 0.0.0.0 203.0.113.1',
                'language': 'bash'
            },
            {
                'title': 'Configure NAT',
                'description': 'Enable Network Address Translation.',
                'code': '! Define inside and outside interfaces\nOffice-Router(config)# interface GigabitEthernet0/0\nOffice-Router(config-if)# ip nat outside\nOffice-Router(config-if)# exit\n\nOffice-Router(config)# interface GigabitEthernet0/1\nOffice-Router(config-if)# ip nat inside\nOffice-Router(config-if)# exit\n\n! Create access list and NAT rule\nOffice-Router(config)# access-list 1 permit 192.168.1.0 0.0.0.255\nOffice-Router(config)# ip nat inside source list 1 interface GigabitEthernet0/0 overload',
                'language': 'bash'
            },
            {
                'title': 'Save Configuration',
                'description': 'Save running configuration to startup.',
                'code': 'Office-Router# copy running-config startup-config\nDestination filename [startup-config]? [Enter]\nBuilding configuration...\n[OK]',
                'language': 'bash'
            }
        ],
        'postInstallation': {
            'title': 'Verification Commands',
            'content': 'Use "show ip interface brief" to verify interfaces, "show ip route" to check routing table, and "show running-config" to review configuration.'
        }
    },
    {
        'title': 'Setup OpenWrt on Router',
        'description': 'Install and configure OpenWrt firmware on compatible routers for advanced features.',
        'category': 'networking',
        'os': ['linux'],
        'difficulty': 'advanced',
        'tags': ['openwrt', 'router', 'firmware', 'linux', 'opensource'],
        'steps': [
            {
                'title': 'Check Router Compatibility',
                'description': 'Verify your router supports OpenWrt.',
                'code': '# Visit OpenWrt Table of Hardware:\nhttps://openwrt.org/toh/start\n\n# Search for your router model\n# Download the correct firmware image',
                'language': 'bash'
            },
            {
                'title': 'Backup Original Firmware',
                'description': 'Save stock firmware before flashing.',
                'code': '# Access router admin panel\n# Go to System > Backup\n# Download backup file\n# Note: Keep this backup safe for recovery',
                'language': 'text'
            },
            {
                'title': 'Flash OpenWrt Firmware',
                'description': 'Install OpenWrt on your router.',
                'code': '# In router admin panel:\n# Go to System > Firmware Upgrade\n# Upload the OpenWrt .bin file\n# Click Upgrade and wait 3-5 minutes\n# DO NOT power off during flashing!\n\n# Or via TFTP (advanced):\ntftp 192.168.1.1\nput openwrt-firmware.bin\nquit',
                'language': 'bash'
            },
            {
                'title': 'Initial OpenWrt Setup',
                'description': 'Access and configure OpenWrt.',
                'code': '# Connect to router via ethernet\n# Default IP: 192.168.1.1\n# Open browser: http://192.168.1.1\n# Default: no password\n\n# Or via SSH:\nssh root@192.168.1.1',
                'language': 'bash'
            },
            {
                'title': 'Set Root Password',
                'description': 'Secure the router with a password.',
                'code': '# Via LuCI (web interface):\n# Go to System > Administration\n# Set Router Password\n\n# Or via SSH:\npasswd\n# Enter new password twice',
                'language': 'bash'
            },
            {
                'title': 'Configure WAN and WiFi',
                'description': 'Set up internet and wireless.',
                'code': '# Via LuCI:\n# Network > Interfaces > WAN\n# Set Protocol: DHCP client (or PPPoE)\n\n# Network > Wireless\n# Click "Edit" on your radio\n# Set ESSID (network name)\n# Set Encryption: WPA2-PSK\n# Set Key (password)\n# Enable the interface',
                'language': 'text'
            }
        ],
        'postInstallation': {
            'title': 'Post Installation',
            'content': 'Update packages with "opkg update", install LuCI if not included with "opkg install luci", and explore additional packages for VPN, QoS, and more.'
        }
    },
    {
        'title': 'Configure VPN Server with WireGuard',
        'description': 'Set up a modern, fast VPN server using WireGuard on Linux.',
        'category': 'networking',
        'os': ['ubuntu', 'debian', 'centos', 'linux'],
        'difficulty': 'intermediate',
        'tags': ['wireguard', 'vpn', 'networking', 'security', 'tunnel'],
        'steps': [
            {
                'title': 'Install WireGuard',
                'description': 'Install WireGuard packages.',
                'code': '# Ubuntu/Debian\nsudo apt update\nsudo apt install wireguard -y\n\n# CentOS/RHEL 8+\nsudo dnf install epel-release -y\nsudo dnf install wireguard-tools -y',
                'language': 'bash'
            },
            {
                'title': 'Generate Server Keys',
                'description': 'Create private and public keys for server.',
                'code': '# Create directory\nsudo mkdir -p /etc/wireguard\ncd /etc/wireguard\n\n# Generate keys\nwg genkey | sudo tee server_private.key\ncat server_private.key | wg pubkey | sudo tee server_public.key\n\n# Secure private key\nsudo chmod 600 server_private.key',
                'language': 'bash'
            },
            {
                'title': 'Create Server Configuration',
                'description': 'Configure WireGuard server interface.',
                'code': 'sudo nano /etc/wireguard/wg0.conf\n\n# Add the following:\n[Interface]\nAddress = 10.0.0.1/24\nListenPort = 51820\nPrivateKey = <server_private_key>\n\n# Enable IP forwarding\nPostUp = iptables -A FORWARD -i wg0 -j ACCEPT; iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE\nPostDown = iptables -D FORWARD -i wg0 -j ACCEPT; iptables -t nat -D POSTROUTING -o eth0 -j MASQUERADE',
                'language': 'bash'
            },
            {
                'title': 'Enable IP Forwarding',
                'description': 'Allow packet forwarding for VPN traffic.',
                'code': '# Enable immediately\nsudo sysctl -w net.ipv4.ip_forward=1\n\n# Make permanent\necho "net.ipv4.ip_forward=1" | sudo tee -a /etc/sysctl.conf\nsudo sysctl -p',
                'language': 'bash'
            },
            {
                'title': 'Generate Client Keys',
                'description': 'Create keys for VPN client.',
                'code': '# Generate client keys\nwg genkey | tee client_private.key\ncat client_private.key | wg pubkey | tee client_public.key',
                'language': 'bash'
            },
            {
                'title': 'Add Client to Server Config',
                'description': 'Add peer section for the client.',
                'code': '# Add to /etc/wireguard/wg0.conf:\n\n[Peer]\nPublicKey = <client_public_key>\nAllowedIPs = 10.0.0.2/32',
                'language': 'bash'
            },
            {
                'title': 'Start WireGuard',
                'description': 'Enable and start the VPN service.',
                'code': '# Start WireGuard\nsudo wg-quick up wg0\n\n# Enable on boot\nsudo systemctl enable wg-quick@wg0\n\n# Check status\nsudo wg show',
                'language': 'bash'
            }
        ],
        'postInstallation': {
            'title': 'Client Configuration',
            'content': 'Create client config file with server public key and endpoint. Use WireGuard app on Windows, macOS, iOS, or Android to connect.'
        }
    },
    {
        'title': 'Setup OpenVPN Server on Ubuntu',
        'description': 'Install and configure OpenVPN server with certificate-based authentication.',
        'category': 'networking',
        'os': ['ubuntu', 'debian'],
        'difficulty': 'intermediate',
        'tags': ['openvpn', 'vpn', 'networking', 'security', 'ssl'],
        'steps': [
            {
                'title': 'Install OpenVPN and Easy-RSA',
                'description': 'Install required packages.',
                'code': 'sudo apt update\nsudo apt install openvpn easy-rsa -y',
                'language': 'bash'
            },
            {
                'title': 'Setup CA Directory',
                'description': 'Create Certificate Authority structure.',
                'code': 'make-cadir ~/openvpn-ca\ncd ~/openvpn-ca',
                'language': 'bash'
            },
            {
                'title': 'Configure CA Variables',
                'description': 'Edit vars file with your information.',
                'code': 'nano vars\n\n# Modify these lines:\nset_var EASYRSA_REQ_COUNTRY    "US"\nset_var EASYRSA_REQ_PROVINCE   "California"\nset_var EASYRSA_REQ_CITY       "San Francisco"\nset_var EASYRSA_REQ_ORG        "MyOrganization"\nset_var EASYRSA_REQ_EMAIL      "admin@example.com"\nset_var EASYRSA_REQ_OU         "IT Department"',
                'language': 'bash'
            },
            {
                'title': 'Build CA and Server Certificates',
                'description': 'Generate all required certificates.',
                'code': '# Initialize PKI\n./easyrsa init-pki\n\n# Build CA\n./easyrsa build-ca nopass\n\n# Generate server certificate\n./easyrsa gen-req server nopass\n./easyrsa sign-req server server\n\n# Generate Diffie-Hellman parameters\n./easyrsa gen-dh\n\n# Generate TLS auth key\nopenvpn --genkey secret ta.key',
                'language': 'bash'
            },
            {
                'title': 'Copy Files to OpenVPN Directory',
                'description': 'Move certificates to OpenVPN config.',
                'code': 'sudo cp pki/ca.crt /etc/openvpn/\nsudo cp pki/issued/server.crt /etc/openvpn/\nsudo cp pki/private/server.key /etc/openvpn/\nsudo cp pki/dh.pem /etc/openvpn/\nsudo cp ta.key /etc/openvpn/',
                'language': 'bash'
            },
            {
                'title': 'Create Server Configuration',
                'description': 'Configure OpenVPN server.',
                'code': 'sudo nano /etc/openvpn/server.conf\n\n# Add configuration:\nport 1194\nproto udp\ndev tun\nca ca.crt\ncert server.crt\nkey server.key\ndh dh.pem\nserver 10.8.0.0 255.255.255.0\npush "redirect-gateway def1 bypass-dhcp"\npush "dhcp-option DNS 8.8.8.8"\nkeepalive 10 120\ntls-auth ta.key 0\ncipher AES-256-CBC\nuser nobody\ngroup nogroup\npersist-key\npersist-tun\nstatus /var/log/openvpn-status.log\nverb 3',
                'language': 'bash'
            },
            {
                'title': 'Start OpenVPN Server',
                'description': 'Enable and start the service.',
                'code': 'sudo systemctl start openvpn@server\nsudo systemctl enable openvpn@server\nsudo systemctl status openvpn@server',
                'language': 'bash'
            }
        ],
        'postInstallation': {
            'title': 'Generate Client Certificates',
            'content': 'Use "./easyrsa gen-req client1 nopass" and "./easyrsa sign-req client client1" to create client certificates. Distribute ca.crt, client1.crt, client1.key, and ta.key to clients.'
        }
    },
    {
        'title': 'Configure pfSense Firewall Router',
        'description': 'Complete guide to installing and configuring pfSense as your network firewall and router.',
        'category': 'networking',
        'os': ['linux'],
        'difficulty': 'advanced',
        'tags': ['pfsense', 'firewall', 'router', 'networking', 'security'],
        'steps': [
            {
                'title': 'Download pfSense ISO',
                'description': 'Get the pfSense installation image.',
                'code': '# Download from official website:\nhttps://www.pfsense.org/download/\n\n# Select:\n# Architecture: AMD64\n# Installer: DVD Image (ISO)\n# Mirror: Choose nearest location',
                'language': 'text'
            },
            {
                'title': 'Install pfSense',
                'description': 'Boot from ISO and complete installation.',
                'code': '# Boot from USB/DVD\n# Select "Install"\n# Choose filesystem: ZFS or UFS\n# Select target disk\n# Complete installation\n# Remove installation media\n# Reboot',
                'language': 'text'
            },
            {
                'title': 'Initial Console Setup',
                'description': 'Configure interfaces from console.',
                'code': '# When prompted:\n# Assign WAN interface: Select WAN NIC\n# Assign LAN interface: Select LAN NIC\n# Set interface IP addresses:\n#   LAN: 192.168.1.1/24\n#   WAN: DHCP or Static based on ISP',
                'language': 'text'
            },
            {
                'title': 'Access Web Interface',
                'description': 'Connect to pfSense web GUI.',
                'code': '# Connect computer to LAN port\n# Open browser:\nhttps://192.168.1.1\n\n# Default credentials:\nUsername: admin\nPassword: pfsense',
                'language': 'text'
            },
            {
                'title': 'Complete Setup Wizard',
                'description': 'Configure basic settings.',
                'code': '# Setup Wizard steps:\n1. Hostname: pfsense\n2. Domain: home.local\n3. Primary DNS: 8.8.8.8\n4. Secondary DNS: 8.8.4.4\n5. Timezone: Select your zone\n6. WAN Configuration: Based on ISP\n7. LAN Configuration: 192.168.1.1/24\n8. Admin Password: Change from default!',
                'language': 'text'
            },
            {
                'title': 'Configure Firewall Rules',
                'description': 'Set up basic firewall rules.',
                'code': '# Navigate to: Firewall > Rules > LAN\n# Default rule allows all LAN to any\n\n# Navigate to: Firewall > Rules > WAN\n# By default, all incoming blocked\n\n# To allow SSH from WAN:\n# Add rule: Action: Pass\n# Interface: WAN\n# Protocol: TCP\n# Destination Port: 22',
                'language': 'text'
            }
        ],
        'postInstallation': {
            'title': 'Additional Configuration',
            'content': 'Enable NAT under Firewall > NAT > Outbound. Configure DHCP Server under Services > DHCP Server. Set up VPN under VPN menu. Enable traffic shaping under Firewall > Traffic Shaper.'
        }
    },
    {
        'title': 'Setup VLAN on Managed Switch',
        'description': 'Configure VLANs on a managed network switch for network segmentation.',
        'category': 'networking',
        'os': ['linux'],
        'difficulty': 'intermediate',
        'tags': ['vlan', 'switch', 'networking', 'segmentation', 'enterprise'],
        'steps': [
            {
                'title': 'Access Switch Management',
                'description': 'Connect to switch admin interface.',
                'code': '# Via Web Interface:\n# Connect PC to switch management port\n# Default IPs vary by manufacturer:\n# - TP-Link: 192.168.0.1\n# - Netgear: 192.168.0.239\n# - Cisco: 192.168.1.254\n# - HP: 192.168.1.1\n\n# Via SSH (if enabled):\nssh admin@switch_ip',
                'language': 'bash'
            },
            {
                'title': 'Plan VLAN Structure',
                'description': 'Design your VLAN layout.',
                'code': '# Example VLAN plan:\n# VLAN 10 - Management (192.168.10.0/24)\n# VLAN 20 - Staff (192.168.20.0/24)\n# VLAN 30 - Guests (192.168.30.0/24)\n# VLAN 40 - Servers (192.168.40.0/24)\n# VLAN 50 - IoT Devices (192.168.50.0/24)',
                'language': 'text'
            },
            {
                'title': 'Create VLANs',
                'description': 'Add VLANs to the switch.',
                'code': '# Cisco IOS Example:\nenable\nconfigure terminal\nvlan 10\nname Management\nexit\nvlan 20\nname Staff\nexit\nvlan 30\nname Guests\nexit\nend\nwrite memory',
                'language': 'bash'
            },
            {
                'title': 'Configure Access Ports',
                'description': 'Assign switch ports to VLANs.',
                'code': '# Cisco IOS - Access port (single VLAN):\nconfigure terminal\ninterface GigabitEthernet0/1\nswitchport mode access\nswitchport access vlan 20\nexit\n\n# Repeat for other ports:\ninterface range GigabitEthernet0/2-10\nswitchport mode access\nswitchport access vlan 20\nexit',
                'language': 'bash'
            },
            {
                'title': 'Configure Trunk Ports',
                'description': 'Set up trunk ports for router/switch connections.',
                'code': '# Cisco IOS - Trunk port (multiple VLANs):\nconfigure terminal\ninterface GigabitEthernet0/24\nswitchport mode trunk\nswitchport trunk allowed vlan 10,20,30,40,50\nswitchport trunk native vlan 10\nexit\nend\nwrite memory',
                'language': 'bash'
            },
            {
                'title': 'Verify VLAN Configuration',
                'description': 'Check VLAN setup.',
                'code': '# Show all VLANs:\nshow vlan brief\n\n# Show trunk ports:\nshow interfaces trunk\n\n# Show specific interface:\nshow interfaces GigabitEthernet0/1 switchport',
                'language': 'bash'
            }
        ],
        'postInstallation': {
            'title': 'Router Configuration',
            'content': 'Configure router-on-a-stick or Layer 3 switch for inter-VLAN routing. Each VLAN needs a gateway IP on the router. Configure DHCP scopes for each VLAN subnet.'
        }
    },
    {
        'title': 'Network Troubleshooting Commands',
        'description': 'Essential network diagnostic commands for troubleshooting connectivity issues.',
        'category': 'networking',
        'os': ['linux', 'ubuntu', 'centos', 'debian'],
        'difficulty': 'beginner',
        'tags': ['networking', 'troubleshooting', 'diagnostics', 'commands'],
        'steps': [
            {
                'title': 'Check Network Interfaces',
                'description': 'View network interface configuration.',
                'code': '# Show all interfaces\nip addr show\n\n# Legacy command\nifconfig -a\n\n# Show specific interface\nip addr show eth0',
                'language': 'bash'
            },
            {
                'title': 'Test Connectivity with Ping',
                'description': 'Check if hosts are reachable.',
                'code': '# Ping IP address\nping -c 4 8.8.8.8\n\n# Ping hostname\nping -c 4 google.com\n\n# Continuous ping (stop with Ctrl+C)\nping 192.168.1.1',
                'language': 'bash'
            },
            {
                'title': 'Trace Network Path',
                'description': 'See the route packets take.',
                'code': '# Traceroute (install if needed: apt install traceroute)\ntraceroute google.com\n\n# MTR - Better traceroute (apt install mtr)\nmtr google.com\n\n# Windows equivalent\ntracert google.com',
                'language': 'bash'
            },
            {
                'title': 'Check DNS Resolution',
                'description': 'Test DNS lookup.',
                'code': '# Using dig\ndig google.com\ndig google.com +short\n\n# Using nslookup\nnslookup google.com\n\n# Check specific DNS server\ndig @8.8.8.8 google.com',
                'language': 'bash'
            },
            {
                'title': 'View Open Ports',
                'description': 'Check listening ports and connections.',
                'code': '# Show listening ports\nss -tuln\n\n# Show all connections with process names\nss -tulnp\n\n# Legacy netstat\nnetstat -tuln\n\n# Check if specific port is open\nss -tuln | grep :80',
                'language': 'bash'
            },
            {
                'title': 'Check Routing Table',
                'description': 'View network routes.',
                'code': '# Show routing table\nip route show\n\n# Legacy command\nroute -n\n\n# Show route to specific destination\nip route get 8.8.8.8',
                'language': 'bash'
            },
            {
                'title': 'Test TCP Connection',
                'description': 'Check if TCP port is accessible.',
                'code': '# Using netcat\nnc -zv 192.168.1.1 22\nnc -zv google.com 443\n\n# Using telnet\ntelnet 192.168.1.1 22\n\n# Scan port range\nnc -zv 192.168.1.1 20-25',
                'language': 'bash'
            }
        ],
        'postInstallation': {
            'title': 'Additional Tools',
            'content': 'Install tcpdump for packet capture, Wireshark for GUI analysis, iftop for bandwidth monitoring, and nethogs for per-process network usage.'
        }
    },
    {
        'title': 'Configure UniFi Network Controller',
        'description': 'Set up Ubiquiti UniFi Controller for managing UniFi access points and network devices.',
        'category': 'networking',
        'os': ['ubuntu', 'debian'],
        'difficulty': 'intermediate',
        'tags': ['unifi', 'ubiquiti', 'wifi', 'networking', 'controller'],
        'steps': [
            {
                'title': 'Install Prerequisites',
                'description': 'Install Java and MongoDB requirements.',
                'code': 'sudo apt update\nsudo apt install ca-certificates apt-transport-https -y\n\n# Install Java\nsudo apt install openjdk-11-jre-headless -y\n\n# Install MongoDB (required for UniFi)\nwget -qO - https://www.mongodb.org/static/pgp/server-4.4.asc | sudo apt-key add -\necho "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/4.4 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-4.4.list\nsudo apt update\nsudo apt install mongodb-org -y',
                'language': 'bash'
            },
            {
                'title': 'Add UniFi Repository',
                'description': 'Add Ubiquiti APT repository.',
                'code': '# Add UniFi GPG key\nwget -qO - https://dl.ui.com/unifi/unifi-repo.gpg | sudo apt-key add -\n\n# Add repository\necho "deb https://www.ui.com/downloads/unifi/debian stable ubiquiti" | sudo tee /etc/apt/sources.list.d/100-ubnt-unifi.list',
                'language': 'bash'
            },
            {
                'title': 'Install UniFi Controller',
                'description': 'Install the UniFi Network Application.',
                'code': 'sudo apt update\nsudo apt install unifi -y',
                'language': 'bash'
            },
            {
                'title': 'Start UniFi Service',
                'description': 'Enable and start the controller.',
                'code': 'sudo systemctl enable unifi\nsudo systemctl start unifi\nsudo systemctl status unifi',
                'language': 'bash'
            },
            {
                'title': 'Configure Firewall',
                'description': 'Allow UniFi required ports.',
                'code': '# Required ports:\nsudo ufw allow 8443/tcp   # Controller GUI\nsudo ufw allow 8080/tcp   # Device communication\nsudo ufw allow 3478/udp   # STUN\nsudo ufw allow 10001/udp  # Device discovery\nsudo ufw allow 6789/tcp   # Speed test\nsudo ufw reload',
                'language': 'bash'
            },
            {
                'title': 'Access UniFi Controller',
                'description': 'Complete initial setup via web interface.',
                'code': '# Wait 2-3 minutes for service to start\n# Open browser:\nhttps://your_server_ip:8443\n\n# Complete setup wizard:\n# 1. Create admin account\n# 2. Set controller name\n# 3. Configure WiFi networks\n# 4. Adopt discovered devices',
                'language': 'text'
            }
        ],
        'postInstallation': {
            'title': 'Device Adoption',
            'content': 'UniFi devices on the same network will auto-discover. For devices on different networks, SSH to device and run: set-inform http://controller_ip:8080/inform'
        }
    }
]

# Virtualization Articles (SolusVM & Virtualizor)
virtualization_articles = [
    {
        'title': 'Install SolusVM Master on CentOS',
        'description': 'Complete guide to install SolusVM virtualization management panel master server.',
        'category': 'virtualization',
        'os': ['centos', 'linux'],
        'difficulty': 'advanced',
        'tags': ['solusvm', 'virtualization', 'vps', 'master', 'hosting'],
        'steps': [
            {
                'title': 'System Requirements',
                'description': 'Verify server meets minimum requirements.',
                'code': '# Minimum Requirements:\n# - CentOS 7 64-bit\n# - 2GB RAM minimum (4GB recommended)\n# - 20GB disk space\n# - Static IP address\n# - Valid SolusVM license\n\n# Check system:\ncat /etc/centos-release\nfree -h\ndf -h',
                'language': 'bash'
            },
            {
                'title': 'Prepare Server',
                'description': 'Update system and set hostname.',
                'code': '# Update system\nyum update -y\n\n# Set hostname (FQDN required)\nhostnamectl set-hostname master.yourdomain.com\n\n# Edit hosts file\necho "YOUR_IP master.yourdomain.com master" >> /etc/hosts\n\n# Disable SELinux\nsetenforce 0\nsed -i \'s/SELINUX=enforcing/SELINUX=disabled/g\' /etc/selinux/config',
                'language': 'bash'
            },
            {
                'title': 'Install SolusVM Master',
                'description': 'Download and run SolusVM installer.',
                'code': '# Download installer\nwget https://files.soluslabs.com/install.sh\n\n# Make executable\nchmod +x install.sh\n\n# Run installer and select Master\n./install.sh\n\n# When prompted:\n# Select: 1 (Install Master)\n# Enter license key when asked',
                'language': 'bash'
            },
            {
                'title': 'Configure Firewall',
                'description': 'Allow SolusVM required ports.',
                'code': '# Allow SolusVM ports\nfirewall-cmd --permanent --add-port=5353/tcp  # Master\nfirewall-cmd --permanent --add-port=5656/tcp  # Master\nfirewall-cmd --permanent --add-port=80/tcp    # HTTP\nfirewall-cmd --permanent --add-port=443/tcp   # HTTPS\nfirewall-cmd --reload',
                'language': 'bash'
            },
            {
                'title': 'Access SolusVM Admin',
                'description': 'Login to SolusVM admin panel.',
                'code': '# Admin Panel URL:\nhttps://your_server_ip:5656/admincp\n\n# Default credentials:\nUsername: vpsadmin\nPassword: vpsadmin\n\n# IMPORTANT: Change password immediately!',
                'language': 'text'
            },
            {
                'title': 'Initial Configuration',
                'description': 'Complete initial setup in admin panel.',
                'code': '# In Admin Panel:\n1. Go to Configuration > Settings\n2. Set Master URL (https://master.yourdomain.com:5656)\n3. Configure email settings for notifications\n4. Set default nameservers\n5. Configure IP pools',
                'language': 'text'
            }
        ],
        'postInstallation': {
            'title': 'Next Steps',
            'content': 'Add slave nodes for KVM/OpenVZ/Xen virtualization. Configure IP address pools. Create VPS plans and templates. Integrate with WHMCS for billing.'
        }
    },
    {
        'title': 'Install SolusVM Slave Node (KVM)',
        'description': 'Set up SolusVM KVM slave node for creating virtual machines.',
        'category': 'virtualization',
        'os': ['centos', 'linux'],
        'difficulty': 'advanced',
        'tags': ['solusvm', 'kvm', 'virtualization', 'slave', 'vps'],
        'steps': [
            {
                'title': 'Check Hardware Virtualization',
                'description': 'Verify CPU supports virtualization.',
                'code': '# Check for virtualization support\negrep -c \'(vmx|svm)\' /proc/cpuinfo\n\n# If output is 0, virtualization is not supported\n# If output is > 0, virtualization is available\n\n# Check if KVM modules loaded\nlsmod | grep kvm',
                'language': 'bash'
            },
            {
                'title': 'Prepare Slave Server',
                'description': 'Update system and install dependencies.',
                'code': '# Update system\nyum update -y\n\n# Set hostname\nhostnamectl set-hostname slave1.yourdomain.com\necho "SLAVE_IP slave1.yourdomain.com slave1" >> /etc/hosts\n\n# Disable SELinux\nsetenforce 0\nsed -i \'s/SELINUX=enforcing/SELINUX=disabled/g\' /etc/selinux/config',
                'language': 'bash'
            },
            {
                'title': 'Install SolusVM Slave',
                'description': 'Run installer and select KVM slave.',
                'code': '# Download installer\nwget https://files.soluslabs.com/install.sh\nchmod +x install.sh\n\n# Run installer\n./install.sh\n\n# Select: 2 (Install Slave)\n# Select: 2 (KVM)\n# Enter Master IP when prompted\n# Enter ID Key and ID Password from Master',
                'language': 'bash'
            },
            {
                'title': 'Configure Storage',
                'description': 'Set up storage for virtual machines.',
                'code': '# Create LVM volume group for VMs\npvcreate /dev/sdb\nvgcreate vps /dev/sdb\n\n# Or use directory-based storage:\nmkdir -p /home/solusvm/kvm\n\n# Configure in SolusVM Master:\n# Node > Edit > Storage Type: LVM or File',
                'language': 'bash'
            },
            {
                'title': 'Configure Network Bridge',
                'description': 'Set up network bridge for VMs.',
                'code': '# Create bridge configuration\ncat > /etc/sysconfig/network-scripts/ifcfg-br0 << EOF\nDEVICE=br0\nTYPE=Bridge\nBOOTPROTO=static\nIPADDR=YOUR_SERVER_IP\nNETMASK=255.255.255.0\nGATEWAY=YOUR_GATEWAY\nONBOOT=yes\nNM_CONTROLLED=no\nEOF\n\n# Modify eth0 to use bridge\ncat > /etc/sysconfig/network-scripts/ifcfg-eth0 << EOF\nDEVICE=eth0\nBRIDGE=br0\nONBOOT=yes\nNM_CONTROLLED=no\nEOF\n\nsystemctl restart network',
                'language': 'bash'
            },
            {
                'title': 'Add Node to Master',
                'description': 'Register slave in SolusVM Master.',
                'code': '# In SolusVM Master Admin Panel:\n1. Go to Nodes > Add Node\n2. Name: Slave1-KVM\n3. Type: KVM\n4. IP Address: Slave server IP\n5. ID Key: (from slave installation)\n6. ID Password: (from slave installation)\n7. Click Add Node',
                'language': 'text'
            }
        ],
        'postInstallation': {
            'title': 'Verification',
            'content': 'Check node status in Master panel. Sync templates from media library. Add IP addresses to the node. Create test VPS to verify setup.'
        }
    },
    {
        'title': 'Install Virtualizor on CentOS',
        'description': 'Complete installation guide for Virtualizor VPS control panel.',
        'category': 'virtualization',
        'os': ['centos', 'linux'],
        'difficulty': 'advanced',
        'tags': ['virtualizor', 'virtualization', 'vps', 'hosting', 'panel'],
        'steps': [
            {
                'title': 'System Requirements',
                'description': 'Verify server specifications.',
                'code': '# Requirements:\n# - CentOS 7/8 or AlmaLinux/Rocky\n# - 4GB RAM minimum\n# - 50GB disk space\n# - Hardware virtualization (VT-x/AMD-V)\n# - Valid Virtualizor license\n\n# Check virtualization:\negrep -c \'(vmx|svm)\' /proc/cpuinfo',
                'language': 'bash'
            },
            {
                'title': 'Prepare Server',
                'description': 'Update system and set hostname.',
                'code': '# Update system\nyum update -y\n\n# Set hostname\nhostnamectl set-hostname virt.yourdomain.com\n\n# Update hosts file\necho "YOUR_IP virt.yourdomain.com virt" >> /etc/hosts\n\n# Disable SELinux\nsetenforce 0\nsed -i \'s/SELINUX=enforcing/SELINUX=disabled/g\' /etc/selinux/config',
                'language': 'bash'
            },
            {
                'title': 'Download and Install Virtualizor',
                'description': 'Run the Virtualizor installer script.',
                'code': '# Download installer\nwget -N http://files.virtualizor.com/install.sh\n\n# Run installer for KVM\nsh install.sh email=your@email.com kernel=kvm\n\n# For OpenVZ 7:\nsh install.sh email=your@email.com kernel=openvz\n\n# For LXC:\nsh install.sh email=your@email.com kernel=lxc\n\n# Wait for installation (20-40 minutes)',
                'language': 'bash'
            },
            {
                'title': 'Access Admin Panel',
                'description': 'Login to Virtualizor admin interface.',
                'code': '# Admin Panel URL:\nhttps://your_server_ip:4085\n\n# Default credentials:\nUsername: admin\nPassword: (shown at end of installation)\n\n# API credentials saved at:\ncat /etc/virtualizor/master.php',
                'language': 'text'
            },
            {
                'title': 'Configure Storage',
                'description': 'Set up storage for virtual machines.',
                'code': '# In Admin Panel:\n1. Go to Storage > Add Storage\n\n# For LVM:\n# Create volume group first:\npvcreate /dev/sdb\nvgcreate vg /dev/sdb\n\n# In panel:\nName: Primary-Storage\nPath: vg (volume group name)\nType: LVM Thin\n\n# For File Storage:\nName: File-Storage\nPath: /var/virtualizor\nType: File',
                'language': 'bash'
            },
            {
                'title': 'Add IP Pool',
                'description': 'Configure IP addresses for VPS.',
                'code': '# In Admin Panel:\n1. Go to IPs > Add IPv4\n\n# Single IP:\nFirst IP: 192.168.1.100\nNum IPs: 1\nNetmask: 255.255.255.0\nGateway: 192.168.1.1\n\n# IP Range:\nFirst IP: 192.168.1.100\nLast IP: 192.168.1.150\nNetmask: 255.255.255.0\nGateway: 192.168.1.1',
                'language': 'text'
            },
            {
                'title': 'Download OS Templates',
                'description': 'Get operating system templates.',
                'code': '# In Admin Panel:\n1. Go to Media > OS Templates\n2. Click "OS Template Recipes"\n3. Select templates to download:\n   - CentOS 7 x86_64\n   - Ubuntu 20.04 x86_64\n   - Debian 11 x86_64\n   - Windows Server (if licensed)\n4. Click Download',
                'language': 'text'
            }
        ],
        'postInstallation': {
            'title': 'Next Steps',
            'content': 'Create VPS plans under Plans menu. Set up user groups for resellers. Configure email templates. Integrate with WHMCS/Blesta for billing automation.'
        }
    },
    {
        'title': 'Virtualizor KVM VPS Creation',
        'description': 'Step-by-step guide to create and manage KVM virtual machines in Virtualizor.',
        'category': 'virtualization',
        'os': ['centos', 'linux'],
        'difficulty': 'intermediate',
        'tags': ['virtualizor', 'kvm', 'vps', 'virtual-machine', 'hosting'],
        'steps': [
            {
                'title': 'Create VPS Plan',
                'description': 'Define resource allocation for VPS.',
                'code': '# In Admin Panel > Plans > Add Plan\n\nPlan Name: Basic-KVM\nVirtualization: KVM\nDisk Space: 20 GB\nGuaranteed RAM: 1024 MB\nSwap: 1024 MB\nCPU Cores: 1\nCPU Weight: 1024\nBandwidth: 1000 GB\nNetwork Speed: 100 Mbps\nNumber of IPs: 1',
                'language': 'text'
            },
            {
                'title': 'Create VPS via Admin Panel',
                'description': 'Create a new virtual machine.',
                'code': '# Go to List VPS > Create VPS\n\n# Basic Settings:\nNode: Select your server\nUser: Admin or create user\nPlan: Basic-KVM\nOS: CentOS-7-x86_64\nHostname: vps1.example.com\n\n# Password: Set root password\n# IP: Select from pool\n# Click Create VPS',
                'language': 'text'
            },
            {
                'title': 'Create VPS via API',
                'description': 'Automate VPS creation using API.',
                'code': '# API endpoint\nPOST https://your_server:4085/index.php?act=addvs\n\n# Required parameters:\ncurl -k -X POST "https://server:4085/index.php?act=addvs" \\\n  -d "api_key=YOUR_API_KEY" \\\n  -d "api_pass=YOUR_API_PASS" \\\n  -d "user_email=user@example.com" \\\n  -d "user_pass=UserPassword123" \\\n  -d "fname=John" \\\n  -d "lname=Doe" \\\n  -d "hostname=vps1.example.com" \\\n  -d "rootpass=RootPassword123" \\\n  -d "osid=270" \\\n  -d "plid=1" \\\n  -d "ips=1"',
                'language': 'bash'
            },
            {
                'title': 'Manage VPS Operations',
                'description': 'Common VPS management tasks.',
                'code': '# Start VPS\nvirt-manager start <vpsid>\n\n# Stop VPS\nvirt-manager stop <vpsid>\n\n# Restart VPS\nvirt-manager restart <vpsid>\n\n# Or via Admin Panel:\n# List VPS > Select VPS > Power Options',
                'language': 'bash'
            },
            {
                'title': 'Access VPS Console',
                'description': 'Connect to VPS via VNC console.',
                'code': '# In Admin Panel:\n1. Go to List VPS\n2. Click on VPS hostname\n3. Click "VNC" button\n4. Java/noVNC console opens\n\n# Via SSH (after VPS is running):\nssh root@vps_ip_address',
                'language': 'text'
            },
            {
                'title': 'Backup and Restore',
                'description': 'Create and restore VPS backups.',
                'code': '# Enable backups in Plan settings:\n# Plans > Edit Plan > Enable Backups\n\n# Create backup:\n# List VPS > Select VPS > Backups > Create Backup\n\n# Restore backup:\n# List VPS > Select VPS > Backups > Select backup > Restore\n\n# CLI backup:\n/usr/local/emps/bin/php /usr/local/virtualizor/scripts/backup_vps.php <vpsid>',
                'language': 'bash'
            }
        ],
        'postInstallation': {
            'title': 'VPS Management Tips',
            'content': 'Enable automatic backups for important VPS. Monitor resource usage through VPS stats. Set up email alerts for high usage. Use templates for faster deployment.'
        }
    },
    {
        'title': 'Setup Proxmox VE Cluster',
        'description': 'Install and configure Proxmox Virtual Environment for enterprise virtualization.',
        'category': 'virtualization',
        'os': ['debian', 'linux'],
        'difficulty': 'advanced',
        'tags': ['proxmox', 'virtualization', 'cluster', 'enterprise', 'kvm'],
        'steps': [
            {
                'title': 'Download Proxmox VE ISO',
                'description': 'Get the Proxmox installation image.',
                'code': '# Download from official website:\nhttps://www.proxmox.com/en/downloads\n\n# Or via wget:\nwget https://enterprise.proxmox.com/iso/proxmox-ve_8.0-1.iso\n\n# Create bootable USB:\ndd if=proxmox-ve_8.0-1.iso of=/dev/sdX bs=4M status=progress',
                'language': 'bash'
            },
            {
                'title': 'Install Proxmox VE',
                'description': 'Complete installation wizard.',
                'code': '# Boot from ISO\n# Select "Install Proxmox VE"\n\n# Installation steps:\n1. Accept EULA\n2. Select target disk\n3. Country, timezone, keyboard\n4. Set root password and email\n5. Network configuration:\n   - Hostname: pve1.local\n   - IP: 192.168.1.100/24\n   - Gateway: 192.168.1.1\n   - DNS: 8.8.8.8\n6. Complete installation and reboot',
                'language': 'text'
            },
            {
                'title': 'Access Web Interface',
                'description': 'Login to Proxmox management interface.',
                'code': '# Open browser:\nhttps://192.168.1.100:8006\n\n# Login:\nUsername: root\nRealm: PAM\nPassword: (set during installation)\n\n# Ignore certificate warning for self-signed cert',
                'language': 'text'
            },
            {
                'title': 'Configure No-Subscription Repository',
                'description': 'Enable community repository for updates.',
                'code': '# Edit sources list\nnano /etc/apt/sources.list\n\n# Add non-subscription repository:\ndeb http://download.proxmox.com/debian/pve bookworm pve-no-subscription\n\n# Disable enterprise repository\nmv /etc/apt/sources.list.d/pve-enterprise.list /etc/apt/sources.list.d/pve-enterprise.list.bak\n\n# Update\napt update && apt dist-upgrade -y',
                'language': 'bash'
            },
            {
                'title': 'Create Storage',
                'description': 'Configure storage for VMs and containers.',
                'code': '# Via Web GUI:\n# Datacenter > Storage > Add\n\n# LVM-Thin (recommended for VMs):\nID: local-lvm\nVolume Group: pve\nThin Pool: data\n\n# Directory storage:\nID: backup\nDirectory: /var/lib/vz/dump\nContent: VZDump backup files\n\n# NFS storage:\nID: nfs-storage\nServer: 192.168.1.50\nExport: /mnt/nfs/proxmox',
                'language': 'text'
            },
            {
                'title': 'Create VM',
                'description': 'Create a new virtual machine.',
                'code': '# Via Web GUI:\n# Click "Create VM"\n\n# General:\nName: ubuntu-server\nVM ID: 100\n\n# OS:\nISO image: ubuntu-22.04-server.iso\nType: Linux\nVersion: 6.x - 2.6 Kernel\n\n# System:\nMachine: q35\nBIOS: OVMF (UEFI)\nAdd EFI Disk: Yes\n\n# Disks:\nStorage: local-lvm\nSize: 32 GB\n\n# CPU:\nCores: 2\nType: host\n\n# Memory:\nMemory: 2048 MB\n\n# Network:\nBridge: vmbr0\nModel: VirtIO',
                'language': 'text'
            },
            {
                'title': 'Create Cluster',
                'description': 'Set up multi-node Proxmox cluster.',
                'code': '# On first node (pve1):\npvecm create my-cluster\n\n# On additional nodes (pve2, pve3):\npvecm add 192.168.1.100\n\n# Enter root password for first node\n\n# Check cluster status:\npvecm status\npvecm nodes',
                'language': 'bash'
            }
        ],
        'postInstallation': {
            'title': 'High Availability',
            'content': 'With 3+ nodes, enable HA for VMs. Configure shared storage (Ceph, NFS, iSCSI) for live migration. Set up backup schedules via Datacenter > Backup.'
        }
    },
    {
        'title': 'VMware ESXi Installation Guide',
        'description': 'Install and configure VMware ESXi hypervisor for enterprise virtualization.',
        'category': 'virtualization',
        'os': ['linux'],
        'difficulty': 'advanced',
        'tags': ['vmware', 'esxi', 'virtualization', 'enterprise', 'hypervisor'],
        'steps': [
            {
                'title': 'System Requirements',
                'description': 'Verify hardware compatibility.',
                'code': '# Minimum Requirements:\n# - 64-bit x86 CPU with VT-x/AMD-V\n# - Minimum 8GB RAM (16GB+ recommended)\n# - One or more Gigabit NICs\n# - Boot device: 32GB+ (USB, SD, or disk)\n# - VMFS datastore: Separate disk(s)\n\n# Check VMware Compatibility Guide:\nhttps://www.vmware.com/resources/compatibility/search.php',
                'language': 'text'
            },
            {
                'title': 'Download ESXi ISO',
                'description': 'Get VMware ESXi installation image.',
                'code': '# Create VMware account at:\nhttps://customerconnect.vmware.com\n\n# Download ESXi ISO:\n# - Free version: ESXi (Free)\n# - Licensed: ESXi with vSphere license\n\n# Create bootable USB (Linux):\ndd if=VMware-VMvisor-Installer-8.0-xxxx.x86_64.iso of=/dev/sdX bs=4M status=progress',
                'language': 'bash'
            },
            {
                'title': 'Install ESXi',
                'description': 'Boot and install ESXi.',
                'code': '# Boot from ISO/USB\n# Press Enter to start installer\n\n# Installation steps:\n1. Accept EULA (F11)\n2. Select installation disk\n3. Select keyboard layout\n4. Set root password\n5. Confirm installation (F11)\n6. Remove media and reboot',
                'language': 'text'
            },
            {
                'title': 'Configure Network',
                'description': 'Set up management network.',
                'code': '# At ESXi console (Direct Console UI):\n# Press F2 to customize\n# Enter root password\n\n# Configure Management Network:\n# - Network Adapters: Select NIC(s)\n# - IPv4 Configuration:\n#   Set static IP\n#   IP: 192.168.1.50\n#   Subnet: 255.255.255.0\n#   Gateway: 192.168.1.1\n# - DNS Configuration:\n#   Primary: 8.8.8.8\n#   Hostname: esxi1\n\n# Press Escape and confirm restart',
                'language': 'text'
            },
            {
                'title': 'Access vSphere Client',
                'description': 'Connect to ESXi web interface.',
                'code': '# Open browser:\nhttps://192.168.1.50\n\n# Login:\nUsername: root\nPassword: (set during installation)\n\n# Or use vSphere Client (Windows app):\n# Connect to: 192.168.1.50',
                'language': 'text'
            },
            {
                'title': 'Create Datastore',
                'description': 'Configure storage for VMs.',
                'code': '# In vSphere Client:\n# Storage > New Datastore\n\n# VMFS Datastore:\n1. Select "Create new VMFS datastore"\n2. Name: datastore1\n3. Select device (disk)\n4. Choose VMFS version (VMFS 6)\n5. Review and finish\n\n# NFS Datastore:\n1. Select "Mount NFS datastore"\n2. Name: nfs-storage\n3. NFS server: 192.168.1.60\n4. NFS share: /exports/vmware',
                'language': 'text'
            },
            {
                'title': 'Create Virtual Machine',
                'description': 'Deploy a new VM.',
                'code': '# Virtual Machines > Create/Register VM\n\n# Creation type: Create a new VM\n\n# Name and guest OS:\nName: ubuntu-server\nCompatibility: ESXi 8.0\nGuest OS family: Linux\nGuest OS version: Ubuntu Linux (64-bit)\n\n# Storage: Select datastore\n\n# Customize settings:\nCPU: 2\nMemory: 4 GB\nHard disk: 40 GB\nNetwork: VM Network\nCD/DVD: Datastore ISO file',
                'language': 'text'
            }
        ],
        'postInstallation': {
            'title': 'License and vCenter',
            'content': 'Apply license key in Host > Manage > Licensing. For multiple hosts, deploy vCenter Server for centralized management. Enable SSH under Host > Actions > Services > Enable SSH.'
        }
    },
    {
        'title': 'OpenVZ Container Management',
        'description': 'Create and manage OpenVZ containers for lightweight virtualization.',
        'category': 'virtualization',
        'os': ['centos', 'linux'],
        'difficulty': 'intermediate',
        'tags': ['openvz', 'containers', 'virtualization', 'lightweight', 'vps'],
        'steps': [
            {
                'title': 'Install OpenVZ 7',
                'description': 'Install OpenVZ on CentOS.',
                'code': '# Add OpenVZ repository\nyum install -y https://download.openvz.org/virtuozzo/releases/openvz-7.0.12-285/x86_64/os/Packages/o/openvz-release-7.0.12-1.vz7.x86_64.rpm\n\n# Install OpenVZ\nyum install -y vzkernel prlctl ploop\n\n# Reboot into OpenVZ kernel\nreboot',
                'language': 'bash'
            },
            {
                'title': 'Download Container Templates',
                'description': 'Get OS templates for containers.',
                'code': '# List available templates\nvzpkg list -O\n\n# Download specific template\nvzpkg fetch centos-7-x86_64\nvzpkg fetch ubuntu-18.04-x86_64\nvzpkg fetch debian-10-x86_64\n\n# Templates stored at:\nls /vz/template/cache/',
                'language': 'bash'
            },
            {
                'title': 'Create Container',
                'description': 'Create a new OpenVZ container.',
                'code': '# Create container\nprlctl create mycontainer --vmtype ct --ostemplate centos-7-x86_64\n\n# Or with vzctl (legacy):\nvzctl create 101 --ostemplate centos-7-x86_64\n\n# Set resources\nprlctl set mycontainer --cpus 2\nprlctl set mycontainer --memsize 2G\nprlctl set mycontainer --diskspace 20G',
                'language': 'bash'
            },
            {
                'title': 'Configure Network',
                'description': 'Set up container networking.',
                'code': '# Add IP address\nprlctl set mycontainer --ipadd 192.168.1.101\n\n# Set hostname\nprlctl set mycontainer --hostname mycontainer.local\n\n# Set DNS\nprlctl set mycontainer --nameserver 8.8.8.8\n\n# Or with vzctl:\nvzctl set 101 --ipadd 192.168.1.101 --save',
                'language': 'bash'
            },
            {
                'title': 'Start and Manage Container',
                'description': 'Container lifecycle management.',
                'code': '# Start container\nprlctl start mycontainer\n\n# Stop container\nprlctl stop mycontainer\n\n# Restart container\nprlctl restart mycontainer\n\n# List all containers\nprlctl list -a\n\n# Enter container\nprlctl enter mycontainer\n\n# Execute command in container\nprlctl exec mycontainer cat /etc/os-release',
                'language': 'bash'
            },
            {
                'title': 'Container Resource Limits',
                'description': 'Configure resource restrictions.',
                'code': '# CPU limits\nprlctl set mycontainer --cpulimit 50%\nprlctl set mycontainer --cpuunits 1000\n\n# Memory limits\nprlctl set mycontainer --memsize 2G\nprlctl set mycontainer --swappages 1G\n\n# Disk quota\nprlctl set mycontainer --diskspace 20G:25G\n\n# I/O priority\nprlctl set mycontainer --ioprio 5',
                'language': 'bash'
            }
        ],
        'postInstallation': {
            'title': 'Container Tips',
            'content': 'Use "prlctl snapshot" for backups. Monitor with "prlctl statistics". Templates can be customized and saved with "prlctl clone". Enable container autostart with "--onboot yes".'
        }
    },
    {
        'title': 'SolusVM WHMCS Integration',
        'description': 'Integrate SolusVM with WHMCS for automated VPS provisioning and billing.',
        'category': 'virtualization',
        'os': ['linux'],
        'difficulty': 'intermediate',
        'tags': ['solusvm', 'whmcs', 'integration', 'billing', 'automation'],
        'steps': [
            {
                'title': 'Download SolusVM Module',
                'description': 'Get the WHMCS integration module.',
                'code': '# Download from SolusVM Master:\nhttps://your_master:5656/admincp/modules.php\n\n# Or from SolusVM Documentation:\nhttps://documentation.solusvm.com/display/DOCS/WHMCS+Module\n\n# Extract to WHMCS directory:\nunzip solusvm-whmcs.zip -d /path/to/whmcs/modules/servers/',
                'language': 'bash'
            },
            {
                'title': 'Configure WHMCS Server',
                'description': 'Add SolusVM server in WHMCS.',
                'code': '# In WHMCS Admin:\n# Setup > Products/Services > Servers\n# Click "Add New Server"\n\nName: SolusVM-Master\nHostname: master.yourdomain.com\nIP Address: Your master IP\nAssigned IP: (leave blank)\n\n# Module settings:\nModule: SolusVM\nSecure: Yes (HTTPS)\nPort: 5656\nAPI Key: (from SolusVM)\nAPI Hash: (from SolusVM)',
                'language': 'text'
            },
            {
                'title': 'Get API Credentials',
                'description': 'Generate API key in SolusVM.',
                'code': '# In SolusVM Master:\n# Configuration > API Access\n# Click "Generate New"\n\n# Copy:\n# - API Key\n# - API Hash\n\n# Note: Restrict API to WHMCS server IP\n# Allowed IPs: your_whmcs_server_ip',
                'language': 'text'
            },
            {
                'title': 'Create Product Group',
                'description': 'Set up VPS product category.',
                'code': '# In WHMCS:\n# Setup > Products/Services > Products/Services\n# Click "Create a New Group"\n\nProduct Group Name: VPS Hosting\nHeadline: Virtual Private Servers\nTagline: High-performance KVM VPS\n\n# Save',
                'language': 'text'
            },
            {
                'title': 'Create VPS Product',
                'description': 'Configure VPS product for sale.',
                'code': '# Create Product:\n# Setup > Products/Services > Products/Services\n# Click "Create a New Product"\n\n# Details tab:\nProduct Type: Server/VPS\nProduct Group: VPS Hosting\nProduct Name: KVM VPS Basic\n\n# Module Settings tab:\nModule Name: SolusVM\nServer: SolusVM-Master\nNode: Select node or "Select Least Used"\nType: KVM\nPlan: Basic-KVM (from SolusVM)\nDefault OS: Select default\n\n# Custom Fields tab:\nAdd fields for:\n- Hostname (required)\n- Root Password',
                'language': 'text'
            },
            {
                'title': 'Configure Automation',
                'description': 'Set up automatic provisioning.',
                'code': '# Module Settings in Product:\n\n# Automatic Setup:\nAutomatically setup the product: Yes\nOn: When first payment is received\n\n# Actions:\nCreate Account: Automatically provision VPS\nSuspend: Suspend VPS on non-payment\nUnsuspend: Reactivate on payment\nTerminate: Delete VPS on termination\n\n# Test with a new order',
                'language': 'text'
            }
        ],
        'postInstallation': {
            'title': 'Additional Setup',
            'content': 'Configure email templates for VPS welcome message. Set up configurable options for RAM/disk upgrades. Enable client area functions for VPS management. Test full order-to-provision cycle.'
        }
    },
    {
        'title': 'Virtualizor to WHMCS Integration',
        'description': 'Connect Virtualizor with WHMCS for automated VPS management and billing.',
        'category': 'virtualization',
        'os': ['linux'],
        'difficulty': 'intermediate',
        'tags': ['virtualizor', 'whmcs', 'integration', 'billing', 'automation'],
        'steps': [
            {
                'title': 'Get Virtualizor WHMCS Module',
                'description': 'Download the integration module.',
                'code': '# Download from Virtualizor:\n# In Admin Panel > Settings > WHMCS Module\n# Or from:\nhttps://www.virtualizor.com/whmcs-vps-module/\n\n# Extract module:\nunzip virtualizor-whmcs.zip -d /path/to/whmcs/modules/servers/',
                'language': 'bash'
            },
            {
                'title': 'Configure API Access',
                'description': 'Get API credentials from Virtualizor.',
                'code': '# In Virtualizor Admin Panel:\n# Settings > API Credentials\n\n# Copy:\n# - API Key\n# - API Password\n\n# Or find in:\ncat /etc/virtualizor/master.php | grep key\ncat /etc/virtualizor/master.php | grep pass',
                'language': 'bash'
            },
            {
                'title': 'Add Server in WHMCS',
                'description': 'Configure Virtualizor server.',
                'code': '# In WHMCS Admin:\n# Setup > Products/Services > Servers\n# Add New Server\n\nName: Virtualizor-Main\nHostname: virt.yourdomain.com\nIP Address: Server IP\nPort: 4085\n\n# Server Details:\nModule: Virtualizor\nAPI Key: (from Virtualizor)\nAPI Password: (from Virtualizor)\nSecure Connection: Yes',
                'language': 'text'
            },
            {
                'title': 'Create VPS Product',
                'description': 'Set up product for Virtualizor VPS.',
                'code': '# Create Product:\n# Setup > Products/Services > Create Product\n\n# Product Details:\nProduct Type: Server/VPS\nProduct Group: VPS Hosting\nProduct Name: KVM VPS 1GB\n\n# Module Settings:\nModule: Virtualizor\nServer: Virtualizor-Main\n\n# Virtualizor Settings:\nPlan: Select plan from Virtualizor\nServer Group: Default or specific\nNumber of IPs: 1\nOperating System: Allow user selection',
                'language': 'text'
            },
            {
                'title': 'Configure Custom Fields',
                'description': 'Add required fields for VPS.',
                'code': '# In Product > Custom Fields:\n\n# Field 1:\nField Name: hostname\nField Type: Text Box\nDescription: Enter server hostname\nRequired: Yes\n\n# Field 2:\nField Name: rootpassword\nField Type: Password\nDescription: Set root password\nRequired: Yes\nValidation: /^.{8,}$/ (min 8 chars)\n\n# Field 3:\nField Name: os\nField Type: Dropdown\nOptions: (OS templates from Virtualizor)',
                'language': 'text'
            },
            {
                'title': 'Test Provisioning',
                'description': 'Verify automation works correctly.',
                'code': '# Test Steps:\n1. Place test order as admin\n2. Complete payment\n3. Check WHMCS module log:\n   Utilities > Logs > Module Log\n4. Verify VPS created in Virtualizor\n5. Check client receives welcome email\n6. Test client area VPS controls\n\n# Common issues:\n- Check API credentials\n- Verify IP pool has available IPs\n- Ensure plan exists and is active',
                'language': 'text'
            }
        ],
        'postInstallation': {
            'title': 'Configurable Options',
            'content': 'Set up configurable options for upgrades: additional RAM, disk space, bandwidth, IPs. Configure automatic suspension for overdue invoices. Enable VPS management in client area.'
        }
    }
]

async def seed_database():
    all_articles = networking_articles + virtualization_articles
    
    for article in all_articles:
        # Check if article already exists
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
    
    total = await db.code_snippets.count_documents({})
    print(f"\nTotal articles in database: {total}")

if __name__ == "__main__":
    asyncio.run(seed_database())
