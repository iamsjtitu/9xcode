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

# WHMCS Articles (20+)
whmcs_articles = [
    {
        'title': 'Install WHMCS on cPanel Server',
        'description': 'Complete guide to install WHMCS billing and automation platform on cPanel/WHM server.',
        'category': 'billing',
        'os': ['linux', 'ubuntu', 'centos'],
        'difficulty': 'intermediate',
        'tags': ['whmcs', 'installation', 'cpanel', 'billing'],
        'steps': [
            {
                'title': 'Download WHMCS',
                'description': 'Download WHMCS from your client area.',
                'code': '# Login to whmcs.com client area\n# Download the latest WHMCS release\n# You will get a zip file like whmcs_v8.x.x_full.zip',
                'language': 'bash'
            },
            {
                'title': 'Create Database',
                'description': 'Create MySQL database in cPanel.',
                'code': '# In cPanel:\n# 1. Go to MySQL Databases\n# 2. Create database: whmcs_db\n# 3. Create user: whmcs_user\n# 4. Add user to database with ALL PRIVILEGES\n# 5. Note down database name, user, and password',
                'language': 'text'
            },
            {
                'title': 'Upload and Extract Files',
                'description': 'Upload WHMCS to your server.',
                'code': '# Upload zip to public_html/billing/ via File Manager\n# Or via SSH:\ncd /home/username/public_html\nmkdir billing\ncd billing\nunzip ~/whmcs_v8.x.x_full.zip\nmv whmcs/* .\nrm -rf whmcs',
                'language': 'bash'
            },
            {
                'title': 'Set File Permissions',
                'description': 'Configure proper permissions for WHMCS.',
                'code': '# Set permissions\nchmod 755 .\nchmod 777 configuration.php\nchmod 777 attachments/\nchmod 777 downloads/\nchmod 777 templates_c/',
                'language': 'bash'
            },
            {
                'title': 'Run Installation Wizard',
                'description': 'Complete WHMCS installation via browser.',
                'code': '# Open browser:\nhttps://yourdomain.com/billing/install/install.php\n\n# Follow wizard:\n# 1. Accept license agreement\n# 2. Enter license key\n# 3. Enter database details\n# 4. Create admin account\n# 5. Complete installation',
                'language': 'text'
            },
            {
                'title': 'Secure Installation',
                'description': 'Remove install directory and secure files.',
                'code': '# Remove install directory\nrm -rf install/\n\n# Move configuration outside public\nmv configuration.php ../\n\n# Update path in init.php if needed\n# Set configuration.php to 400\nchmod 400 ../configuration.php',
                'language': 'bash'
            }
        ],
        'postInstallation': {
            'title': 'Post Installation',
            'content': 'Login to admin area at /billing/admin. Configure general settings, payment gateways, and create your first products. Set up cron job for automation.'
        }
    },
    {
        'title': 'WHMCS Cron Job Configuration',
        'description': 'Set up and configure WHMCS cron jobs for automated billing, invoicing, and system tasks.',
        'category': 'billing',
        'os': ['linux'],
        'difficulty': 'beginner',
        'tags': ['whmcs', 'cron', 'automation', 'billing'],
        'steps': [
            {
                'title': 'Locate Cron Command',
                'description': 'Find the correct cron command in WHMCS.',
                'code': '# In WHMCS Admin:\n# Go to Setup > Automation Settings\n# Copy the System Cron Command shown\n\n# Example command:\nphp -q /home/user/public_html/billing/crons/cron.php',
                'language': 'text'
            },
            {
                'title': 'Add Cron Job in cPanel',
                'description': 'Set up cron job in cPanel.',
                'code': '# In cPanel > Cron Jobs:\n# Common Settings: Once Per Five Minutes\n# Or custom: */5 * * * *\n\n# Command:\nphp -q /home/username/public_html/billing/crons/cron.php\n\n# Or with full path:\n/usr/local/bin/php -q /home/username/public_html/billing/crons/cron.php',
                'language': 'bash'
            },
            {
                'title': 'Add Cron via SSH',
                'description': 'Configure cron using command line.',
                'code': '# Edit crontab\ncrontab -e\n\n# Add line (runs every 5 minutes):\n*/5 * * * * /usr/bin/php -q /home/username/public_html/billing/crons/cron.php > /dev/null 2>&1\n\n# Save and exit',
                'language': 'bash'
            },
            {
                'title': 'Configure Cron Settings',
                'description': 'Adjust automation settings in WHMCS.',
                'code': '# In WHMCS Admin > Setup > Automation Settings:\n\n# Enable/Configure:\n# - Invoice Generation\n# - Invoice Reminders\n# - Overdue Notices\n# - Suspension/Termination\n# - Domain Sync\n# - Credit Card Processing',
                'language': 'text'
            },
            {
                'title': 'Verify Cron Execution',
                'description': 'Check if cron is running properly.',
                'code': '# In WHMCS Admin:\n# Utilities > System > Automation Status\n\n# Check last cron run time\n# Should show recent timestamp\n\n# Check logs:\n# Utilities > Logs > Activity Log\n# Filter by "Cron"',
                'language': 'text'
            }
        ],
        'postInstallation': {
            'title': 'Cron Tips',
            'content': 'Run cron every 5 minutes for best automation. Monitor cron logs regularly. Use pop cron for email processing if needed. Set up daily report emails for cron status.'
        }
    },
    {
        'title': 'WHMCS Payment Gateway Setup - PayPal',
        'description': 'Configure PayPal payment gateway in WHMCS for accepting payments.',
        'category': 'billing',
        'os': ['linux'],
        'difficulty': 'beginner',
        'tags': ['whmcs', 'paypal', 'payment', 'gateway'],
        'steps': [
            {
                'title': 'Enable PayPal Gateway',
                'description': 'Activate PayPal in WHMCS.',
                'code': '# In WHMCS Admin:\n# Setup > Payments > Payment Gateways\n# Click "All Payment Gateways"\n# Find "PayPal" and click "Activate"',
                'language': 'text'
            },
            {
                'title': 'Configure PayPal Settings',
                'description': 'Enter PayPal account details.',
                'code': '# PayPal Gateway Settings:\n\n# PayPal Email: your-paypal@email.com\n# API Username: (from PayPal business account)\n# API Password: (from PayPal business account)\n# API Signature: (from PayPal business account)\n\n# Enable:\n# - Accept PayPal payments\n# - Show on order form',
                'language': 'text'
            },
            {
                'title': 'Get PayPal API Credentials',
                'description': 'Obtain API credentials from PayPal.',
                'code': '# In PayPal Business Account:\n# 1. Go to Settings > Account Settings\n# 2. Click "API Access"\n# 3. Under "NVP/SOAP API integration"\n# 4. Click "Manage API Credentials"\n# 5. Request API signature\n# 6. Copy API Username, Password, and Signature',
                'language': 'text'
            },
            {
                'title': 'Configure IPN Settings',
                'description': 'Set up Instant Payment Notification.',
                'code': '# In PayPal Account:\n# Account Settings > Notifications > IPN\n\n# IPN URL:\nhttps://yourdomain.com/billing/modules/gateways/callback/paypal.php\n\n# Enable IPN message delivery',
                'language': 'text'
            },
            {
                'title': 'Test Payment',
                'description': 'Verify PayPal integration.',
                'code': '# Create test invoice in WHMCS\n# Use PayPal Sandbox for testing:\n# 1. Create sandbox accounts at developer.paypal.com\n# 2. In WHMCS, check "Sandbox Mode"\n# 3. Process test payment\n# 4. Verify invoice marked paid',
                'language': 'text'
            }
        ],
        'postInstallation': {
            'title': 'Important Notes',
            'content': 'Always test with sandbox before going live. Enable "Require Valid SSL" for security. Set up PayPal email notifications. Consider PayPal Checkout for modern checkout experience.'
        }
    },
    {
        'title': 'WHMCS Payment Gateway Setup - Stripe',
        'description': 'Integrate Stripe payment gateway with WHMCS for credit card processing.',
        'category': 'billing',
        'os': ['linux'],
        'difficulty': 'intermediate',
        'tags': ['whmcs', 'stripe', 'payment', 'creditcard'],
        'steps': [
            {
                'title': 'Create Stripe Account',
                'description': 'Set up Stripe business account.',
                'code': '# Go to stripe.com\n# Create account and verify business\n# Complete account activation\n# Get API keys from Dashboard > Developers > API keys',
                'language': 'text'
            },
            {
                'title': 'Enable Stripe in WHMCS',
                'description': 'Activate Stripe gateway.',
                'code': '# In WHMCS Admin:\n# Setup > Payments > Payment Gateways\n# All Payment Gateways > Stripe\n# Click "Activate"',
                'language': 'text'
            },
            {
                'title': 'Configure Stripe Settings',
                'description': 'Enter Stripe API credentials.',
                'code': '# Stripe Gateway Settings:\n\nPublishable Key: pk_live_xxxxxxxxx\nSecret Key: sk_live_xxxxxxxxx\n\n# For testing use:\nPublishable Key: pk_test_xxxxxxxxx\nSecret Key: sk_test_xxxxxxxxx\n\n# Enable:\n# - Credit Card payments\n# - Store cards for future use',
                'language': 'text'
            },
            {
                'title': 'Configure Webhooks',
                'description': 'Set up Stripe webhooks for payment notifications.',
                'code': '# In Stripe Dashboard:\n# Developers > Webhooks > Add endpoint\n\n# Endpoint URL:\nhttps://yourdomain.com/billing/modules/gateways/callback/stripe.php\n\n# Events to send:\n# - payment_intent.succeeded\n# - payment_intent.payment_failed\n# - customer.subscription.updated\n# - invoice.paid\n# - invoice.payment_failed\n\n# Copy Webhook signing secret to WHMCS',
                'language': 'text'
            },
            {
                'title': 'Enable 3D Secure',
                'description': 'Configure 3D Secure for card authentication.',
                'code': '# In WHMCS Stripe settings:\n# Enable "3D Secure"\n\n# This adds extra authentication for supported cards\n# Required for SCA compliance in EU\n\n# Stripe automatically handles 3DS when required',
                'language': 'text'
            }
        ],
        'postInstallation': {
            'title': 'Stripe Features',
            'content': 'Enable automatic card updates for expiring cards. Set up Stripe Radar for fraud protection. Configure subscription billing for recurring products. Use Stripe Tax for automatic tax calculation.'
        }
    },
    {
        'title': 'WHMCS Domain Registrar Integration - Enom',
        'description': 'Connect Enom domain registrar with WHMCS for automated domain registration.',
        'category': 'billing',
        'os': ['linux'],
        'difficulty': 'intermediate',
        'tags': ['whmcs', 'domains', 'enom', 'registrar'],
        'steps': [
            {
                'title': 'Get Enom Reseller Account',
                'description': 'Set up Enom reseller account.',
                'code': '# Apply at enom.com for reseller account\n# Complete verification process\n# Fund account with credits\n# Access reseller control panel',
                'language': 'text'
            },
            {
                'title': 'Enable Enom Module',
                'description': 'Activate Enom in WHMCS.',
                'code': '# In WHMCS Admin:\n# Setup > Products/Services > Domain Registrars\n# Find "Enom" and click "Activate"',
                'language': 'text'
            },
            {
                'title': 'Configure API Credentials',
                'description': 'Enter Enom API settings.',
                'code': '# Enom Module Settings:\n\nUsername: your_enom_id\nPassword: your_enom_password\n\n# Test Mode: Enable for testing\n# Use Testing Server: Enable for sandbox\n\n# Save configuration',
                'language': 'text'
            },
            {
                'title': 'Configure Domain Pricing',
                'description': 'Set up domain TLD pricing.',
                'code': '# In WHMCS Admin:\n# Setup > Products/Services > Domain Pricing\n\n# For each TLD (.com, .net, etc.):\n# - Set registration price\n# - Set renewal price  \n# - Set transfer price\n# - Select "Enom" as registrar\n# - Enable auto-registration',
                'language': 'text'
            },
            {
                'title': 'Test Domain Registration',
                'description': 'Verify domain integration.',
                'code': '# Enable test mode in Enom settings\n# Create test order with domain\n# Process order\n# Check domain registered in Enom panel\n\n# Verify:\n# - Domain appears in WHMCS\n# - Nameservers set correctly\n# - WHOIS information accurate',
                'language': 'text'
            }
        ],
        'postInstallation': {
            'title': 'Domain Management Tips',
            'content': 'Enable domain sync cron for status updates. Configure default nameservers. Set up ID protection addon. Enable domain transfer lock by default.'
        }
    },
    {
        'title': 'WHMCS cPanel Server Module Setup',
        'description': 'Configure WHMCS to automatically provision cPanel hosting accounts.',
        'category': 'billing',
        'os': ['linux'],
        'difficulty': 'intermediate',
        'tags': ['whmcs', 'cpanel', 'automation', 'provisioning'],
        'steps': [
            {
                'title': 'Add Server in WHMCS',
                'description': 'Register your cPanel server.',
                'code': '# In WHMCS Admin:\n# Setup > Products/Services > Servers\n# Click "Add New Server"\n\n# Server Details:\nName: Main cPanel Server\nHostname: server.yourdomain.com\nIP Address: 192.168.1.100\nAssigned IP Addresses: (optional)\n\n# Server Details:\nType: cPanel\nUsername: root (or reseller)\nPassword/Access Hash: WHM Access Hash\nSecure: Yes (use SSL)',
                'language': 'text'
            },
            {
                'title': 'Get WHM Access Hash',
                'description': 'Generate API token in WHM.',
                'code': '# In WHM:\n# Development > Manage API Tokens\n# Click "Generate Token"\n# Name: WHMCS\n# Copy the generated token\n\n# Or get access hash:\n# cat /root/.accesshash\n\n# For cPanel API token (preferred):\n# Use API Token instead of password',
                'language': 'bash'
            },
            {
                'title': 'Create Server Group',
                'description': 'Organize servers into groups.',
                'code': '# In WHMCS Admin:\n# Setup > Products/Services > Servers\n# Tab: Server Groups\n# Click "Create New Group"\n\nName: US Shared Hosting\nFill Type: Fill Active Server First\nSelected Servers: Main cPanel Server\n\n# Save group',
                'language': 'text'
            },
            {
                'title': 'Create Hosting Product',
                'description': 'Set up hosting package.',
                'code': '# Setup > Products/Services > Products/Services\n# Create New Product\n\n# Details:\nProduct Type: Shared Hosting\nProduct Group: Web Hosting\nProduct Name: Starter Plan\n\n# Module Settings:\nModule Name: cPanel\nServer Group: US Shared Hosting\nPackage Name: starter (from WHM packages)\n\n# Automatically setup: Order\n# Create on Add: Yes',
                'language': 'text'
            },
            {
                'title': 'Configure Package Options',
                'description': 'Set up configurable options.',
                'code': '# Module Settings continued:\n\n# Dedicated IP: Optional addon\n# Reseller: No\n# ACL: (leave blank for default)\n# CGI Access: Yes\n# Shell Access: No\n# Frontpage Extensions: No\n\n# Save product',
                'language': 'text'
            }
        ],
        'postInstallation': {
            'title': 'Testing',
            'content': 'Place test order and verify account creation in WHM. Check welcome email contains correct details. Test suspend/unsuspend/terminate functions. Verify disk and bandwidth limits applied correctly.'
        }
    },
    {
        'title': 'WHMCS Email Templates Customization',
        'description': 'Customize WHMCS email templates for professional client communication.',
        'category': 'billing',
        'os': ['linux'],
        'difficulty': 'beginner',
        'tags': ['whmcs', 'email', 'templates', 'customization'],
        'steps': [
            {
                'title': 'Access Email Templates',
                'description': 'Navigate to email template editor.',
                'code': '# In WHMCS Admin:\n# Setup > Email Templates\n\n# Categories:\n# - General Messages\n# - Product/Service Messages  \n# - Domain Messages\n# - Support Messages\n# - Invoice Messages\n# - Affiliate Messages',
                'language': 'text'
            },
            {
                'title': 'Edit Welcome Email',
                'description': 'Customize new account welcome email.',
                'code': '# Edit: Product/Service > Service Welcome Email\n\n# Available merge fields:\n{$client_name}\n{$service_product_name}\n{$service_domain}\n{$service_username}\n{$service_password}\n{$service_server_hostname}\n{$service_server_ip}\n{$service_dedicated_ip}\n\n# Add your branding and instructions',
                'language': 'text'
            },
            {
                'title': 'Customize Invoice Email',
                'description': 'Edit invoice notification template.',
                'code': '# Edit: Invoices > Invoice Created\n\n# Key merge fields:\n{$invoice_num}\n{$invoice_date_created}\n{$invoice_date_due}\n{$invoice_total}\n{$invoice_balance}\n{$invoice_link}\n\n# Add payment instructions\n# Include payment methods available',
                'language': 'text'
            },
            {
                'title': 'Create Custom Template',
                'description': 'Add new email template.',
                'code': '# Click "Create New Email Template"\n\n# Template Details:\nType: Product\nUnique Name: custom_welcome\nSubject: Welcome to {$companyname}\n\n# Email Content:\n<p>Dear {$client_name},</p>\n<p>Thank you for choosing us!</p>\n<p>Your service details:</p>\n<ul>\n  <li>Product: {$service_product_name}</li>\n  <li>Domain: {$service_domain}</li>\n</ul>',
                'language': 'html'
            },
            {
                'title': 'Set Up Email Styling',
                'description': 'Configure global email header/footer.',
                'code': '# Setup > General Settings > Mail\n\n# Global Email Header:\n<html><body style="font-family: Arial, sans-serif;">\n<div style="max-width: 600px; margin: 0 auto;">\n<img src="https://yourdomain.com/logo.png" alt="Logo">\n\n# Global Email Footer:\n<hr>\n<p>Best regards,<br>{$companyname}</p>\n<p><a href="{$whmcs_url}">Client Area</a></p>\n</div></body></html>',
                'language': 'html'
            }
        ],
        'postInstallation': {
            'title': 'Email Tips',
            'content': 'Test all templates after editing. Use HTML emails for professional look. Include unsubscribe links where required. Set up DKIM/SPF for deliverability.'
        }
    },
    {
        'title': 'WHMCS Module Development Basics',
        'description': 'Introduction to developing custom modules for WHMCS.',
        'category': 'billing',
        'os': ['linux'],
        'difficulty': 'advanced',
        'tags': ['whmcs', 'modules', 'development', 'php'],
        'steps': [
            {
                'title': 'Understand Module Types',
                'description': 'Learn WHMCS module categories.',
                'code': '# WHMCS Module Types:\n\n# 1. Provisioning Modules\n# - /modules/servers/modulename/\n# - Automate service provisioning\n\n# 2. Payment Gateway Modules\n# - /modules/gateways/modulename.php\n# - Process payments\n\n# 3. Registrar Modules\n# - /modules/registrars/modulename/\n# - Domain registration\n\n# 4. Addon Modules\n# - /modules/addons/modulename/\n# - Extend WHMCS functionality\n\n# 5. Report Modules\n# - /modules/reports/modulename.php\n# - Custom reports',
                'language': 'text'
            },
            {
                'title': 'Create Provisioning Module',
                'description': 'Basic server module structure.',
                'code': '<?php\n// modules/servers/mymodule/mymodule.php\n\nfunction mymodule_MetaData() {\n    return array(\n        \'DisplayName\' => \'My Module\',\n        \'APIVersion\' => \'1.1\',\n    );\n}\n\nfunction mymodule_ConfigOptions() {\n    return array(\n        \'Package\' => array(\n            \'Type\' => \'text\',\n            \'Size\' => \'25\',\n            \'Default\' => \'\',\n            \'Description\' => \'Package name\',\n        ),\n    );\n}\n\nfunction mymodule_CreateAccount(array $params) {\n    // Provisioning logic here\n    return \'success\';\n}\n\nfunction mymodule_SuspendAccount(array $params) {\n    return \'success\';\n}\n\nfunction mymodule_UnsuspendAccount(array $params) {\n    return \'success\';\n}\n\nfunction mymodule_TerminateAccount(array $params) {\n    return \'success\';\n}',
                'language': 'php'
            },
            {
                'title': 'Create Addon Module',
                'description': 'Basic addon module structure.',
                'code': '<?php\n// modules/addons/myaddon/myaddon.php\n\nfunction myaddon_config() {\n    return array(\n        \'name\' => \'My Addon\',\n        \'description\' => \'Custom functionality\',\n        \'version\' => \'1.0\',\n        \'author\' => \'Your Name\',\n    );\n}\n\nfunction myaddon_activate() {\n    // Create database tables\n    return array(\'status\' => \'success\');\n}\n\nfunction myaddon_deactivate() {\n    // Cleanup\n    return array(\'status\' => \'success\');\n}\n\nfunction myaddon_output($vars) {\n    echo \'<h2>My Addon</h2>\';\n    echo \'<p>Admin interface here</p>\';\n}\n\nfunction myaddon_clientarea($vars) {\n    return array(\n        \'pagetitle\' => \'My Addon\',\n        \'templatefile\' => \'clientarea\',\n        \'vars\' => array(),\n    );\n}',
                'language': 'php'
            },
            {
                'title': 'Use WHMCS API',
                'description': 'Interact with WHMCS internal API.',
                'code': '<?php\n// Using local API within module\nuse WHMCS\\Database\\Capsule;\n\n// Get client details\n$result = localAPI(\'GetClientsDetails\', array(\n    \'clientid\' => $params[\'clientid\'],\n), \'admin\');\n\n// Create invoice\n$result = localAPI(\'CreateInvoice\', array(\n    \'userid\' => $params[\'clientid\'],\n    \'itemdescription1\' => \'Custom charge\',\n    \'itemamount1\' => 10.00,\n    \'autoapplycredit\' => true,\n), \'admin\');\n\n// Database query\n$services = Capsule::table(\'tblhosting\')\n    ->where(\'userid\', $params[\'clientid\'])\n    ->get();',
                'language': 'php'
            }
        ],
        'postInstallation': {
            'title': 'Development Resources',
            'content': 'Use WHMCS Developer Documentation at developers.whmcs.com. Test modules in sandbox environment. Use hooks for extending functionality without core modifications. Submit modules to WHMCS Marketplace.'
        }
    },
    {
        'title': 'WHMCS Hooks System Guide',
        'description': 'Learn to use WHMCS hooks for custom functionality and automation.',
        'category': 'billing',
        'os': ['linux'],
        'difficulty': 'advanced',
        'tags': ['whmcs', 'hooks', 'automation', 'development'],
        'steps': [
            {
                'title': 'Understanding Hooks',
                'description': 'Learn hook system basics.',
                'code': '# Hooks allow custom code execution at specific events\n# Located in: /includes/hooks/\n\n# Hook file naming:\n# - custom_hooks.php\n# - any_name.php\n\n# All .php files in hooks folder are loaded automatically',
                'language': 'text'
            },
            {
                'title': 'Create Hook File',
                'description': 'Set up custom hook file.',
                'code': '<?php\n// includes/hooks/custom_hooks.php\n\nuse WHMCS\\Database\\Capsule;\n\n// Hook registration\nadd_hook(\'HookPointName\', 1, function($vars) {\n    // Your code here\n    return $vars;\n});',
                'language': 'php'
            },
            {
                'title': 'Common Hook Examples',
                'description': 'Frequently used hooks.',
                'code': '<?php\n// After client registration\nadd_hook(\'ClientAdd\', 1, function($vars) {\n    $clientId = $vars[\'userid\'];\n    // Send to CRM, create ticket, etc.\n    logActivity("New client registered: " . $clientId);\n});\n\n// Before invoice creation\nadd_hook(\'PreInvoicingGenerateInvoiceItems\', 1, function($vars) {\n    // Modify invoice items\n    return $vars;\n});\n\n// After payment received\nadd_hook(\'InvoicePaid\', 1, function($vars) {\n    $invoiceId = $vars[\'invoiceid\'];\n    // Process payment, update external system\n});\n\n// Service activated\nadd_hook(\'AfterModuleCreate\', 1, function($vars) {\n    $serviceId = $vars[\'params\'][\'serviceid\'];\n    // Post-provisioning tasks\n});',
                'language': 'php'
            },
            {
                'title': 'Client Area Hooks',
                'description': 'Modify client area behavior.',
                'code': '<?php\n// Add custom page\nadd_hook(\'ClientAreaPage\', 1, function($vars) {\n    return array(\n        \'customvar\' => \'value\',\n    );\n});\n\n// Modify navigation\nadd_hook(\'ClientAreaPrimarySidebar\', 1, function($sidebar) {\n    $sidebar->addChild(\'custom-link\')\n        ->setLabel(\'Custom Page\')\n        ->setUri(\'custom.php\');\n});\n\n// Add header output\nadd_hook(\'ClientAreaHeadOutput\', 1, function($vars) {\n    return \'<script>console.log("Custom JS");</script>\';\n});',
                'language': 'php'
            },
            {
                'title': 'Admin Area Hooks',
                'description': 'Extend admin functionality.',
                'code': '<?php\n// Admin login\nadd_hook(\'AdminLogin\', 1, function($vars) {\n    logActivity("Admin login: " . $vars[\'username\']);\n});\n\n// Before ticket reply\nadd_hook(\'PreAdminTicketReply\', 1, function($vars) {\n    // Modify reply, add signature\n    return $vars;\n});\n\n// Custom admin widget\nadd_hook(\'AdminHomeWidgets\', 1, function() {\n    return new CustomWidget();\n});',
                'language': 'php'
            }
        ],
        'postInstallation': {
            'title': 'Hook Best Practices',
            'content': 'Use priority parameter to control execution order. Return modified $vars array when required. Use logging for debugging. Keep hooks efficient to avoid performance issues.'
        }
    },
    {
        'title': 'WHMCS Security Hardening',
        'description': 'Secure your WHMCS installation against common threats.',
        'category': 'billing',
        'os': ['linux'],
        'difficulty': 'intermediate',
        'tags': ['whmcs', 'security', 'hardening', 'protection'],
        'steps': [
            {
                'title': 'Secure Configuration File',
                'description': 'Protect configuration.php.',
                'code': '# Move configuration outside web root\nmv /home/user/public_html/billing/configuration.php /home/user/\n\n# Update path in init.php:\n$whmcspath = dirname(__DIR__);\ninclude dirname($whmcspath) . \'/configuration.php\';\n\n# Or use .htaccess:\n<Files configuration.php>\n    order allow,deny\n    deny from all\n</Files>',
                'language': 'bash'
            },
            {
                'title': 'Enable Admin Security',
                'description': 'Configure admin area protection.',
                'code': '# In WHMCS Admin > Setup > Security:\n\n# Enable:\n# - Two-Factor Authentication\n# - IP Whitelist for Admin\n# - CAPTCHA on login\n# - Disable Password Reset via Email\n\n# IP Whitelist:\n# Add your static IPs only\n\n# .htaccess for admin folder:\n<Files *.php>\n    order deny,allow\n    deny from all\n    allow from YOUR.IP.ADDRESS\n</Files>',
                'language': 'text'
            },
            {
                'title': 'Disable Unnecessary Features',
                'description': 'Remove attack surface.',
                'code': '# In configuration.php:\n$api_enable_logging = true;\n$display_errors = false;\n\n# Disable unused features:\n# - Disable API if not used\n# - Disable announcements if not used\n# - Disable affiliates if not used\n\n# In WHMCS Admin > Setup > Security:\n# Disable: "Display Errors"',
                'language': 'php'
            },
            {
                'title': 'Implement CSP Headers',
                'description': 'Add security headers.',
                'code': '# In .htaccess:\nHeader set X-Frame-Options "SAMEORIGIN"\nHeader set X-Content-Type-Options "nosniff"\nHeader set X-XSS-Protection "1; mode=block"\nHeader set Referrer-Policy "strict-origin-when-cross-origin"\nHeader set Content-Security-Policy "default-src \'self\'; script-src \'self\' \'unsafe-inline\';"',
                'language': 'apache'
            },
            {
                'title': 'Database Security',
                'description': 'Secure database access.',
                'code': '# Use dedicated database user\nCREATE USER \'whmcs_user\'@\'localhost\' IDENTIFIED BY \'StrongPassword123!\';\nGRANT SELECT, INSERT, UPDATE, DELETE ON whmcs_db.* TO \'whmcs_user\'@\'localhost\';\nFLUSH PRIVILEGES;\n\n# Avoid GRANT ALL - only give needed permissions\n# Enable MySQL SSL if connecting remotely\n\n# Regular backups:\nmysqldump -u root -p whmcs_db > backup_$(date +%Y%m%d).sql',
                'language': 'sql'
            }
        ],
        'postInstallation': {
            'title': 'Ongoing Security',
            'content': 'Keep WHMCS updated to latest version. Monitor admin activity logs. Set up intrusion detection. Regular security audits. Use strong, unique passwords for all accounts.'
        }
    },
    {
        'title': 'WHMCS Backup and Restore Guide',
        'description': 'Complete guide to backing up and restoring WHMCS installation.',
        'category': 'billing',
        'os': ['linux'],
        'difficulty': 'beginner',
        'tags': ['whmcs', 'backup', 'restore', 'disaster-recovery'],
        'steps': [
            {
                'title': 'Backup Database',
                'description': 'Export WHMCS database.',
                'code': '# Via command line:\nmysqldump -u root -p whmcs_database > whmcs_backup_$(date +%Y%m%d).sql\n\n# Compressed backup:\nmysqldump -u root -p whmcs_database | gzip > whmcs_backup_$(date +%Y%m%d).sql.gz\n\n# Via phpMyAdmin:\n# Select database > Export > Quick > Go',
                'language': 'bash'
            },
            {
                'title': 'Backup Files',
                'description': 'Backup WHMCS files and folders.',
                'code': '# Critical folders to backup:\n# - /billing/ (entire WHMCS directory)\n# - configuration.php (if outside web root)\n\n# Create archive:\ncd /home/user/public_html\ntar -czvf whmcs_files_$(date +%Y%m%d).tar.gz billing/\n\n# Or via cPanel > Backup > Download a Home Directory Backup',
                'language': 'bash'
            },
            {
                'title': 'Automated Backup Script',
                'description': 'Create automated backup cron.',
                'code': '#!/bin/bash\n# /home/user/scripts/whmcs_backup.sh\n\nDATE=$(date +%Y%m%d)\nBACKUP_DIR="/home/user/backups"\nDB_NAME="whmcs_database"\nDB_USER="root"\nDB_PASS="password"\nWHMCS_DIR="/home/user/public_html/billing"\n\n# Create backup directory\nmkdir -p $BACKUP_DIR\n\n# Database backup\nmysqldump -u$DB_USER -p$DB_PASS $DB_NAME | gzip > $BACKUP_DIR/db_$DATE.sql.gz\n\n# Files backup\ntar -czvf $BACKUP_DIR/files_$DATE.tar.gz $WHMCS_DIR\n\n# Delete backups older than 30 days\nfind $BACKUP_DIR -type f -mtime +30 -delete\n\n# Add to cron: 0 2 * * * /home/user/scripts/whmcs_backup.sh',
                'language': 'bash'
            },
            {
                'title': 'Restore Database',
                'description': 'Import database backup.',
                'code': '# Create fresh database\nmysql -u root -p -e "CREATE DATABASE whmcs_new;"\n\n# Import backup:\nmysql -u root -p whmcs_new < whmcs_backup.sql\n\n# Or compressed:\ngunzip < whmcs_backup.sql.gz | mysql -u root -p whmcs_new\n\n# Update configuration.php with new database name if different',
                'language': 'bash'
            },
            {
                'title': 'Restore Files',
                'description': 'Restore WHMCS files from backup.',
                'code': '# Extract files backup:\ncd /home/user/public_html\ntar -xzvf whmcs_files_backup.tar.gz\n\n# Set permissions:\nchmod 755 billing/\nchmod 777 billing/attachments/\nchmod 777 billing/downloads/\nchmod 777 billing/templates_c/\n\n# Update configuration.php:\n# - Database credentials\n# - License key\n# - System URLs',
                'language': 'bash'
            }
        ],
        'postInstallation': {
            'title': 'Backup Best Practices',
            'content': 'Store backups offsite (cloud storage, remote server). Test restoration periodically. Encrypt sensitive backups. Keep multiple backup generations. Document restoration procedure.'
        }
    },
    {
        'title': 'WHMCS Multi-Brand Setup',
        'description': 'Configure WHMCS for multiple brands and storefronts.',
        'category': 'billing',
        'os': ['linux'],
        'difficulty': 'advanced',
        'tags': ['whmcs', 'multi-brand', 'storefront', 'reseller'],
        'steps': [
            {
                'title': 'Enable Multi-Brand',
                'description': 'Activate multiple storefronts.',
                'code': '# Requirements:\n# - WHMCS version 8.0+\n# - Business license or higher\n\n# In WHMCS Admin:\n# Setup > General Settings > Brands\n# Click "Create New Brand"',
                'language': 'text'
            },
            {
                'title': 'Create New Brand',
                'description': 'Set up additional brand.',
                'code': '# Brand Settings:\n\nBrand Name: Second Brand\nSystem URL: https://brand2.com/billing/\nEmail From: support@brand2.com\nEmail Name: Brand2 Support\n\n# Logo & Styling:\nUpload brand-specific logo\nCustomize colors\nSelect template',
                'language': 'text'
            },
            {
                'title': 'Configure Domain Routing',
                'description': 'Set up domain-based brand selection.',
                'code': '# In web server (Apache):\n<VirtualHost *:443>\n    ServerName brand2.com\n    DocumentRoot /home/user/public_html/billing\n    SetEnv WHMCS_BRAND_ID 2\n</VirtualHost>\n\n# Or in .htaccess:\nSetEnvIf Host brand2.com WHMCS_BRAND_ID=2\n\n# Or via configuration.php:\n$brandIdOverride = (strpos($_SERVER[\'HTTP_HOST\'], \'brand2\') !== false) ? 2 : 0;',
                'language': 'apache'
            },
            {
                'title': 'Assign Products to Brands',
                'description': 'Configure product visibility.',
                'code': '# In Product Settings:\n# Edit Product > Details tab\n\n# Brand Assignment:\n# Select which brands can see this product\n# Uncheck brands to hide product\n\n# Or at Product Group level:\n# Edit Product Group > Brand Availability',
                'language': 'text'
            },
            {
                'title': 'Customize Templates per Brand',
                'description': 'Set brand-specific templates.',
                'code': '# Create template copy:\ncp -r templates/twenty-one templates/brand2\n\n# Customize brand2 template:\n# - Update logo references\n# - Change color scheme\n# - Modify layouts\n\n# Assign template to brand:\n# Setup > Brands > Edit Brand\n# Select "brand2" template',
                'language': 'bash'
            }
        ],
        'postInstallation': {
            'title': 'Multi-Brand Tips',
            'content': 'Use separate email configurations per brand. Create brand-specific email templates. Set up separate support departments. Consider separate payment gateways per brand if needed.'
        }
    }
]

