#!/bin/bash
# Auto-update script for 9xCodes
# This runs as a standalone script to avoid subprocess signal issues

PROJECT_PATH="/var/www/9xcodes"
LOG_FILE="/tmp/9xcodes_update.log"
VENV_PIP="$PROJECT_PATH/backend/venv/bin/pip"

echo "[$(date)] Update started" > "$LOG_FILE"

# Step 1: Git Pull
echo "[INFO] >> Git Pull" >> "$LOG_FILE"
cd "$PROJECT_PATH"
git pull origin main >> "$LOG_FILE" 2>&1
if [ $? -ne 0 ]; then
    echo "[ERROR] Git pull failed" >> "$LOG_FILE"
    echo "RESULT:failed" >> "$LOG_FILE"
    exit 1
fi
echo "[INFO] Git Pull completed" >> "$LOG_FILE"

# Step 2: Backend Dependencies
echo "[INFO] >> Backend Dependencies" >> "$LOG_FILE"
cd "$PROJECT_PATH/backend"
$VENV_PIP install -r requirements.txt >> "$LOG_FILE" 2>&1
echo "[INFO] Backend deps done" >> "$LOG_FILE"

# Step 3: Frontend Build
echo "[INFO] >> Frontend Build" >> "$LOG_FILE"
cd "$PROJECT_PATH/frontend"
export NODE_OPTIONS="--max_old_space_size=1024"
yarn build >> "$LOG_FILE" 2>&1
BUILD_STATUS=$?
if [ $BUILD_STATUS -ne 0 ]; then
    echo "[ERROR] Frontend build failed (exit: $BUILD_STATUS)" >> "$LOG_FILE"
    echo "[INFO] Trying with npm..." >> "$LOG_FILE"
    npm run build >> "$LOG_FILE" 2>&1
    if [ $? -ne 0 ]; then
        echo "[ERROR] npm build also failed" >> "$LOG_FILE"
        echo "RESULT:failed" >> "$LOG_FILE"
        exit 1
    fi
fi
echo "[INFO] Frontend Build completed" >> "$LOG_FILE"

# Step 4: PM2 Restart
echo "[INFO] >> PM2 Restart" >> "$LOG_FILE"
pm2 restart all >> "$LOG_FILE" 2>&1
echo "[INFO] PM2 Restart done" >> "$LOG_FILE"

echo "[$(date)] Update completed successfully" >> "$LOG_FILE"
echo "RESULT:success" >> "$LOG_FILE"
