# 9xcodes.com - Ubuntu 22 VPS Deployment Guide

Complete step-by-step guide to deploy 9xcodes.com on your Ubuntu 22 VPS server.

---

## Prerequisites
- Ubuntu 22.04 LTS VPS
- Root or sudo access
- Domain: 9xcodes.com (pointed to your VPS IP)

---

## Step 1: Point Domain to VPS

Before starting, update your domain's DNS settings:
1. Go to your domain registrar (GoDaddy, Namecheap, etc.)
2. Add/Update **A Record**:
   - **Host**: `@`
   - **Value**: `YOUR_VPS_IP_ADDRESS`
   - **TTL**: 300 or Auto
3. Add another **A Record** for www:
   - **Host**: `www`
   - **Value**: `YOUR_VPS_IP_ADDRESS`
4. Wait 5-15 minutes for DNS propagation

---

## Step 2: Update System

```bash
# SSH into your VPS
ssh root@YOUR_VPS_IP

# Update system packages
sudo apt update && sudo apt upgrade -y
```

---

## Step 3: Install Node.js 20.x

```bash
# Install Node.js 20.x
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt install -y nodejs

# Verify installation
node --version
npm --version

# Install Yarn globally
sudo npm install -g yarn
```

---

## Step 4: Install Python 3.11 & pip

```bash
# Install Python and pip
sudo apt install -y python3 python3-pip python3-venv

# Verify installation
python3 --version
pip3 --version
```

---

## Step 5: Install MongoDB 7.0

```bash
# Import MongoDB public GPG key
curl -fsSL https://www.mongodb.org/static/pgp/server-7.0.asc | \
   sudo gpg -o /usr/share/keyrings/mongodb-server-7.0.gpg --dearmor

# Add MongoDB repository
echo "deb [ arch=amd64,arm64 signed-by=/usr/share/keyrings/mongodb-server-7.0.gpg ] https://repo.mongodb.org/apt/ubuntu jammy/mongodb-org/7.0 multiverse" | \
   sudo tee /etc/apt/sources.list.d/mongodb-org-7.0.list

# Update and install MongoDB
sudo apt update
sudo apt install -y mongodb-org

# Start and enable MongoDB
sudo systemctl start mongod
sudo systemctl enable mongod

# Verify MongoDB is running
sudo systemctl status mongod
```

---

## Step 6: Install Nginx

```bash
# Install Nginx
sudo apt install -y nginx

# Start and enable Nginx
sudo systemctl start nginx
sudo systemctl enable nginx
```

---

## Step 7: Install PM2 (Process Manager)

```bash
# Install PM2 globally
sudo npm install -g pm2
```

---

## Step 8: Upload Code to VPS

**Option A: Using SCP (from your local machine)**
```bash
# Download code from Emergent platform (ZIP file)
# Then upload to VPS
scp 9xcodes-code.zip root@YOUR_VPS_IP:/var/www/
```

**Option B: Using Git (if you pushed to GitHub)**
```bash
# On VPS
cd /var/www
git clone https://github.com/YOUR_USERNAME/9xcodes.git
```

---

## Step 9: Setup Backend

```bash
# Navigate to backend folder
cd /var/www/9xcodes/backend

# Create Python virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt

# Create/Edit .env file
nano .env
```

**Backend .env file content:**
```env
MONGO_URL="mongodb://localhost:27017"
DB_NAME="9xcodes_db"
CORS_ORIGINS="https://9xcodes.com,https://www.9xcodes.com"
JWT_SECRET="your-super-secret-jwt-key-change-this-to-random-string"
```

**Save file:** Press `Ctrl+X`, then `Y`, then `Enter`

---

## Step 10: Setup Frontend

```bash
# Navigate to frontend folder
cd /var/www/9xcodes/frontend

# Create/Edit .env file
nano .env
```

**Frontend .env file content:**
```env
REACT_APP_BACKEND_URL=https://9xcodes.com
```

**Save and install dependencies:**
```bash
# Install dependencies
yarn install

# Build production version
yarn build
```

---

## Step 11: Start Backend with PM2

```bash
# Navigate to backend
cd /var/www/9xcodes/backend

# Activate virtual environment
source venv/bin/activate

# Start backend with PM2
pm2 start "uvicorn server:app --host 0.0.0.0 --port 8001" --name "9xcodes-backend"

# Save PM2 configuration
pm2 save

# Setup PM2 to start on boot
pm2 startup systemd
# Run the command it shows you
```