# Additional Billing System Articles
billing_articles = [
    {
        'title': 'Install Blesta Billing System',
        'description': 'Complete installation guide for Blesta billing and client management platform.',
        'category': 'billing',
        'os': ['linux', 'ubuntu', 'centos'],
        'difficulty': 'intermediate',
        'tags': ['blesta', 'installation', 'billing', 'automation'],
        'steps': [
            {
                'title': 'Download Blesta',
                'description': 'Get Blesta from client area.',
                'code': '# Purchase license at blesta.com\n# Download from client area\n# Get latest version zip file',
                'language': 'text'
            },
            {
                'title': 'Upload and Extract',
                'description': 'Install Blesta files.',
                'code': 'cd /home/user/public_html\nmkdir billing\ncd billing\nunzip ~/blesta-*.zip\nmv blesta/* .\nrm -rf blesta',
                'language': 'bash'
            },
            {
                'title': 'Set Permissions',
                'description': 'Configure file permissions.',
                'code': 'chmod 755 .\nchmod -R 755 cache/\nchmod -R 755 uploads/\nchmod -R 755 logs_blesta/',
                'language': 'bash'
            },
            {
                'title': 'Create Database',
                'description': 'Set up MySQL database.',
                'code': 'mysql -u root -p\nCREATE DATABASE blesta_db;\nCREATE USER \'blesta_user\'@\'localhost\' IDENTIFIED BY \'SecurePassword\';\nGRANT ALL PRIVILEGES ON blesta_db.* TO \'blesta_user\'@\'localhost\';\nFLUSH PRIVILEGES;\nEXIT;',
                'language': 'sql'
            },
            {
                'title': 'Run Installer',
                'description': 'Complete web installation.',
                'code': '# Open browser:\nhttps://yourdomain.com/billing/\n\n# Follow wizard:\n# 1. System Requirements check\n# 2. Enter license key\n# 3. Database configuration\n# 4. Create admin account\n# 5. Basic settings',
                'language': 'text'
            }
        ],
        'postInstallation': {
            'title': 'Next Steps',
            'content': 'Configure cron job for automation. Set up payment gateways. Install modules for cPanel/WHM integration. Create product packages.'
        }
    },
    {
        'title': 'Blesta cPanel Module Configuration',
        'description': 'Set up automated hosting provisioning with Blesta and cPanel/WHM.',
        'category': 'billing',
        'os': ['linux'],
        'difficulty': 'intermediate',
        'tags': ['blesta', 'cpanel', 'automation', 'modules'],
        'steps': [
            {
                'title': 'Install cPanel Module',
                'description': 'Add cPanel module to Blesta.',
                'code': '# Module included with Blesta\n# In Blesta Admin:\n# Settings > Company > Modules\n# Click "Install" next to cPanel',
                'language': 'text'
            },
            {
                'title': 'Add Server',
                'description': 'Configure cPanel server.',
                'code': '# Settings > Company > Modules > cPanel\n# Click "Add Server"\n\n# Server Details:\nLabel: Main Server\nHostname: server.yourdomain.com\nUsername: root\nAPI Token: (from WHM)\nUse SSL: Yes\nAccount Limit: 500',
                'language': 'text'
            },
            {
                'title': 'Create Server Group',
                'description': 'Organize servers.',
                'code': '# Settings > Company > Module Groups\n# Create New Group\n\nName: Shared Hosting\nModule: cPanel\nAdd Action: Add to least full server\n\n# Assign servers to group',
                'language': 'text'
            },
            {
                'title': 'Create Package',
                'description': 'Set up hosting package.',
                'code': '# Packages > Browse > Create Package\n\nModule: cPanel\nPackage Name: Starter Plan\nModule Row: Main Server (or group)\n\n# Package Options:\nCPanel Package: starter\nType: Hosting\nACL: default\n\n# Pricing: Set monthly/yearly rates',
                'language': 'text'
            },
            {
                'title': 'Test Provisioning',
                'description': 'Verify automation works.',
                'code': '# Create test client\n# Order service with package\n# Process order\n# Verify:\n# - Account created in WHM\n# - Welcome email sent\n# - Service active in Blesta',
                'language': 'text'
            }
        ],
        'postInstallation': {
            'title': 'Tips',
            'content': 'Use API tokens instead of passwords. Set up package sync for consistency. Configure email templates. Test suspend/terminate functions.'
        }
    },
    {
        'title': 'Install HostBill Billing Platform',
        'description': 'Installation and setup guide for HostBill billing automation software.',
        'category': 'billing',
        'os': ['linux'],
        'difficulty': 'intermediate',
        'tags': ['hostbill', 'installation', 'billing', 'automation'],
        'steps': [
            {
                'title': 'System Requirements',
                'description': 'Verify server meets requirements.',
                'code': '# Requirements:\n# - PHP 7.4+ with extensions: curl, mysql, gd, mbstring, zip\n# - MySQL 5.7+ or MariaDB 10.2+\n# - Apache/Nginx with mod_rewrite\n# - ionCube Loader\n\n# Check ionCube:\nphp -v | grep ionCube',
                'language': 'bash'
            },
            {
                'title': 'Install ionCube',
                'description': 'Install ionCube loader if missing.',
                'code': '# Download ionCube\ncd /tmp\nwget https://downloads.ioncube.com/loader_downloads/ioncube_loaders_lin_x86-64.tar.gz\ntar -xzf ioncube_loaders_lin_x86-64.tar.gz\n\n# Copy loader for your PHP version\ncp ioncube/ioncube_loader_lin_7.4.so /usr/lib64/php/modules/\n\n# Add to php.ini:\nzend_extension = /usr/lib64/php/modules/ioncube_loader_lin_7.4.so\n\n# Restart PHP\nsystemctl restart php-fpm',
                'language': 'bash'
            },
            {
                'title': 'Upload HostBill',
                'description': 'Install HostBill files.',
                'code': '# Upload hostbill zip to server\ncd /home/user/public_html\nmkdir hostbill\ncd hostbill\nunzip ~/hostbill.zip\n\n# Set permissions\nchmod 755 .\nchmod 777 includes/config.php\nchmod -R 777 cache/\nchmod -R 777 logs/',
                'language': 'bash'
            },
            {
                'title': 'Run Installer',
                'description': 'Complete web installation.',
                'code': '# Open: https://yourdomain.com/hostbill/install/\n\n# Steps:\n# 1. Requirements check\n# 2. License key entry\n# 3. Database configuration\n# 4. Admin account creation\n# 5. Cron setup\n\n# After install, remove:\nrm -rf install/',
                'language': 'text'
            },
            {
                'title': 'Configure Cron',
                'description': 'Set up automation cron.',
                'code': '# Add to crontab:\n*/5 * * * * php /home/user/public_html/hostbill/cron.php\n\n# Or via cPanel Cron Jobs:\n# Every 5 minutes:\n*/5 * * * * /usr/bin/php /home/user/public_html/hostbill/cron.php > /dev/null 2>&1',
                'language': 'bash'
            }
        ],
        'postInstallation': {
            'title': 'Post Install',
            'content': 'Configure payment gateways. Add hosting servers. Create products and services. Set up client templates. Enable SSL for security.'
        }
    },
    {
        'title': 'Install FOSSBilling (Free Billing)',
        'description': 'Set up FOSSBilling open-source billing platform (BoxBilling successor).',
        'category': 'billing',
        'os': ['linux', 'ubuntu', 'debian'],
        'difficulty': 'intermediate',
        'tags': ['fossbilling', 'opensource', 'billing', 'free'],
        'steps': [
            {
                'title': 'Download FOSSBilling',
                'description': 'Get the latest release.',
                'code': '# Clone from GitHub\ncd /home/user/public_html\ngit clone https://github.com/FOSSBilling/FOSSBilling.git billing\n\n# Or download release:\nwget https://github.com/FOSSBilling/FOSSBilling/releases/latest/download/FOSSBilling.zip\nunzip FOSSBilling.zip -d billing',
                'language': 'bash'
            },
            {
                'title': 'Install Dependencies',
                'description': 'Install PHP dependencies with Composer.',
                'code': 'cd /home/user/public_html/billing\n\n# Install Composer if not present\ncurl -sS https://getcomposer.org/installer | php\n\n# Install dependencies\nphp composer.phar install --no-dev',
                'language': 'bash'
            },
            {
                'title': 'Set Permissions',
                'description': 'Configure directory permissions.',
                'code': 'chmod 755 .\nchmod 777 data/cache\nchmod 777 data/log\nchmod 777 data/uploads',
                'language': 'bash'
            },
            {
                'title': 'Create Database',
                'description': 'Set up MySQL database.',
                'code': 'mysql -u root -p\nCREATE DATABASE fossbilling;\nCREATE USER \'fossuser\'@\'localhost\' IDENTIFIED BY \'password\';\nGRANT ALL ON fossbilling.* TO \'fossuser\'@\'localhost\';\nFLUSH PRIVILEGES;\nEXIT;',
                'language': 'sql'
            },
            {
                'title': 'Run Installer',
                'description': 'Complete installation wizard.',
                'code': '# Open browser:\nhttps://yourdomain.com/billing/install\n\n# Follow steps:\n# 1. Accept license\n# 2. Requirements check\n# 3. Database configuration\n# 4. Admin account setup\n# 5. Complete installation\n\n# Remove install folder:\nrm -rf install/',
                'language': 'text'
            }
        ],
        'postInstallation': {
            'title': 'Getting Started',
            'content': 'FOSSBilling is free and open-source. Community-driven development. Compatible with many WHMCS modules. Active Discord community for support.'
        }
    },
    {
        'title': 'WHMCS to Blesta Migration',
        'description': 'Step-by-step guide to migrate from WHMCS to Blesta billing system.',
        'category': 'billing',
        'os': ['linux'],
        'difficulty': 'advanced',
        'tags': ['whmcs', 'blesta', 'migration', 'billing'],
        'steps': [
            {
                'title': 'Prepare Migration',
                'description': 'Pre-migration checklist.',
                'code': '# Before starting:\n# 1. Backup WHMCS database completely\n# 2. Install fresh Blesta\n# 3. Document custom configurations\n# 4. List all integrations/modules used\n# 5. Plan downtime window',
                'language': 'text'
            },
            {
                'title': 'Install Migration Tool',
                'description': 'Set up Blesta migration utility.',
                'code': '# In Blesta Admin:\n# Settings > Company > Import\n\n# Install WHMCS import module if not present\n# Download from Blesta marketplace',
                'language': 'text'
            },
            {
                'title': 'Configure Import',
                'description': 'Set up WHMCS connection.',
                'code': '# Import Settings:\n\nWHMCS Database Host: localhost\nWHMCS Database Name: whmcs_db\nWHMCS Database User: whmcs_user\nWHMCS Database Password: ****\nWHMCS URL: https://old-site.com/billing/\n\n# Test connection',
                'language': 'text'
            },
            {
                'title': 'Run Import',
                'description': 'Execute migration process.',
                'code': '# Import order:\n# 1. Clients & Contacts\n# 2. Services/Products\n# 3. Invoices & Transactions\n# 4. Support Tickets\n# 5. Domains\n\n# Monitor progress\n# Check error logs\n# Verify data accuracy',
                'language': 'text'
            },
            {
                'title': 'Post-Migration Tasks',
                'description': 'Complete migration cleanup.',
                'code': '# After import:\n# 1. Configure payment gateways in Blesta\n# 2. Set up server modules\n# 3. Test client login\n# 4. Update DNS/redirect old URL\n# 5. Notify clients of changes\n# 6. Monitor for issues',
                'language': 'text'
            }
        ],
        'postInstallation': {
            'title': 'Migration Tips',
            'content': 'Keep old WHMCS running in read-only during transition. Test thoroughly in staging first. Have rollback plan ready. Allow time for clients to adjust.'
        }
    }
]

