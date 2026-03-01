#!/bin/bash

# 9xcodes.com - Quick Setup Script for Ubuntu 22.04
# Run as root: sudo bash setup.sh

set -e

echo "========================================="
echo "  9xcodes.com - Ubuntu 22 Setup Script  "
echo "========================================="

# Update system
echo "[1/8] Updating system..."
apt update && apt upgrade -y

# Install Node.js 20.x
echo "[2/8] Installing Node.js 20.x..."
curl -fsSL https://deb.nodesource.com/setup_20.x | bash -
apt install -y nodejs
npm install -g yarn pm2

# Install Python
echo "[3/8] Installing Python..."
apt install -y python3 python3-pip python3-venv

# Install MongoDB 7.0
echo "[4/8] Installing MongoDB 7.0..."
curl -fsSL https://www.mongodb.org/static/pgp/server-7.0.asc | \
   gpg -o /usr/share/keyrings/mongodb-server-7.0.gpg --dearmor
echo "deb [ arch=amd64,arm64 signed-by=/usr/share/keyrings/mongodb-server-7.0.gpg ] https://repo.mongodb.org/apt/ubuntu jammy/mongodb-org/7.0 multiverse" | \
   tee /etc/apt/sources.list.d/mongodb-org-7.0.list
apt update
apt install -y mongodb-org
systemctl start mongod
systemctl enable mongod

# Install Nginx
echo "[5/8] Installing Nginx..."
apt install -y nginx
systemctl start nginx
systemctl enable nginx

# Install Certbot
echo "[6/8] Installing Certbot..."
apt install -y certbot python3-certbot-nginx

# Setup Firewall
echo "[7/8] Configuring Firewall..."
ufw allow ssh
ufw allow 'Nginx Full'
ufw --force enable

echo "[8/8] Setup Complete!"
echo ""
echo "========================================="
echo "  Next Steps:                           "
echo "========================================="
echo "1. Upload your code to /var/www/9xcodes/"
echo "2. Setup backend: cd /var/www/9xcodes/backend"
echo "   - python3 -m venv venv"
echo "   - source venv/bin/activate"
echo "   - pip install -r requirements.txt"
echo "   - nano .env (configure environment)"
echo ""
echo "3. Setup frontend: cd /var/www/9xcodes/frontend"
echo "   - nano .env (configure environment)"
echo "   - yarn install"
echo "   - yarn build"
echo ""
echo "4. Start backend with PM2:"
echo "   - pm2 start 'uvicorn server:app --host 0.0.0.0 --port 8001' --name '9xcodes-backend'"
echo ""
echo "5. Configure Nginx (see DEPLOYMENT_GUIDE.md)"
echo ""
echo "6. Get SSL: sudo certbot --nginx -d 9xcodes.com -d www.9xcodes.com"
echo "========================================="