---

## Step 12: Configure Nginx

```bash
# Create Nginx config file
sudo nano /etc/nginx/sites-available/9xcodes.com
```

**Paste this configuration:**
```nginx
server {
    listen 80;
    server_name 9xcodes.com www.9xcodes.com;

    # Frontend - React static files
    root /var/www/9xcodes/frontend/build;
    index index.html;

    # Gzip compression
    gzip on;
    gzip_types text/plain text/css application/json application/javascript text/xml application/xml;

    # API routes - Proxy to backend
    location /api/ {
        proxy_pass http://127.0.0.1:8001/api/;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
        proxy_read_timeout 90;
    }

    # React Router - Handle all frontend routes
    location / {
        try_files $uri $uri/ /index.html;
    }

    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
}
```

**Enable the site:**
```bash
# Create symbolic link
sudo ln -s /etc/nginx/sites-available/9xcodes.com /etc/nginx/sites-enabled/

# Remove default site (optional)
sudo rm /etc/nginx/sites-enabled/default

# Test Nginx configuration
sudo nginx -t

# Restart Nginx
sudo systemctl restart nginx
```

---

## Step 13: Install SSL Certificate (HTTPS)

```bash
# Install Certbot
sudo apt install -y certbot python3-certbot-nginx

# Get SSL certificate
sudo certbot --nginx -d 9xcodes.com -d www.9xcodes.com

# Follow the prompts:
# - Enter email address
# - Agree to terms
# - Choose redirect HTTP to HTTPS (option 2)

# Auto-renewal test
sudo certbot renew --dry-run
```

---

## Step 14: Seed Initial Data (First time only)

```bash
# Navigate to backend
cd /var/www/9xcodes/backend

# Activate virtual environment
source venv/bin/activate

# Run seed scripts to add articles
python seed_data.py
python seed_more_computers.py
python seed_networking_virtualization.py
python seed_billing_hosting.py
python seed_more_articles.py

# This will add 220+ articles to your database
```

---

## Step 15: Setup Firewall

```bash
# Allow SSH, HTTP, HTTPS
sudo ufw allow ssh
sudo ufw allow 'Nginx Full'

# Enable firewall
sudo ufw enable

# Check status
sudo ufw status
```

---

## Verification Checklist

After completing all steps, verify:

1. **MongoDB Running:**
   ```bash
   sudo systemctl status mongod
   ```

2. **Backend Running:**
   ```bash
   pm2 status
   curl http://localhost:8001/api/snippets
   ```

3. **Nginx Running:**
   ```bash
   sudo systemctl status nginx
   ```

4. **Website Accessible:**
   - Open https://9xcodes.com in browser
   - Check if articles are loading
   - Test admin login at https://9xcodes.com/login

---

## Admin Login Credentials

- **URL:** https://9xcodes.com/login
- **Username:** admin
- **Password:** admin123

⚠️ **IMPORTANT:** After first login, immediately change your password from Admin Panel!

---

## Useful Commands

```bash
# Check backend logs
pm2 logs 9xcodes-backend

# Restart backend
pm2 restart 9xcodes-backend

# Restart Nginx
sudo systemctl restart nginx

# Check MongoDB status
sudo systemctl status mongod

# View Nginx error logs
sudo tail -f /var/log/nginx/error.log
```

---

## Troubleshooting

### Backend not starting?
```bash
cd /var/www/9xcodes/backend
source venv/bin/activate
python server.py
# Check for any errors
```

### MongoDB connection error?
```bash
sudo systemctl restart mongod
mongo
# Should open MongoDB shell
```

### 502 Bad Gateway?
```bash
# Check if backend is running
pm2 status
pm2 restart 9xcodes-backend
```

### Permission issues?
```bash
sudo chown -R www-data:www-data /var/www/9xcodes
sudo chmod -R 755 /var/www/9xcodes
```

---

## Updating Website

When you want to update the code:

```bash
# Pull latest code (if using Git)
cd /var/www/9xcodes
git pull

# Rebuild frontend
cd frontend
yarn install
yarn build

# Restart backend
pm2 restart 9xcodes-backend
```

---

## Support

If you face any issues, check:
1. PM2 logs: `pm2 logs`
2. Nginx logs: `sudo tail -f /var/log/nginx/error.log`
3. MongoDB logs: `sudo tail -f /var/log/mongodb/mongod.log`

---

**Deployment Guide Created for 9xcodes.com**
**Date: December 2025**