# Web Hosting Articles
webhosting_articles = [
    {
        'title': 'cPanel Account Management Guide',
        'description': 'Complete guide to creating and managing cPanel hosting accounts in WHM.',
        'category': 'web-hosting',
        'os': ['linux', 'centos'],
        'difficulty': 'beginner',
        'tags': ['cpanel', 'whm', 'hosting', 'account'],
        'steps': [
            {
                'title': 'Create Hosting Account',
                'description': 'Set up new cPanel account in WHM.',
                'code': '# In WHM:\n# Account Functions > Create a New Account\n\n# Account Details:\nDomain: example.com\nUsername: exampleu\nPassword: StrongPassword123!\nEmail: admin@example.com\n\n# Package: Select hosting package\n# Settings: Choose options\n# Create',
                'language': 'text'
            },
            {
                'title': 'Modify Account',
                'description': 'Change account settings.',
                'code': '# Account Functions > Modify an Account\n\n# Changeable options:\n# - Disk quota\n# - Bandwidth limit\n# - Email limits\n# - Database limits\n# - Addon domains\n# - Package assignment',
                'language': 'text'
            },
            {
                'title': 'Suspend Account',
                'description': 'Suspend hosting account.',
                'code': '# Account Functions > Manage Account Suspension\n\n# Select account\n# Enter suspension reason\n# Click Suspend\n\n# Or via command line:\n/scripts/suspendacct username "Non-payment"',
                'language': 'bash'
            },
            {
                'title': 'Terminate Account',
                'description': 'Remove hosting account.',
                'code': '# Account Functions > Terminate an Account\n\n# Select account\n# Confirm deletion\n# Optional: Keep DNS\n\n# Via command line:\n/scripts/removeacct username',
                'language': 'bash'
            },
            {
                'title': 'Account Transfer',
                'description': 'Migrate accounts between servers.',
                'code': '# In WHM:\n# Transfers > Transfer Tool\n\n# Remote Server:\nHostname: source.server.com\nUsername: root\nPassword: ****\n\n# Select accounts to transfer\n# Configure options\n# Start transfer',
                'language': 'text'
            }
        ],
        'postInstallation': {
            'title': 'Account Tips',
            'content': 'Use packages for consistent resource allocation. Enable account notifications. Monitor disk usage regularly. Set up automatic suspension for overuse.'
        }
    },
    {
        'title': 'Create cPanel Hosting Packages',
        'description': 'Design and configure hosting packages in WHM for reselling.',
        'category': 'web-hosting',
        'os': ['linux'],
        'difficulty': 'beginner',
        'tags': ['cpanel', 'whm', 'packages', 'reseller'],
        'steps': [
            {
                'title': 'Access Package Manager',
                'description': 'Navigate to package creation.',
                'code': '# In WHM:\n# Packages > Add a Package\n\n# Or edit existing:\n# Packages > Edit a Package',
                'language': 'text'
            },
            {
                'title': 'Basic Package Settings',
                'description': 'Configure core resources.',
                'code': '# Package Name: starter\n\n# Resources:\nDisk Quota: 5000 MB (5GB)\nMonthly Bandwidth: 50000 MB (50GB)\nMax FTP Accounts: 10\nMax Email Accounts: 25\nMax Mailing Lists: 5\nMax SQL Databases: 5\nMax Subdomains: 10\nMax Parked Domains: 5\nMax Addon Domains: 3',
                'language': 'text'
            },
            {
                'title': 'Advanced Options',
                'description': 'Configure additional settings.',
                'code': '# Advanced Settings:\n\nMax Hourly Email by Domain: 500\nMax % of CPU Usage: 25\nMax Concurrent Connections: 25\n\n# Features:\nCGI Access: Yes\nShell Access: No\ncPHulk Disabled: No\n\n# Locale: Default',
                'language': 'text'
            },
            {
                'title': 'Feature List Assignment',
                'description': 'Assign feature list to package.',
                'code': '# In WHM:\n# Packages > Feature Manager\n\n# Create feature list:\n# - Enable/disable cPanel features\n# - Save as "starter_features"\n\n# Assign to package:\n# Edit Package > Feature List: starter_features',
                'language': 'text'
            },
            {
                'title': 'Sample Packages',
                'description': 'Example package tiers.',
                'code': '# Starter Package:\nDisk: 5GB, Bandwidth: 50GB\nEmails: 25, Databases: 5\nAddons: 3\n\n# Business Package:\nDisk: 20GB, Bandwidth: 200GB\nEmails: 100, Databases: 20\nAddons: 10\n\n# Enterprise Package:\nDisk: 50GB, Bandwidth: 500GB\nEmails: Unlimited, Databases: 50\nAddons: 25',
                'language': 'text'
            }
        ],
        'postInstallation': {
            'title': 'Package Tips',
            'content': 'Create clear package names. Document package features for sales. Set reasonable limits. Review packages periodically. Use resource limits to prevent abuse.'
        }
    },
    {
        'title': 'Plesk Server Administration',
        'description': 'Essential Plesk server administration tasks and configuration.',
        'category': 'web-hosting',
        'os': ['linux', 'ubuntu', 'centos'],
        'difficulty': 'intermediate',
        'tags': ['plesk', 'administration', 'hosting', 'management'],
        'steps': [
            {
                'title': 'Create Subscription',
                'description': 'Set up new hosting subscription.',
                'code': '# In Plesk:\n# Customers > Add Customer\n\n# Or directly:\n# Subscriptions > Add Subscription\n\n# Details:\nDomain: example.com\nUsername: example_admin\nPassword: ****\nService Plan: Basic Hosting\n\n# Create',
                'language': 'text'
            },
            {
                'title': 'Configure Service Plans',
                'description': 'Create hosting service plans.',
                'code': '# Service Plans > Add Plan\n\n# Resources:\nDisk Space: 5 GB\nTraffic: 50 GB\nDomains: 5\nSubdomains: 10\nMailboxes: 25\nDatabases: 5\n\n# Permissions:\n# Enable/disable features\n# PHP version options',
                'language': 'text'
            },
            {
                'title': 'Manage Domains',
                'description': 'Domain management operations.',
                'code': '# Domains > Add Domain\n\n# Domain Settings:\nDomain name: newdomain.com\nDocument root: /httpdocs\nPHP Support: Yes\nPHP Version: 8.1\n\n# DNS Settings:\n# A Record: Server IP\n# MX Record: Mail server',
                'language': 'text'
            },
            {
                'title': 'Email Configuration',
                'description': 'Set up email services.',
                'code': '# Mail > Mail Settings\n\n# Configuration:\nMail Service: Enabled\nAnti-spam: SpamAssassin\nAntivirus: Yes\n\n# Create mailbox:\nMail > Create Email Address\nname@domain.com\nPassword: ****\nMailbox size: 500 MB',
                'language': 'text'
            },
            {
                'title': 'Backup Management',
                'description': 'Configure Plesk backups.',
                'code': '# Tools & Settings > Backup Manager\n\n# Schedule Backup:\nRun: Daily at 3:00 AM\nType: Full backup\nStore: Local + Remote FTP\n\n# Remote Storage:\nFTP Server: backup.server.com\nPath: /backups/plesk/',
                'language': 'text'
            }
        ],
        'postInstallation': {
            'title': 'Plesk Tips',
            'content': 'Use Plesk extensions for additional functionality. Enable fail2ban for security. Configure automatic updates. Monitor server resources via Plesk interface.'
        }
    },
    {
        'title': 'DirectAdmin Installation Guide',
        'description': 'Install and configure DirectAdmin control panel on Linux server.',
        'category': 'web-hosting',
        'os': ['linux', 'centos', 'debian'],
        'difficulty': 'intermediate',
        'tags': ['directadmin', 'installation', 'hosting', 'panel'],
        'steps': [
            {
                'title': 'System Preparation',
                'description': 'Prepare server for installation.',
                'code': '# Update system\nyum update -y  # CentOS\napt update && apt upgrade -y  # Debian/Ubuntu\n\n# Set hostname\nhostnamectl set-hostname server.yourdomain.com\n\n# Disable conflicting services\nsystemctl stop apache2 nginx postfix\nsystemctl disable apache2 nginx postfix',
                'language': 'bash'
            },
            {
                'title': 'Get License',
                'description': 'Obtain DirectAdmin license.',
                'code': '# Purchase license at directadmin.com\n# Get Client ID and License ID\n\n# Or request trial license:\n# Contact sales for 15-day trial',
                'language': 'text'
            },
            {
                'title': 'Run Installer',
                'description': 'Execute DirectAdmin installation.',
                'code': '# Download installer\nwget https://www.directadmin.com/setup.sh\nchmod +x setup.sh\n\n# Run installer\n./setup.sh auto\n\n# Or with options:\n./setup.sh auto uid=YOUR_CLIENT_ID lid=YOUR_LICENSE_ID hostname=server.domain.com email=admin@domain.com',
                'language': 'bash'
            },
            {
                'title': 'Post-Installation Setup',
                'description': 'Complete initial configuration.',
                'code': '# Access DirectAdmin:\nhttps://your_server_ip:2222\n\n# Login with credentials shown after installation\n# Or in: /usr/local/directadmin/conf/setup.txt\n\n# Change admin password:\n# Admin Settings > Change Password',
                'language': 'text'
            },
            {
                'title': 'Configure Services',
                'description': 'Set up web and email services.',
                'code': '# In DirectAdmin Admin:\n# Server Manager > PHP Config\n# Select PHP versions to install\n\n# Email:\n# Admin Settings > Mail Admin\n# Enable SpamAssassin\n# Configure mail limits\n\n# SSL:\n# SSL Certificates > Auto SSL\n# Enable Lets Encrypt',
                'language': 'text'
            }
        ],
        'postInstallation': {
            'title': 'DirectAdmin Tips',
            'content': 'DirectAdmin is lightweight and fast. Supports CustomBuild 2.0 for software management. Good for VPS with limited resources. Active community forums for support.'
        }
    },
    {
        'title': 'Set Up Reseller Hosting Business',
        'description': 'Complete guide to starting a reseller hosting business with WHM.',
        'category': 'web-hosting',
        'os': ['linux'],
        'difficulty': 'intermediate',
        'tags': ['reseller', 'cpanel', 'whm', 'business'],
        'steps': [
            {
                'title': 'Create Reseller Account',
                'description': 'Set up reseller in WHM.',
                'code': '# In WHM (root):\n# Resellers > Create a New Reseller\n\n# Account Details:\nUsername: reseller1\nDomain: reseller.example.com\nPassword: ****\nEmail: reseller@example.com\n\n# Resource Allocation:\nDisk Space: 50GB\nBandwidth: 500GB\nMax Accounts: 100',
                'language': 'text'
            },
            {
                'title': 'Configure Reseller Permissions',
                'description': 'Set reseller privileges.',
                'code': '# Reseller Center > Edit Reseller Privileges\n\n# Privileges:\n# - Create accounts\n# - Suspend accounts\n# - List accounts\n# - DNS Clustering\n# - Create packages\n\n# Resource Limits:\n# - Max accounts\n# - Disk/Bandwidth allocation',
                'language': 'text'
            },
            {
                'title': 'Create Reseller Packages',
                'description': 'Define packages for reseller clients.',
                'code': '# Login as Reseller in WHM:\n# Packages > Add a Package\n\n# Sample Reseller Packages:\n\n# Basic: 1GB disk, 10GB bandwidth\n# Standard: 5GB disk, 50GB bandwidth\n# Premium: 10GB disk, 100GB bandwidth',
                'language': 'text'
            },
            {
                'title': 'Set Up Nameservers',
                'description': 'Configure private nameservers.',
                'code': '# Create NS records:\nns1.yourbrand.com -> Server IP 1\nns2.yourbrand.com -> Server IP 2\n\n# In WHM:\n# Server Configuration > Nameserver IPs\n# Add private nameservers\n\n# At domain registrar:\n# Register ns1 and ns2 as child nameservers',
                'language': 'text'
            },
            {
                'title': 'Brand WHM/cPanel',
                'description': 'White-label control panels.',
                'code': '# WHM > cPanel > Customization\n\n# Branding Options:\n# - Upload custom logo\n# - Set company name\n# - Custom colors\n# - Hide cPanel branding\n\n# Custom hostname:\n# cpanel.yourbrand.com',
                'language': 'text'
            }
        ],
        'postInstallation': {
            'title': 'Business Tips',
            'content': 'Integrate with billing system (WHMCS/Blesta). Offer competitive pricing. Provide 24/7 support. Create knowledge base. Focus on specific niche markets.'
        }
    },
    {
        'title': 'SSL Certificate Installation Guide',
        'description': 'Install and manage SSL certificates on web hosting servers.',
        'category': 'web-hosting',
        'os': ['linux'],
        'difficulty': 'beginner',
        'tags': ['ssl', 'security', 'https', 'certificates'],
        'steps': [
            {
                'title': 'Generate CSR',
                'description': 'Create Certificate Signing Request.',
                'code': '# Via cPanel:\n# Security > SSL/TLS > Generate CSR\n\n# Fill details:\nDomains: example.com, www.example.com\nCity: New York\nState: NY\nCountry: US\nCompany: Your Company\n\n# Generate and copy CSR',
                'language': 'text'
            },
            {
                'title': 'Purchase SSL Certificate',
                'description': 'Buy SSL from certificate authority.',
                'code': '# Popular SSL providers:\n# - Comodo/Sectigo\n# - DigiCert\n# - GlobalSign\n# - GeoTrust\n\n# Submit CSR to provider\n# Complete domain validation\n# Receive certificate files',
                'language': 'text'
            },
            {
                'title': 'Install Certificate (cPanel)',
                'description': 'Install SSL in cPanel.',
                'code': '# In cPanel:\n# Security > SSL/TLS > Install SSL\n\n# Paste:\n# 1. Certificate (CRT)\n# 2. Private Key\n# 3. CA Bundle (intermediate)\n\n# Click Install Certificate',
                'language': 'text'
            },
            {
                'title': 'Free SSL with Lets Encrypt',
                'description': 'Install free SSL certificates.',
                'code': '# In cPanel:\n# Security > SSL/TLS Status\n# Click "Run AutoSSL"\n\n# Or via WHM:\n# SSL/TLS > Manage AutoSSL\n# Provider: Lets Encrypt\n# Run AutoSSL for all users',
                'language': 'text'
            },
            {
                'title': 'Force HTTPS',
                'description': 'Redirect all traffic to HTTPS.',
                'code': '# In .htaccess:\nRewriteEngine On\nRewriteCond %{HTTPS} off\nRewriteRule ^(.*)$ https://%{HTTP_HOST}%{REQUEST_URI} [L,R=301]\n\n# Or in cPanel:\n# Domains > Force HTTPS Redirect: ON',
                'language': 'apache'
            }
        ],
        'postInstallation': {
            'title': 'SSL Tips',
            'content': 'Use AutoSSL for easy management. Monitor certificate expiration. Use HSTS for additional security. Test with SSL Labs analyzer.'
        }
    },
    {
        'title': 'Email Server Configuration',
        'description': 'Set up and configure email services for web hosting.',
        'category': 'web-hosting',
        'os': ['linux'],
        'difficulty': 'intermediate',
        'tags': ['email', 'smtp', 'imap', 'hosting'],
        'steps': [
            {
                'title': 'Configure Mail Server',
                'description': 'Set up basic email settings.',
                'code': '# In WHM:\n# Service Configuration > Mailserver Configuration\n\n# Settings:\nMailserver: Dovecot\nMail Transfer Agent: Exim\nAnti-spam: SpamAssassin\nAntivirus: ClamAV',
                'language': 'text'
            },
            {
                'title': 'Set Up SPF Record',
                'description': 'Configure SPF for email authentication.',
                'code': '# In DNS Zone:\n# Add TXT record:\n\n# Basic SPF:\nv=spf1 +a +mx ~all\n\n# With specific IP:\nv=spf1 ip4:192.168.1.100 +a +mx ~all\n\n# Include other senders:\nv=spf1 include:_spf.google.com +a +mx ~all',
                'language': 'text'
            },
            {
                'title': 'Configure DKIM',
                'description': 'Enable DKIM signing.',
                'code': '# In WHM:\n# Email > DKIM Keys\n# Enable DKIM for domains\n\n# Or generate manually:\n# opendkim-genkey -d example.com -s default\n\n# Add DNS TXT record:\ndefault._domainkey.example.com\nv=DKIM1; k=rsa; p=MIGf...',
                'language': 'text'
            },
            {
                'title': 'Set Up DMARC',
                'description': 'Configure DMARC policy.',
                'code': '# Add DNS TXT record:\n_dmarc.example.com\n\n# DMARC record content:\nv=DMARC1; p=quarantine; rua=mailto:dmarc@example.com; pct=100\n\n# Policy options:\n# p=none (monitor only)\n# p=quarantine (spam folder)\n# p=reject (block)',
                'language': 'text'
            },
            {
                'title': 'Test Email Configuration',
                'description': 'Verify email setup.',
                'code': '# Test tools:\n# - mail-tester.com (score check)\n# - mxtoolbox.com (DNS check)\n# - Google Postmaster Tools\n\n# Send test email:\necho "Test" | mail -s "Test Email" test@gmail.com\n\n# Check mail queue:\nexim -bp\nmailq',
                'language': 'bash'
            }
        ],
        'postInstallation': {
            'title': 'Email Best Practices',
            'content': 'Monitor mail queue regularly. Set rate limits to prevent spam. Use rDNS (PTR record). Configure proper MX records. Enable greylisting for spam reduction.'
        }
    },
    {
        'title': 'Domain DNS Management',
        'description': 'Complete guide to managing DNS zones and records for domains.',
        'category': 'web-hosting',
        'os': ['linux'],
        'difficulty': 'beginner',
        'tags': ['dns', 'domains', 'nameservers', 'records'],
        'steps': [
            {
                'title': 'Access DNS Zone Editor',
                'description': 'Navigate to DNS management.',
                'code': '# In cPanel:\n# Domains > Zone Editor\n\n# In WHM:\n# DNS Functions > Edit DNS Zone\n\n# Select domain to edit',
                'language': 'text'
            },
            {
                'title': 'Common DNS Records',
                'description': 'Understanding record types.',
                'code': '# A Record - Points domain to IP\nexample.com  A  192.168.1.100\n\n# CNAME - Alias for another domain\nwww  CNAME  example.com\n\n# MX Record - Mail server\n@  MX  10  mail.example.com\n\n# TXT Record - Text information\n@  TXT  "v=spf1 +a +mx ~all"\n\n# AAAA Record - IPv6 address\n@  AAAA  2001:db8::1',
                'language': 'text'
            },
            {
                'title': 'Add Subdomain',
                'description': 'Create subdomain DNS entry.',
                'code': '# For subdomain: blog.example.com\n\n# A Record:\nblog  A  192.168.1.100\n\n# Or point to different server:\nblog  A  203.0.113.50\n\n# For external service:\nshop  CNAME  shops.myshopify.com',
                'language': 'text'
            },
            {
                'title': 'Configure MX Records',
                'description': 'Set up email routing.',
                'code': '# Local mail server:\n@  MX  0  mail.example.com\nmail  A  192.168.1.100\n\n# Google Workspace:\n@  MX  1  aspmx.l.google.com\n@  MX  5  alt1.aspmx.l.google.com\n@  MX  10  alt2.aspmx.l.google.com\n\n# Microsoft 365:\n@  MX  0  example-com.mail.protection.outlook.com',
                'language': 'text'
            },
            {
                'title': 'DNS Propagation',
                'description': 'Check DNS updates.',
                'code': '# Check propagation:\n# whatsmydns.net\n# dnschecker.org\n\n# Command line check:\ndig example.com A +short\ndig example.com MX +short\nnslookup example.com 8.8.8.8\n\n# Propagation takes 1-48 hours\n# Lower TTL for faster updates',
                'language': 'bash'
            }
        ],
        'postInstallation': {
            'title': 'DNS Tips',
            'content': 'Always keep backup of DNS records. Use low TTL before major changes. Test changes with nslookup. Document all custom records.'
        }
    }
]

