#!/bin/bash
# Auto-update script for 9xCodes
# This runs as a standalone script to avoid subprocess signal issues

PROJECT_PATH="/var/www/9xcodes"
LOG_FILE="/tmp/9xcodes_update.log"
STATUS_FILE="/tmp/9xcodes_update_status.json"
VENV_PIP="$PROJECT_PATH/backend/venv/bin/pip"
EXTRA_INDEX="--extra-index-url https://d33sy5i8bnduwe.cloudfront.net/simple/"

echo "[$(date)] Update started" > "$LOG_FILE"

# Step 1: Git Pull
echo "[INFO] >> Git Pull" >> "$LOG_FILE"
cd "$PROJECT_PATH"
git stash >> "$LOG_FILE" 2>&1
git pull origin main >> "$LOG_FILE" 2>&1
if [ $? -ne 0 ]; then
    echo "[ERROR] Git pull failed" >> "$LOG_FILE"
    echo "RESULT:failed" >> "$LOG_FILE"
    echo '{"is_running":false,"last_run":"'$(date -u +%Y-%m-%dT%H:%M:%S)'","last_status":"failed","step":"Done"}' > "$STATUS_FILE"
    exit 1
fi
echo "[INFO] Git Pull completed" >> "$LOG_FILE"

# Step 2: Backend Dependencies
echo "[INFO] >> Backend Dependencies" >> "$LOG_FILE"
cd "$PROJECT_PATH/backend"
$VENV_PIP install -r requirements.txt $EXTRA_INDEX >> "$LOG_FILE" 2>&1
echo "[INFO] Backend deps done" >> "$LOG_FILE"

# Step 3: Frontend Build
echo "[INFO] >> Frontend Build" >> "$LOG_FILE"
cd "$PROJECT_PATH/frontend"
export NODE_OPTIONS="--max_old_space_size=1024"
yarn build >> "$LOG_FILE" 2>&1

# Check if build folder was created/updated recently (within last 2 minutes)
if [ -d "$PROJECT_PATH/frontend/build" ] && [ -n "$(find $PROJECT_PATH/frontend/build -name 'index.html' -mmin -2 2>/dev/null)" ]; then
    echo "[INFO] Frontend Build completed (build folder verified)" >> "$LOG_FILE"
else
    echo "[WARN] yarn build may have issues, trying npm..." >> "$LOG_FILE"
    npm run build >> "$LOG_FILE" 2>&1
    if [ ! -d "$PROJECT_PATH/frontend/build" ]; then
        echo "[ERROR] Frontend build failed completely" >> "$LOG_FILE"
        echo "RESULT:failed" >> "$LOG_FILE"
        echo '{"is_running":false,"last_run":"'$(date -u +%Y-%m-%dT%H:%M:%S)'","last_status":"failed","step":"Done"}' > "$STATUS_FILE"
        exit 1
    fi
    echo "[INFO] Frontend Build completed via npm" >> "$LOG_FILE"
fi

# Step 4: Write success BEFORE pm2 restart (pm2 restart kills the backend process)
echo "[$(date)] Update completed successfully" >> "$LOG_FILE"
echo "RESULT:success" >> "$LOG_FILE"
echo '{"is_running":false,"last_run":"'$(date -u +%Y-%m-%dT%H:%M:%S)'","last_status":"success","step":"Done"}' > "$STATUS_FILE"

# Step 5: PM2 Restart (this will kill the backend, so we do it LAST after writing result)
echo "[INFO] >> PM2 Restart" >> "$LOG_FILE"
pm2 restart all >> "$LOG_FILE" 2>&1
