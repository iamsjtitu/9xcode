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

BACKUP_ARTICLES = [
    {
        'title': 'Setup Automated MySQL Database Backup',
        'description': 'Create automated MySQL database backups with compression and retention policy.',
        'category': 'backup',
        'os': ['ubuntu', 'centos', 'linux'],
        'difficulty': 'intermediate',
        'tags': ['mysql', 'backup', 'database', 'automation', 'cron'],
        'steps': [
            {'title': 'Create Backup Script', 'description': 'Create MySQL backup shell script.', 'code': 'sudo nano /usr/local/bin/mysql_backup.sh\n\n#!/bin/bash\n\n# Configuration\nBACKUP_DIR="/var/backups/mysql"\nDATE=$(date +%Y-%m-%d_%H-%M)\nRETENTION_DAYS=7\n\n# MySQL credentials\nMYSQL_USER="root"\nMYSQL_PASS="your_password"\n\n# Create backup directory\nmkdir -p $BACKUP_DIR\n\n# Backup all databases\nmysqldump -u$MYSQL_USER -p$MYSQL_PASS --all-databases | gzip > $BACKUP_DIR/all_databases_$DATE.sql.gz\n\n# Delete old backups\nfind $BACKUP_DIR -name "*.sql.gz" -mtime +$RETENTION_DAYS -delete\n\necho "Backup completed: $DATE"', 'language': 'bash'},
            {'title': 'Secure the Script', 'description': 'Set proper permissions.', 'code': '# Make executable\nsudo chmod +x /usr/local/bin/mysql_backup.sh\n\n# Restrict permissions (contains password)\nsudo chmod 700 /usr/local/bin/mysql_backup.sh\n\n# Better: Use .my.cnf for credentials\nsudo nano ~/.my.cnf\n\n[mysqldump]\nuser=root\npassword=your_password\n\n# Secure the file\nchmod 600 ~/.my.cnf', 'language': 'bash'},
            {'title': 'Setup Cron Job', 'description': 'Schedule automatic backups.', 'code': '# Edit crontab\nsudo crontab -e\n\n# Daily backup at 2 AM\n0 2 * * * /usr/local/bin/mysql_backup.sh >> /var/log/mysql_backup.log 2>&1\n\n# Weekly full backup on Sunday at 3 AM\n0 3 * * 0 /usr/local/bin/mysql_backup.sh --full >> /var/log/mysql_backup.log 2>&1\n\n# Verify cron job\nsudo crontab -l', 'language': 'bash'},
            {'title': 'Backup Specific Database', 'description': 'Script for individual database backup.', 'code': '#!/bin/bash\n# Single database backup\n\nDB_NAME="your_database"\nBACKUP_DIR="/var/backups/mysql"\nDATE=$(date +%Y-%m-%d_%H-%M)\n\nmysqldump -u root -p --single-transaction \\\n    --routines --triggers --events \\\n    $DB_NAME | gzip > $BACKUP_DIR/${DB_NAME}_$DATE.sql.gz\n\necho "Backup of $DB_NAME completed"', 'language': 'bash'}
        ],
        'postInstallation': {'title': 'Restore Backup', 'content': 'To restore: gunzip < backup_file.sql.gz | mysql -u root -p database_name. Test your backups regularly. Consider offsite backup to AWS S3 or Google Cloud Storage.'}
    },
    {
        'title': 'Setup Rsync Backup to Remote Server',
        'description': 'Configure rsync for efficient incremental backups to remote server.',
        'category': 'backup',
        'os': ['ubuntu', 'centos', 'linux'],
        'difficulty': 'intermediate',
        'tags': ['rsync', 'backup', 'remote', 'sync', 'linux'],
        'steps': [
            {'title': 'Install Rsync', 'description': 'Ensure rsync is installed.', 'code': '# Ubuntu/Debian\nsudo apt install -y rsync\n\n# CentOS/RHEL\nsudo yum install -y rsync\n\n# Verify installation\nrsync --version', 'language': 'bash'},
            {'title': 'Setup SSH Key Authentication', 'description': 'Enable passwordless SSH.', 'code': '# Generate SSH key (if not exists)\nssh-keygen -t rsa -b 4096\n\n# Copy to remote server\nssh-copy-id user@remote-server-ip\n\n# Test connection\nssh user@remote-server-ip "echo connected"', 'language': 'bash'},
            {'title': 'Basic Rsync Commands', 'description': 'Common rsync operations.', 'code': '# Sync local to remote\nrsync -avz /local/folder/ user@remote:/backup/folder/\n\n# Sync remote to local\nrsync -avz user@remote:/remote/folder/ /local/backup/\n\n# Options explained:\n# -a : Archive mode (preserves permissions, timestamps)\n# -v : Verbose output\n# -z : Compress during transfer\n# --delete : Delete files at destination not in source\n# --progress : Show progress\n# --exclude : Exclude files/folders', 'language': 'bash'},
            {'title': 'Create Backup Script', 'description': 'Automated rsync backup script.', 'code': 'sudo nano /usr/local/bin/rsync_backup.sh\n\n#!/bin/bash\n\nSOURCE="/var/www/"\nDEST="user@backup-server:/backups/webserver/"\nLOG="/var/log/rsync_backup.log"\nDATE=$(date "+%Y-%m-%d %H:%M:%S")\n\necho "[$DATE] Starting backup..." >> $LOG\n\nrsync -avz --delete \\\n    --exclude "*.log" \\\n    --exclude "cache/" \\\n    --exclude "tmp/" \\\n    $SOURCE $DEST >> $LOG 2>&1\n\necho "[$DATE] Backup completed" >> $LOG\n\n# Make executable and add to cron\nchmod +x /usr/local/bin/rsync_backup.sh', 'language': 'bash'}
        ],
        'postInstallation': {'title': 'Cron Schedule', 'content': 'Add to crontab: 0 1 * * * /usr/local/bin/rsync_backup.sh. Use --dry-run to test before actual backup. Consider bandwidth limits with --bwlimit=1000 (KB/s).'}
    },
    {
        'title': 'Backup Server to AWS S3',
        'description': 'Setup automated backups to Amazon S3 using AWS CLI.',
        'category': 'backup',
        'os': ['ubuntu', 'centos', 'linux'],
        'difficulty': 'intermediate',
        'tags': ['aws', 's3', 'backup', 'cloud', 'automation'],
        'steps': [
            {'title': 'Install AWS CLI', 'description': 'Install and configure AWS CLI.', 'code': '# Install AWS CLI v2\ncurl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"\nunzip awscliv2.zip\nsudo ./aws/install\n\n# Verify\naws --version\n\n# Configure credentials\naws configure\n# Enter: Access Key ID\n# Enter: Secret Access Key\n# Region: ap-south-1 (or your region)\n# Output: json', 'language': 'bash'},
            {'title': 'Create S3 Bucket', 'description': 'Create bucket for backups.', 'code': '# Create bucket\naws s3 mb s3://your-backup-bucket-name --region ap-south-1\n\n# List buckets\naws s3 ls\n\n# Enable versioning (recommended)\naws s3api put-bucket-versioning \\\n    --bucket your-backup-bucket-name \\\n    --versioning-configuration Status=Enabled', 'language': 'bash'},
            {'title': 'Create Backup Script', 'description': 'Script to backup to S3.', 'code': 'sudo nano /usr/local/bin/s3_backup.sh\n\n#!/bin/bash\n\nBUCKET="s3://your-backup-bucket-name"\nSERVER_NAME="webserver1"\nDATE=$(date +%Y-%m-%d)\nBACKUP_DIR="/tmp/backup"\n\n# Create backup directory\nmkdir -p $BACKUP_DIR\n\n# Backup important directories\ntar -czf $BACKUP_DIR/www_$DATE.tar.gz /var/www/\ntar -czf $BACKUP_DIR/etc_$DATE.tar.gz /etc/\n\n# MySQL backup\nmysqldump --all-databases | gzip > $BACKUP_DIR/mysql_$DATE.sql.gz\n\n# Upload to S3\naws s3 sync $BACKUP_DIR $BUCKET/$SERVER_NAME/$DATE/\n\n# Cleanup local\nrm -rf $BACKUP_DIR\n\necho "Backup completed: $DATE"', 'language': 'bash'},
            {'title': 'Setup Lifecycle Rules', 'description': 'Auto-delete old backups.', 'code': '# Create lifecycle policy file\ncat > /tmp/lifecycle.json << EOF\n{\n    "Rules": [\n        {\n            "ID": "DeleteOldBackups",\n            "Status": "Enabled",\n            "Filter": {"Prefix": ""},\n            "Expiration": {"Days": 30},\n            "NoncurrentVersionExpiration": {"NoncurrentDays": 7}\n        }\n    ]\n}\nEOF\n\n# Apply lifecycle rule\naws s3api put-bucket-lifecycle-configuration \\\n    --bucket your-backup-bucket-name \\\n    --lifecycle-configuration file:///tmp/lifecycle.json\n\n# Schedule backup\nsudo crontab -e\n0 3 * * * /usr/local/bin/s3_backup.sh >> /var/log/s3_backup.log 2>&1', 'language': 'bash'}
        ],
        'postInstallation': {'title': 'Cost Optimization', 'content': 'Use S3 Intelligent-Tiering for automatic cost savings. Enable S3 Transfer Acceleration for faster uploads. Consider S3 Glacier for long-term archival.'}
    },
    {
        'title': 'Setup BorgBackup Deduplication Backup',
        'description': 'Install and configure BorgBackup for efficient deduplicated backups.',
        'category': 'backup',
        'os': ['ubuntu', 'linux'],
        'difficulty': 'intermediate',
        'tags': ['borgbackup', 'backup', 'deduplication', 'encryption', 'linux'],
        'steps': [
            {'title': 'Install BorgBackup', 'description': 'Install Borg on source and destination.', 'code': '# Ubuntu/Debian\nsudo apt install -y borgbackup\n\n# CentOS/RHEL\nsudo yum install -y epel-release\nsudo yum install -y borgbackup\n\n# Verify\nborg --version', 'language': 'bash'},
            {'title': 'Initialize Backup Repository', 'description': 'Create encrypted backup repository.', 'code': '# Local repository\nborg init --encryption=repokey /backup/borg-repo\n\n# Remote repository (via SSH)\nborg init --encryption=repokey ssh://user@backup-server/path/to/repo\n\n# Save the encryption key!\nborg key export /backup/borg-repo /safe/location/borg-key.txt', 'language': 'bash'},
            {'title': 'Create Backup', 'description': 'Perform backup operation.', 'code': '# Create backup with timestamp\nborg create --stats --progress \\\n    /backup/borg-repo::backup-{now:%Y-%m-%d_%H-%M} \\\n    /var/www \\\n    /etc \\\n    /home \\\n    --exclude "*.log" \\\n    --exclude "*/cache/*" \\\n    --exclude "*/tmp/*"\n\n# List backups\nborg list /backup/borg-repo\n\n# Check repository\nborg check /backup/borg-repo', 'language': 'bash'},
            {'title': 'Automated Backup Script', 'description': 'Create comprehensive backup script.', 'code': 'sudo nano /usr/local/bin/borg_backup.sh\n\n#!/bin/bash\nexport BORG_REPO="/backup/borg-repo"\nexport BORG_PASSPHRASE="your-encryption-passphrase"\n\n# Create backup\nborg create --stats --compression lz4 \\\n    ::backup-{now:%Y-%m-%d_%H-%M} \\\n    /var/www /etc /home\n\n# Prune old backups\n# Keep: 7 daily, 4 weekly, 6 monthly\nborg prune --keep-daily=7 --keep-weekly=4 --keep-monthly=6\n\n# Verify\nborg check\n\necho "Backup completed: $(date)"', 'language': 'bash'}
        ],
        'postInstallation': {'title': 'Restore Backup', 'content': 'List archives: borg list /repo. Extract: borg extract /repo::archive-name. Mount as filesystem: borg mount /repo::archive /mnt/backup. Borg provides ~50-90% space savings through deduplication.'}
    },
    {
        'title': 'Setup Duplicity Encrypted Backup',
        'description': 'Configure Duplicity for encrypted incremental backups to various backends.',
        'category': 'backup',
        'os': ['ubuntu', 'linux'],
        'difficulty': 'intermediate',
        'tags': ['duplicity', 'backup', 'encryption', 'gpg', 'incremental'],
        'steps': [
            {'title': 'Install Duplicity', 'description': 'Install Duplicity and dependencies.', 'code': '# Ubuntu/Debian\nsudo apt install -y duplicity python3-boto3 gnupg\n\n# Verify\nduplicity --version', 'language': 'bash'},
            {'title': 'Generate GPG Key', 'description': 'Create encryption key.', 'code': '# Generate GPG key\ngpg --full-generate-key\n\n# Choose:\n# - RSA and RSA\n# - 4096 bits\n# - 0 = no expiration\n# - Enter name and email\n# - Set passphrase\n\n# List keys\ngpg --list-keys\n\n# Export key ID (for backup script)\nGPG_KEY=$(gpg --list-keys --keyid-format SHORT | grep pub | awk \'{print $2}\' | cut -d\'/\' -f2)', 'language': 'bash'},
            {'title': 'Backup to Local Directory', 'description': 'Basic duplicity backup.', 'code': '# Set passphrase\nexport PASSPHRASE="your-gpg-passphrase"\n\n# Full backup\nduplicity full /var/www file:///backup/duplicity/\n\n# Incremental backup\nduplicity incr /var/www file:///backup/duplicity/\n\n# Automatic (full if needed, else incremental)\nduplicity /var/www file:///backup/duplicity/', 'language': 'bash'},
            {'title': 'Backup to S3', 'description': 'Configure S3 backend.', 'code': '# Set AWS credentials\nexport AWS_ACCESS_KEY_ID="your-key"\nexport AWS_SECRET_ACCESS_KEY="your-secret"\nexport PASSPHRASE="your-gpg-passphrase"\n\n# Backup to S3\nduplicity --full-if-older-than 7D \\\n    /var/www \\\n    s3://s3.amazonaws.com/your-bucket/backup\n\n# Remove old backups (keep 30 days)\nduplicity remove-older-than 30D \\\n    s3://s3.amazonaws.com/your-bucket/backup --force\n\n# List backups\nduplicity collection-status \\\n    s3://s3.amazonaws.com/your-bucket/backup', 'language': 'bash'}
        ],
        'postInstallation': {'title': 'Restore', 'content': 'Restore all: duplicity restore file:///backup/duplicity/ /restore/path. Restore specific file: duplicity --file-to-restore path/file file:///backup/duplicity/ /restore/path. List files: duplicity list-current-files file:///backup/duplicity/.'}
    },
    {
        'title': 'Full Server Backup with Clonezilla',
        'description': 'Create complete server disk image backup using Clonezilla.',
        'category': 'backup',
        'os': ['ubuntu', 'centos', 'linux'],
        'difficulty': 'advanced',
        'tags': ['clonezilla', 'disk-image', 'backup', 'recovery', 'bare-metal'],
        'steps': [
            {'title': 'Download Clonezilla', 'description': 'Get Clonezilla Live ISO.', 'code': 'Download from:\nhttps://clonezilla.org/downloads.php\n\nChoose:\n- Clonezilla Live (stable)\n- AMD64 (for 64-bit systems)\n- ISO file\n\nCreate bootable USB:\n# Linux\nsudo dd if=clonezilla-live.iso of=/dev/sdX bs=4M status=progress\n\n# Windows\nUse Rufus or Etcher', 'language': 'bash'},
            {'title': 'Boot into Clonezilla', 'description': 'Start Clonezilla Live.', 'code': '1. Insert USB and boot from it\n2. Select "Clonezilla live"\n3. Choose language\n4. Choose keymap\n5. Select "Start Clonezilla"\n6. Choose mode:\n   - device-image: Disk to image file\n   - device-device: Disk to disk clone', 'language': 'bash'},
            {'title': 'Create Disk Image', 'description': 'Backup entire disk to image.', 'code': 'For disk to image backup:\n\n1. Choose "device-image"\n2. Select "local_dev" (save to external drive)\n3. Wait for drives to be detected\n4. Select destination drive (external HDD)\n5. Choose directory for image\n6. Select "Beginner" mode\n7. Choose "savedisk" (backup entire disk)\n8. Enter image name (e.g., server-backup-2024)\n9. Select source disk to backup\n10. Choose compression: -z1p (parallel gzip)\n11. Skip checking: -sfsck (faster)\n12. Confirm and start backup', 'language': 'bash'},
            {'title': 'Restore from Image', 'description': 'Restore disk from Clonezilla image.', 'code': 'To restore:\n\n1. Boot Clonezilla Live\n2. Choose "device-image"\n3. Select "local_dev"\n4. Mount drive containing backup image\n5. Select "Beginner" mode\n6. Choose "restoredisk"\n7. Select image to restore\n8. Select target disk\n9. Confirm (WARNING: erases target disk)\n10. Wait for restore to complete\n11. Reboot\n\nRestore time depends on disk size\nand compression level', 'language': 'bash'}
        ],
        'postInstallation': {'title': 'Tips', 'content': 'Schedule regular image backups for critical servers. Store images on separate physical location. Test restore process periodically. Use -q2 priority for faster operation. Consider Clonezilla Server for network-based imaging of multiple machines.'}
    },
    {
        'title': 'MongoDB Backup and Restore',
        'description': 'Backup and restore MongoDB databases using mongodump and mongorestore.',
        'category': 'backup',
        'os': ['ubuntu', 'linux'],
        'difficulty': 'intermediate',
        'tags': ['mongodb', 'backup', 'database', 'restore', 'nosql'],
        'steps': [
            {'title': 'Basic mongodump', 'description': 'Backup MongoDB databases.', 'code': '# Backup all databases\nmongodump --out /backup/mongodb/\n\n# Backup specific database\nmongodump --db mydb --out /backup/mongodb/\n\n# Backup specific collection\nmongodump --db mydb --collection users --out /backup/mongodb/\n\n# With authentication\nmongodump --uri="mongodb://user:pass@localhost:27017" --out /backup/mongodb/\n\n# Compressed backup\nmongodump --gzip --out /backup/mongodb/', 'language': 'bash'},
            {'title': 'Automated Backup Script', 'description': 'Create scheduled backup script.', 'code': 'sudo nano /usr/local/bin/mongodb_backup.sh\n\n#!/bin/bash\n\nBACKUP_DIR="/backup/mongodb"\nDATE=$(date +%Y-%m-%d_%H-%M)\nRETENTION=7\n\n# Create dated directory\nmkdir -p $BACKUP_DIR/$DATE\n\n# Backup with compression\nmongodump --gzip --out $BACKUP_DIR/$DATE\n\n# Create tar archive\ncd $BACKUP_DIR\ntar -czf mongodb_$DATE.tar.gz $DATE\nrm -rf $DATE\n\n# Delete old backups\nfind $BACKUP_DIR -name "*.tar.gz" -mtime +$RETENTION -delete\n\necho "MongoDB backup completed: $DATE"', 'language': 'bash'},
            {'title': 'Restore from Backup', 'description': 'Restore MongoDB from backup.', 'code': '# Restore all databases\nmongorestore /backup/mongodb/\n\n# Restore specific database\nmongorestore --db mydb /backup/mongodb/mydb/\n\n# Restore and drop existing\nmongorestore --drop /backup/mongodb/\n\n# Restore from compressed backup\nmongorestore --gzip /backup/mongodb/\n\n# Restore from archive\ntar -xzf mongodb_2024-01-15.tar.gz\nmongorestore --gzip 2024-01-15/', 'language': 'bash'},
            {'title': 'Point-in-Time Recovery', 'description': 'Enable oplog for point-in-time recovery.', 'code': '# Backup with oplog (for replica sets)\nmongodump --oplog --out /backup/mongodb/\n\n# Restore with oplog replay\nmongorestore --oplogReplay /backup/mongodb/\n\n# For standalone: Enable replica set first\n# Edit mongod.conf:\nreplication:\n  replSetName: "rs0"\n\n# Initialize replica set\nmongo --eval "rs.initiate()"\n\n# Now oplog is available for PITR', 'language': 'bash'}
        ],
        'postInstallation': {'title': 'Best Practices', 'content': 'Use --oplog for consistent backups of replica sets. Test restores regularly. Store backups offsite (S3, remote server). Monitor backup job success. Consider MongoDB Atlas for managed backups.'}
    },
    {
        'title': 'PostgreSQL Backup and Restore',
        'description': 'Backup and restore PostgreSQL databases using pg_dump and pg_restore.',
        'category': 'backup',
        'os': ['ubuntu', 'linux'],
        'difficulty': 'intermediate',
        'tags': ['postgresql', 'backup', 'database', 'restore', 'pg_dump'],
        'steps': [
            {'title': 'Single Database Backup', 'description': 'Backup individual PostgreSQL database.', 'code': '# Plain SQL backup\npg_dump -U postgres mydb > mydb_backup.sql\n\n# Custom format (recommended - compressed)\npg_dump -U postgres -Fc mydb > mydb_backup.dump\n\n# Directory format (parallel backup)\npg_dump -U postgres -Fd -j 4 mydb -f /backup/mydb_dir/\n\n# With specific tables\npg_dump -U postgres -t users -t orders mydb > tables_backup.sql\n\n# Exclude tables\npg_dump -U postgres --exclude-table=logs mydb > mydb_no_logs.sql', 'language': 'bash'},
            {'title': 'Full Server Backup', 'description': 'Backup all databases.', 'code': '# Backup all databases\npg_dumpall -U postgres > all_databases.sql\n\n# Backup only globals (roles, tablespaces)\npg_dumpall -U postgres --globals-only > globals.sql\n\n# Backup only schemas (no data)\npg_dumpall -U postgres --schema-only > schemas.sql\n\n# Compressed full backup\npg_dumpall -U postgres | gzip > all_databases.sql.gz', 'language': 'bash'},
            {'title': 'Automated Backup Script', 'description': 'Daily backup script with rotation.', 'code': 'sudo nano /usr/local/bin/pg_backup.sh\n\n#!/bin/bash\n\nexport PGPASSWORD="postgres_password"\nBACKUP_DIR="/backup/postgresql"\nDATE=$(date +%Y-%m-%d)\nRETENTION=7\n\nmkdir -p $BACKUP_DIR\n\n# Backup each database\nfor DB in $(psql -U postgres -t -c "SELECT datname FROM pg_database WHERE datistemplate = false;"); do\n    pg_dump -U postgres -Fc $DB > $BACKUP_DIR/${DB}_${DATE}.dump\ndone\n\n# Backup globals\npg_dumpall -U postgres --globals-only > $BACKUP_DIR/globals_${DATE}.sql\n\n# Delete old backups\nfind $BACKUP_DIR -name "*.dump" -mtime +$RETENTION -delete\nfind $BACKUP_DIR -name "*.sql" -mtime +$RETENTION -delete\n\necho "PostgreSQL backup completed: $DATE"', 'language': 'bash'},
            {'title': 'Restore Database', 'description': 'Restore from backup files.', 'code': '# Restore from SQL file\npsql -U postgres mydb < mydb_backup.sql\n\n# Restore from custom format\npg_restore -U postgres -d mydb mydb_backup.dump\n\n# Create database and restore\ncreatedb -U postgres mydb_restored\npg_restore -U postgres -d mydb_restored mydb_backup.dump\n\n# Restore with clean (drop existing)\npg_restore -U postgres -c -d mydb mydb_backup.dump\n\n# Parallel restore (directory format)\npg_restore -U postgres -j 4 -d mydb /backup/mydb_dir/', 'language': 'bash'}
        ],
        'postInstallation': {'title': 'WAL Archiving', 'content': 'For point-in-time recovery, enable WAL archiving in postgresql.conf: archive_mode = on, archive_command = "cp %p /backup/wal/%f". Use pg_basebackup for physical backups. Consider pgBackRest for enterprise-grade backups.'}
    }
]

async def seed_backup():
    print("=" * 60)
    print("  SEEDING: Backup Articles")
    print("=" * 60)
    
    added = 0
    for article in BACKUP_ARTICLES:
        article['id'] = str(uuid.uuid4())
        article['slug'] = create_slug(article['title'])
        article['author'] = 'Admin'
        article['createdAt'] = datetime.utcnow()
        article['updatedAt'] = datetime.utcnow()
        article['views'] = 1000 + (hash(article['title']) % 5000)
        article['likes'] = 50 + (hash(article['title']) % 200)
        
        existing = await db.code_snippets.find_one({'slug': article['slug']})
        if not existing:
            await db.code_snippets.insert_one(article)
            print(f"✓ Added: {article['title'][:50]}...")
            added += 1
        else:
            print(f"- Skipped: {article['title'][:50]}...")
    
    print(f"\n✓ Added {added} Backup articles")
    total = await db.code_snippets.count_documents({'category': 'backup'})
    print(f"Total Backup articles: {total}")

if __name__ == "__main__":
    asyncio.run(seed_backup())