# Additional WHMCS articles to reach 50+
more_whmcs_articles = [
    {
        'title': 'WHMCS Order Form Customization',
        'description': 'Customize WHMCS order forms for better conversion and user experience.',
        'category': 'billing',
        'os': ['linux'],
        'difficulty': 'intermediate',
        'tags': ['whmcs', 'orderform', 'customization', 'templates'],
        'steps': [
            {
                'title': 'Access Order Form Templates',
                'description': 'Navigate to order form settings.',
                'code': '# In WHMCS Admin:\n# Setup > Ordering > Order Form Templates\n\n# Available templates:\n# - Standard Cart\n# - Premium Comparison\n# - Ajax Cart\n# - Vertical Steps',
                'language': 'text'
            },
            {
                'title': 'Customize Template',
                'description': 'Edit order form template.',
                'code': '# Template location:\n/templates/orderforms/standard_cart/\n\n# Key files:\n# - viewcart.tpl\n# - checkout.tpl\n# - products.tpl\n# - configureproduct.tpl\n\n# Copy to custom template:\ncp -r standard_cart custom_cart',
                'language': 'bash'
            },
            {
                'title': 'Add Custom Fields',
                'description': 'Create additional order fields.',
                'code': '# Setup > Custom Client Fields\n# Or per-product:\n# Product > Custom Fields\n\n# Field Types:\n# - Text Box\n# - Text Area\n# - Dropdown\n# - Checkbox\n# - File Upload',
                'language': 'text'
            },
            {
                'title': 'Configure Checkout Flow',
                'description': 'Optimize checkout process.',
                'code': '# Setup > Ordering > General Settings\n\n# Options:\n# - Allow guest checkout\n# - Show promo code field\n# - Terms of Service URL\n# - Required custom fields\n# - Default payment method',
                'language': 'text'
            }
        ],
        'postInstallation': {
            'title': 'Conversion Tips',
            'content': 'Keep checkout simple. Reduce required fields. Show trust badges. Offer multiple payment options. Use clear pricing.'
        }
    },
    {
        'title': 'WHMCS Client Area Customization',
        'description': 'Customize the WHMCS client area template and functionality.',
        'category': 'billing',
        'os': ['linux'],
        'difficulty': 'intermediate',
        'tags': ['whmcs', 'clientarea', 'templates', 'customization'],
        'steps': [
            {
                'title': 'Select Template',
                'description': 'Choose client area template.',
                'code': '# Setup > General Settings > System\n# Template: Twenty-One (or others)\n\n# Available templates:\n# - Twenty-One (default)\n# - Six\n# - Portal\n# - Starter',
                'language': 'text'
            },
            {
                'title': 'Customize Colors',
                'description': 'Change template colors.',
                'code': '# Edit: /templates/twenty-one/css/custom.css\n\n:root {\n  --primary-color: #4e73df;\n  --secondary-color: #858796;\n  --success-color: #1cc88a;\n  --info-color: #36b9cc;\n  --warning-color: #f6c23e;\n  --danger-color: #e74a3b;\n}',
                'language': 'css'
            },
            {
                'title': 'Add Custom Menu Items',
                'description': 'Modify navigation menus.',
                'code': '<?php\n// includes/hooks/custom_menu.php\n\nadd_hook(\'ClientAreaPrimaryNavbar\', 1, function($navbar) {\n    $navbar->addChild(\'Custom Link\')\n        ->setUri(\'https://example.com/docs\')\n        ->setOrder(100);\n});\n\nadd_hook(\'ClientAreaSecondarySidebar\', 1, function($sidebar) {\n    $sidebar->addChild(\'Support\')\n        ->setLabel(\'Quick Support\')\n        ->setUri(\'submitticket.php\');\n});',
                'language': 'php'
            },
            {
                'title': 'Custom Homepage Panels',
                'description': 'Add panels to client dashboard.',
                'code': '<?php\n// includes/hooks/custom_panels.php\n\nadd_hook(\'ClientAreaHomepagePanels\', 1, function($homePagePanels) {\n    $homePagePanels->addChild(\'announcements\')\n        ->setLabel(\'Announcements\')\n        ->setBodyContent(\'<p>Custom content here</p>\')\n        ->setOrder(0);\n});',
                'language': 'php'
            }
        ],
        'postInstallation': {
            'title': 'Customization Tips',
            'content': 'Create child template for upgrades. Test on mobile devices. Keep branding consistent. Use hooks instead of editing core files.'
        }
    },
    {
        'title': 'WHMCS SolusVM Module Setup',
        'description': 'Integrate SolusVM with WHMCS for automated VPS provisioning.',
        'category': 'billing',
        'os': ['linux'],
        'difficulty': 'intermediate',
        'tags': ['whmcs', 'solusvm', 'vps', 'automation'],
        'steps': [
            {
                'title': 'Download SolusVM Module',
                'description': 'Get the WHMCS module from SolusVM.',
                'code': '# In SolusVM Master:\n# Configuration > WHMCS Module\n# Download the module ZIP\n\n# Extract to WHMCS:\nunzip solusvm_whmcs.zip -d /home/user/public_html/billing/modules/servers/',
                'language': 'bash'
            },
            {
                'title': 'Configure Server',
                'description': 'Add SolusVM server in WHMCS.',
                'code': '# Setup > Products > Servers > Add New\n\nName: SolusVM Master\nHostname: master.example.com\nIP Address: 192.168.1.100\n\nModule: SolusVM\nAPI ID: (from SolusVM)\nAPI Key: (from SolusVM)',
                'language': 'text'
            },
            {
                'title': 'Create VPS Product',
                'description': 'Set up VPS hosting product.',
                'code': '# Products > Create Product\n\nType: Server/VPS\nName: KVM VPS Basic\n\n# Module Settings:\nModule: SolusVM\nServer: SolusVM Master\nVirtualization: KVM\nNode/Group: Select node\nDefault OS: CentOS 7',
                'language': 'text'
            },
            {
                'title': 'Configure Options',
                'description': 'Set up configurable options.',
                'code': '# Products > Configurable Options\n# Create Group: VPS Options\n\n# Options:\n# - Extra RAM (per GB)\n# - Extra Disk (per GB)\n# - Extra IPs\n# - Operating System (dropdown)\n\n# Assign to VPS products',
                'language': 'text'
            }
        ],
        'postInstallation': {
            'title': 'Integration Tips',
            'content': 'Sync OS templates regularly. Test provisioning thoroughly. Set up reinstall/reboot client functions. Configure email templates.'
        }
    },
    {
        'title': 'WHMCS Virtualizor Module Setup',
        'description': 'Connect Virtualizor panel with WHMCS for VPS automation.',
        'category': 'billing',
        'os': ['linux'],
        'difficulty': 'intermediate',
        'tags': ['whmcs', 'virtualizor', 'vps', 'automation'],
        'steps': [
            {
                'title': 'Get Virtualizor Module',
                'description': 'Download WHMCS integration module.',
                'code': '# From Virtualizor Admin:\n# API Credentials > WHMCS Module\n# Download the latest module\n\n# Extract:\nunzip virtualizor_whmcs.zip -d /path/to/whmcs/modules/servers/',
                'language': 'bash'
            },
            {
                'title': 'Add Server in WHMCS',
                'description': 'Configure Virtualizor server.',
                'code': '# Setup > Servers > Add New Server\n\nName: Virtualizor Main\nHostname: virt.example.com\nPort: 4085\n\nModule: Virtualizor\nAPI Key: (from Virtualizor)\nAPI Password: (from Virtualizor)\nSecure: Yes',
                'language': 'text'
            },
            {
                'title': 'Create VPS Product',
                'description': 'Set up VPS product in WHMCS.',
                'code': '# Products > Create Product\n\nType: Server/VPS\nGroup: VPS Hosting\nName: Cloud VPS 1\n\n# Module Settings:\nModule: Virtualizor\nServer: Virtualizor Main\nPlan: kvm_plan_1\nServer Group: default',
                'language': 'text'
            },
            {
                'title': 'Enable Client Area Functions',
                'description': 'Allow client VPS management.',
                'code': '# In Product Module Settings:\n\n# Enable:\n# - Start/Stop/Restart\n# - Console Access (VNC/noVNC)\n# - OS Reinstall\n# - Resource Usage Stats\n# - Backup Management\n# - IP Management',
                'language': 'text'
            }
        ],
        'postInstallation': {
            'title': 'Tips',
            'content': 'Configure welcome email with VPS details. Set up automatic backups. Enable client API access if needed. Test all lifecycle functions.'
        }
    },
    {
        'title': 'WHMCS Affiliate System Configuration',
        'description': 'Set up and manage WHMCS affiliate marketing system.',
        'category': 'billing',
        'os': ['linux'],
        'difficulty': 'beginner',
        'tags': ['whmcs', 'affiliate', 'marketing', 'commission'],
        'steps': [
            {
                'title': 'Enable Affiliate System',
                'description': 'Activate affiliates in WHMCS.',
                'code': '# Setup > General Settings > Affiliates\n\n# Settings:\nAffiliate System: Enabled\nAffiliate Commission: 10%\nBonus Deposit: $0.00\nPayout Minimum: $50.00\nPayout Method: PayPal/Bank Transfer',
                'language': 'text'
            },
            {
                'title': 'Configure Commission Rates',
                'description': 'Set up commission structure.',
                'code': '# Global commission:\nDefault Commission: 10%\n\n# Per-product commission:\n# Edit Product > Other tab\nAffiliate Commission Type: Percentage\nAffiliate Commission: 15%\n\n# Or One-Time vs Recurring:\nPay Once: Yes/No',
                'language': 'text'
            },
            {
                'title': 'Affiliate Registration',
                'description': 'Allow client affiliate signup.',
                'code': '# Clients become affiliates at:\n/affiliates.php\n\n# Or auto-enable:\n# All clients are affiliates\n# Setup > Affiliates > Auto Activate\n\n# Affiliate link format:\nhttps://yourdomain.com/?aff=AFFILIATE_ID',
                'language': 'text'
            },
            {
                'title': 'Manage Affiliates',
                'description': 'Review and manage affiliate accounts.',
                'code': '# Orders > Affiliates\n\n# View:\n# - Active affiliates\n# - Pending commissions\n# - Commission history\n# - Withdrawal requests\n\n# Actions:\n# - Approve withdrawals\n# - Adjust commissions\n# - View referral details',
                'language': 'text'
            }
        ],
        'postInstallation': {
            'title': 'Affiliate Tips',
            'content': 'Provide marketing materials. Set clear terms and conditions. Process payouts promptly. Track top performers. Consider tiered commissions.'
        }
    },
    {
        'title': 'WHMCS Support Ticket System',
        'description': 'Configure and optimize WHMCS support ticket management.',
        'category': 'billing',
        'os': ['linux'],
        'difficulty': 'beginner',
        'tags': ['whmcs', 'support', 'tickets', 'helpdesk'],
        'steps': [
            {
                'title': 'Configure Departments',
                'description': 'Set up support departments.',
                'code': '# Setup > Support > Support Departments\n# Add Department\n\nName: Technical Support\nDescription: Server and hosting issues\nEmail: support@example.com\nAssigned Admins: Select staff\nClients Only: Yes\nPipe Replies Only: No',
                'language': 'text'
            },
            {
                'title': 'Email Piping Setup',
                'description': 'Enable email-to-ticket conversion.',
                'code': '# In cPanel:\n# Email > Forwarders > Add Forwarder\n\n# Forward to script:\nsupport@yourdomain.com\nPipe to: /home/user/public_html/billing/pipe.php\n\n# Or add email pipe:\n|/usr/bin/php -q /home/user/public_html/billing/pipe.php',
                'language': 'text'
            },
            {
                'title': 'Predefined Replies',
                'description': 'Create canned responses.',
                'code': '# Setup > Support > Predefined Replies\n# Add New Reply\n\nName: Password Reset\nCategory: Common Issues\nReply:\nDear {$client_name},\n\nTo reset your password, please visit:\n{$whmcs_url}password/reset\n\nBest regards,\nSupport Team',
                'language': 'text'
            },
            {
                'title': 'Ticket Escalation',
                'description': 'Set up auto-escalation rules.',
                'code': '# Setup > Automation Settings\n\n# Escalation Rules:\nEscalate After: 24 hours\nEscalate To: Senior Support\nNotify: Department Manager\n\n# Custom via hook:\n// Check old tickets and escalate',
                'language': 'text'
            }
        ],
        'postInstallation': {
            'title': 'Support Tips',
            'content': 'Create comprehensive predefined replies. Set SLA targets. Use ticket priorities. Enable client satisfaction ratings. Monitor response times.'
        }
    },
    {
        'title': 'WHMCS Reporting and Analytics',
        'description': 'Generate and analyze business reports in WHMCS.',
        'category': 'billing',
        'os': ['linux'],
        'difficulty': 'beginner',
        'tags': ['whmcs', 'reports', 'analytics', 'business'],
        'steps': [
            {
                'title': 'Access Reports',
                'description': 'Navigate to reporting section.',
                'code': '# In WHMCS Admin:\n# Reports > Reports\n\n# Report Categories:\n# - Billing Reports\n# - Client Reports\n# - Income Reports\n# - Support Reports\n# - Transaction Reports',
                'language': 'text'
            },
            {
                'title': 'Key Reports Overview',
                'description': 'Important business reports.',
                'code': '# Income Reports:\n# - Income by Date Range\n# - Transactions List\n# - Monthly Income Summary\n\n# Client Reports:\n# - Active Clients\n# - Client States\n# - New Registrations\n\n# Service Reports:\n# - Products/Services Summary\n# - Domain Statistics',
                'language': 'text'
            },
            {
                'title': 'Schedule Reports',
                'description': 'Automate report delivery.',
                'code': '# Setup > Staff Management > Edit Staff\n# Enable: Daily Report Email\n\n# Content includes:\n# - New orders\n# - Pending orders\n# - Overdue invoices\n# - Support tickets\n# - Revenue summary',
                'language': 'text'
            },
            {
                'title': 'Custom Reports',
                'description': 'Create custom report modules.',
                'code': '<?php\n// modules/reports/my_report.php\n\n$reportdata["title"] = "Custom Report";\n$reportdata["description"] = "My custom report";\n\n$query = "SELECT * FROM tblhosting WHERE domainstatus=\'Active\'";\n$result = full_query($query);\n\nwhile ($data = mysql_fetch_array($result)) {\n    $reportdata["tabledata"][] = array(\n        $data[\'domain\'],\n        $data[\'regdate\'],\n        $data[\'amount\'],\n    );\n}',
                'language': 'php'
            }
        ],
        'postInstallation': {
            'title': 'Analytics Tips',
            'content': 'Review reports weekly. Track MRR and churn. Monitor support metrics. Export to spreadsheets for analysis. Set up dashboard widgets.'
        }
    }
]

async def seed_database():
    all_articles = whmcs_articles + billing_articles + webhosting_articles + more_whmcs_articles
    
    added_count = 0
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
        added_count += 1
    
    total = await db.code_snippets.count_documents({})
    print(f"\n--- Summary ---")
    print(f"New articles added: {added_count}")
    print(f"Total articles in database: {total}")

if __name__ == "__main__":
    asyncio.run(seed_database())
