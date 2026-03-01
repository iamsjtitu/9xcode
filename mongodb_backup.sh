#!/bin/bash

# 9xcodes.com MongoDB Backup Script
# This script creates daily backups of your MongoDB database

# Configuration
BACKUP_DIR="/var/backups/mongodb"
DB_NAME="9xcodes_db"
DATE=$(date +%Y-%m-%d_%H-%M-%S)
BACKUP_PATH="$BACKUP_DIR/$DB_NAME-$DATE"
RETENTION_DAYS=7  # Keep backups for 7 days

# Create backup directory if it doesn't exist
mkdir -p $BACKUP_DIR

# Create backup
echo "Starting backup of $DB_NAME..."
mongodump --db $DB_NAME --out $BACKUP_PATH

# Check if backup was successful
if [ $? -eq 0 ]; then
    echo "Backup completed successfully: $BACKUP_PATH"
    
    # Compress the backup
    cd $BACKUP_DIR
    tar -czf "$DB_NAME-$DATE.tar.gz" "$DB_NAME-$DATE"
    rm -rf "$DB_NAME-$DATE"
    echo "Backup compressed: $DB_NAME-$DATE.tar.gz"
    
    # Delete old backups (older than RETENTION_DAYS)
    find $BACKUP_DIR -name "*.tar.gz" -type f -mtime +$RETENTION_DAYS -delete
    echo "Old backups cleaned up (older than $RETENTION_DAYS days)"
    
    # Show current backups
    echo ""
    echo "Current backups:"
    ls -lh $BACKUP_DIR/*.tar.gz 2>/dev/null || echo "No backups found"
else
    echo "Backup failed!"
    exit 1
fi

echo ""
echo "Backup process completed at $(date)"
