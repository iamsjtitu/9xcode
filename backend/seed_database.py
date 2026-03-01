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

DATABASE_ARTICLES = [
    {
        'title': 'Install MySQL 8 on Ubuntu 22.04',
        'description': 'Complete guide to install and secure MySQL 8 database server on Ubuntu.',
        'category': 'database',
        'os': ['ubuntu', 'linux'],
        'difficulty': 'beginner',
        'tags': ['mysql', 'database', 'ubuntu', 'installation'],
        'steps': [
            {'title': 'Install MySQL Server', 'description': 'Install MySQL from Ubuntu repositories.', 'code': 'sudo apt update\nsudo apt install -y mysql-server\n\n# Check version\nmysql --version\n\n# Check service status\nsudo systemctl status mysql', 'language': 'bash'},
            {'title': 'Secure MySQL Installation', 'description': 'Run security script.', 'code': 'sudo mysql_secure_installation\n\n# Answer prompts:\n# - VALIDATE PASSWORD component: y (recommended)\n# - Password strength: 2 (STRONG)\n# - Set root password: Enter strong password\n# - Remove anonymous users: y\n# - Disallow root login remotely: y\n# - Remove test database: y\n# - Reload privileges: y', 'language': 'bash'},
            {'title': 'Access MySQL', 'description': 'Login to MySQL server.', 'code': '# Login as root\nsudo mysql\n\n# Or with password\nmysql -u root -p\n\n# Show databases\nSHOW DATABASES;\n\n# Exit\nEXIT;', 'language': 'bash'},
            {'title': 'Create Database and User', 'description': 'Setup new database and user.', 'code': '-- Create database\nCREATE DATABASE myapp;\n\n-- Create user\nCREATE USER \'myuser\'@\'localhost\' IDENTIFIED BY \'StrongPassword123!\';\n\n-- Grant privileges\nGRANT ALL PRIVILEGES ON myapp.* TO \'myuser\'@\'localhost\';\n\n-- Apply changes\nFLUSH PRIVILEGES;\n\n-- Verify\nSHOW GRANTS FOR \'myuser\'@\'localhost\';', 'language': 'sql'}
        ],
        'postInstallation': {'title': 'Configuration', 'content': 'Config file: /etc/mysql/mysql.conf.d/mysqld.cnf. For remote access, change bind-address from 127.0.0.1 to 0.0.0.0 (not recommended for production). Use MySQL Workbench for GUI management.'}
    },
    {
        'title': 'Install PostgreSQL on Ubuntu',
        'description': 'Install and configure PostgreSQL database server on Ubuntu Linux.',
        'category': 'database',
        'os': ['ubuntu', 'linux'],
        'difficulty': 'beginner',
        'tags': ['postgresql', 'postgres', 'database', 'ubuntu'],
        'steps': [
            {'title': 'Install PostgreSQL', 'description': 'Install from official repository.', 'code': '# Add PostgreSQL repository\nsudo sh -c \'echo "deb http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list\'\nwget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -\n\n# Install\nsudo apt update\nsudo apt install -y postgresql postgresql-contrib\n\n# Check version\npsql --version', 'language': 'bash'},
            {'title': 'Access PostgreSQL', 'description': 'Connect to PostgreSQL.', 'code': '# Switch to postgres user\nsudo -i -u postgres\n\n# Open PostgreSQL prompt\npsql\n\n# Check connection info\n\\conninfo\n\n# List databases\n\\l\n\n# Exit\n\\q\nexit', 'language': 'bash'},
            {'title': 'Create Database and User', 'description': 'Setup new database and user.', 'code': '# As postgres user\nsudo -u postgres psql\n\n-- Create user\nCREATE USER myuser WITH PASSWORD \'StrongPassword123!\';\n\n-- Create database\nCREATE DATABASE myapp OWNER myuser;\n\n-- Grant privileges\nGRANT ALL PRIVILEGES ON DATABASE myapp TO myuser;\n\n-- List users\n\\du\n\n-- List databases\n\\l', 'language': 'sql'},
            {'title': 'Configure Remote Access', 'description': 'Allow remote connections.', 'code': '# Edit postgresql.conf\nsudo nano /etc/postgresql/15/main/postgresql.conf\n\n# Change:\nlisten_addresses = \'*\'\n\n# Edit pg_hba.conf\nsudo nano /etc/postgresql/15/main/pg_hba.conf\n\n# Add line for remote access:\nhost    all    all    0.0.0.0/0    md5\n\n# Restart PostgreSQL\nsudo systemctl restart postgresql\n\n# Allow firewall\nsudo ufw allow 5432/tcp', 'language': 'bash'}
        ],
        'postInstallation': {'title': 'Tools', 'content': 'Use pgAdmin for GUI management. Data directory: /var/lib/postgresql/15/main/. Config files in /etc/postgresql/15/main/. Connect: psql -h localhost -U myuser -d myapp'}
    },
    {
        'title': 'Install MongoDB on Ubuntu',
        'description': 'Install MongoDB Community Edition on Ubuntu Linux.',
        'category': 'database',
        'os': ['ubuntu', 'linux'],
        'difficulty': 'beginner',
        'tags': ['mongodb', 'nosql', 'database', 'ubuntu'],
        'steps': [
            {'title': 'Add MongoDB Repository', 'description': 'Add official MongoDB repository.', 'code': '# Import GPG key\ncurl -fsSL https://www.mongodb.org/static/pgp/server-7.0.asc | \\\n   sudo gpg -o /usr/share/keyrings/mongodb-server-7.0.gpg --dearmor\n\n# Add repository\necho "deb [ arch=amd64,arm64 signed-by=/usr/share/keyrings/mongodb-server-7.0.gpg ] https://repo.mongodb.org/apt/ubuntu jammy/mongodb-org/7.0 multiverse" | \\\n   sudo tee /etc/apt/sources.list.d/mongodb-org-7.0.list', 'language': 'bash'},
            {'title': 'Install MongoDB', 'description': 'Install MongoDB packages.', 'code': '# Update and install\nsudo apt update\nsudo apt install -y mongodb-org\n\n# Start MongoDB\nsudo systemctl start mongod\nsudo systemctl enable mongod\n\n# Check status\nsudo systemctl status mongod\n\n# Verify installation\nmongod --version', 'language': 'bash'},
            {'title': 'Access MongoDB Shell', 'description': 'Connect to MongoDB.', 'code': '# Open MongoDB shell\nmongosh\n\n# Show databases\nshow dbs\n\n# Use/create database\nuse myapp\n\n# Insert document\ndb.users.insertOne({name: "John", email: "john@example.com"})\n\n# Find documents\ndb.users.find()\n\n# Exit\nexit', 'language': 'bash'},
            {'title': 'Enable Authentication', 'description': 'Secure MongoDB with authentication.', 'code': '# Connect to MongoDB\nmongosh\n\n# Switch to admin database\nuse admin\n\n# Create admin user\ndb.createUser({\n  user: "admin",\n  pwd: "StrongPassword123!",\n  roles: ["root"]\n})\n\n# Exit and edit config\nexit\nsudo nano /etc/mongod.conf\n\n# Add security section:\nsecurity:\n  authorization: enabled\n\n# Restart MongoDB\nsudo systemctl restart mongod\n\n# Connect with auth\nmongosh -u admin -p --authenticationDatabase admin', 'language': 'bash'}
        ],
        'postInstallation': {'title': 'Management', 'content': 'Config file: /etc/mongod.conf. Data directory: /var/lib/mongodb. Use MongoDB Compass for GUI. For remote access, change bindIp from 127.0.0.1 to 0.0.0.0 in config.'}
    },
    {
        'title': 'Install Redis on Ubuntu',
        'description': 'Install and configure Redis in-memory database on Ubuntu.',
        'category': 'database',
        'os': ['ubuntu', 'linux'],
        'difficulty': 'beginner',
        'tags': ['redis', 'cache', 'database', 'ubuntu', 'in-memory'],
        'steps': [
            {'title': 'Install Redis', 'description': 'Install Redis from repositories.', 'code': '# Add Redis repository\ncurl -fsSL https://packages.redis.io/gpg | sudo gpg --dearmor -o /usr/share/keyrings/redis-archive-keyring.gpg\necho "deb [signed-by=/usr/share/keyrings/redis-archive-keyring.gpg] https://packages.redis.io/deb $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/redis.list\n\n# Install\nsudo apt update\nsudo apt install -y redis\n\n# Start Redis\nsudo systemctl start redis-server\nsudo systemctl enable redis-server', 'language': 'bash'},
            {'title': 'Test Redis', 'description': 'Verify Redis installation.', 'code': '# Check status\nsudo systemctl status redis-server\n\n# Connect to Redis CLI\nredis-cli\n\n# Test ping\nPING\n# Response: PONG\n\n# Set and get value\nSET mykey "Hello Redis"\nGET mykey\n\n# Exit\nEXIT', 'language': 'bash'},
            {'title': 'Configure Redis', 'description': 'Edit Redis configuration.', 'code': 'sudo nano /etc/redis/redis.conf\n\n# Key settings:\n\n# Memory limit\nmaxmemory 256mb\nmaxmemory-policy allkeys-lru\n\n# Password (uncomment and set)\nrequirepass YourStrongPassword\n\n# Persistence\nappenonly yes\nappendfsync everysec\n\n# Bind address (for remote access)\nbind 0.0.0.0\n\n# Restart Redis\nsudo systemctl restart redis-server', 'language': 'bash'},
            {'title': 'Basic Redis Operations', 'description': 'Common Redis commands.', 'code': '# Connect with password\nredis-cli -a YourStrongPassword\n\n# String operations\nSET user:1:name "John"\nGET user:1:name\nEXPIRE user:1:name 3600  # Expire in 1 hour\nTTL user:1:name\n\n# List operations\nLPUSH mylist "item1"\nRPUSH mylist "item2"\nLRANGE mylist 0 -1\n\n# Hash operations\nHSET user:1 name "John" email "john@example.com"\nHGETALL user:1\n\n# Info\nINFO\nDBSIZE', 'language': 'bash'}
        ],
        'postInstallation': {'title': 'Use Cases', 'content': 'Redis is ideal for caching, session storage, rate limiting, queues, and real-time analytics. Config file: /etc/redis/redis.conf. Default port: 6379. Use RedisInsight for GUI management.'}
    },
    {
        'title': 'MySQL Performance Tuning',
        'description': 'Optimize MySQL database performance with key configuration settings.',
        'category': 'database',
        'os': ['ubuntu', 'centos', 'linux'],
        'difficulty': 'advanced',
        'tags': ['mysql', 'performance', 'tuning', 'optimization'],
        'steps': [
            {'title': 'Check Current Settings', 'description': 'View current MySQL configuration.', 'code': '# Connect to MySQL\nmysql -u root -p\n\n# Show variables\nSHOW VARIABLES LIKE \'innodb_buffer_pool_size\';\nSHOW VARIABLES LIKE \'max_connections\';\nSHOW VARIABLES LIKE \'query_cache%\';\n\n# Show status\nSHOW GLOBAL STATUS LIKE \'Threads%\';\nSHOW GLOBAL STATUS LIKE \'Innodb_buffer_pool%\';\n\n# Show process list\nSHOW PROCESSLIST;', 'language': 'sql'},
            {'title': 'InnoDB Buffer Pool', 'description': 'Configure buffer pool size.', 'code': '# Edit MySQL config\nsudo nano /etc/mysql/mysql.conf.d/mysqld.cnf\n\n# InnoDB Buffer Pool (50-70% of RAM)\n# For 8GB RAM server:\ninnodb_buffer_pool_size = 5G\ninnodb_buffer_pool_instances = 5\n\n# For 16GB RAM server:\ninnodb_buffer_pool_size = 10G\ninnodb_buffer_pool_instances = 10\n\n# Buffer pool should fit hot data\n# Check usage:\nSHOW GLOBAL STATUS LIKE \'Innodb_buffer_pool_pages%\';', 'language': 'bash'},
            {'title': 'Connection Settings', 'description': 'Optimize connection handling.', 'code': '# In mysqld.cnf:\n\n# Max connections (default 151)\nmax_connections = 500\n\n# Connection timeout\nwait_timeout = 600\ninteractive_timeout = 600\n\n# Thread cache\nthread_cache_size = 128\n\n# Connection limits per user\nmax_user_connections = 50\n\n# Check current connections:\nSHOW STATUS LIKE \'Threads_connected\';\nSHOW STATUS LIKE \'Max_used_connections\';', 'language': 'bash'},
            {'title': 'Query Optimization', 'description': 'Settings for better query performance.', 'code': '# In mysqld.cnf:\n\n# Temporary tables\ntmp_table_size = 256M\nmax_heap_table_size = 256M\n\n# Sort buffer\nsort_buffer_size = 4M\nread_buffer_size = 2M\nread_rnd_buffer_size = 8M\n\n# Join buffer\njoin_buffer_size = 4M\n\n# InnoDB settings\ninnodb_log_file_size = 256M\ninnodb_log_buffer_size = 16M\ninnodb_flush_log_at_trx_commit = 2\ninnodb_flush_method = O_DIRECT\n\n# Apply changes\nsudo systemctl restart mysql', 'language': 'bash'}
        ],
        'postInstallation': {'title': 'Monitoring', 'content': 'Use MySQLTuner: mysqltuner --host localhost --user root. Monitor with: SHOW ENGINE INNODB STATUS. Enable slow query log for optimization. Consider using Percona Monitoring and Management (PMM).'}
    },
    {
        'title': 'Database Migration MySQL to PostgreSQL',
        'description': 'Migrate database from MySQL to PostgreSQL using pgloader.',
        'category': 'database',
        'os': ['ubuntu', 'linux'],
        'difficulty': 'advanced',
        'tags': ['mysql', 'postgresql', 'migration', 'pgloader'],
        'steps': [
            {'title': 'Install pgloader', 'description': 'Install migration tool.', 'code': '# Ubuntu/Debian\nsudo apt update\nsudo apt install -y pgloader\n\n# Verify installation\npgloader --version', 'language': 'bash'},
            {'title': 'Prepare Databases', 'description': 'Setup source and target databases.', 'code': '# On MySQL - grant read access\nmysql -u root -p\nGRANT SELECT, LOCK TABLES ON mydb.* TO \'migration_user\'@\'localhost\' IDENTIFIED BY \'password\';\nFLUSH PRIVILEGES;\n\n# On PostgreSQL - create target database\nsudo -u postgres psql\nCREATE DATABASE mydb_new;\nCREATE USER migration_user WITH PASSWORD \'password\';\nGRANT ALL PRIVILEGES ON DATABASE mydb_new TO migration_user;', 'language': 'bash'},
            {'title': 'Create Migration Script', 'description': 'Configure pgloader migration.', 'code': 'nano migrate.load\n\nLOAD DATABASE\n    FROM mysql://migration_user:password@localhost/mydb\n    INTO postgresql://migration_user:password@localhost/mydb_new\n\nWITH include drop, create tables, create indexes, reset sequences,\n     workers = 4, concurrency = 2\n\nSET maintenance_work_mem to \'512MB\',\n    work_mem to \'48MB\'\n\nCAST type datetime to timestamptz drop default drop not null,\n     type date to date drop default drop not null,\n     type tinyint to smallint,\n     type mediumint to integer,\n     type bigint to bigint,\n     type double to double precision\n\nALTER SCHEMA \'mydb\' RENAME TO \'public\';', 'language': 'bash'},
            {'title': 'Run Migration', 'description': 'Execute the migration.', 'code': '# Run pgloader\npgloader migrate.load\n\n# Or one-liner for simple migration\npgloader mysql://user:pass@localhost/mydb postgresql://user:pass@localhost/mydb_new\n\n# Verify migration\npsql -U migration_user -d mydb_new\n\\dt  # List tables\nSELECT COUNT(*) FROM tablename;', 'language': 'bash'}
        ],
        'postInstallation': {'title': 'Post-Migration', 'content': 'Verify row counts match. Update application connection strings. Test all queries (SQL syntax differences). Run ANALYZE on PostgreSQL tables. Check sequences are set correctly.'}
    },
    {
        'title': 'Setup MySQL Replication Master-Slave',
        'description': 'Configure MySQL master-slave replication for high availability.',
        'category': 'database',
        'os': ['ubuntu', 'centos', 'linux'],
        'difficulty': 'advanced',
        'tags': ['mysql', 'replication', 'master-slave', 'high-availability'],
        'steps': [
            {'title': 'Configure Master Server', 'description': 'Setup master MySQL server.', 'code': '# Edit MySQL config on MASTER\nsudo nano /etc/mysql/mysql.conf.d/mysqld.cnf\n\n# Add under [mysqld]:\nserver-id = 1\nlog_bin = /var/log/mysql/mysql-bin.log\nbinlog_do_db = mydb\nbind-address = 0.0.0.0\n\n# Restart MySQL\nsudo systemctl restart mysql\n\n# Create replication user\nmysql -u root -p\nCREATE USER \'repl_user\'@\'%\' IDENTIFIED BY \'ReplicationPassword123!\';\nGRANT REPLICATION SLAVE ON *.* TO \'repl_user\'@\'%\';\nFLUSH PRIVILEGES;', 'language': 'bash'},
            {'title': 'Get Master Status', 'description': 'Record master binary log position.', 'code': '# On MASTER\nmysql -u root -p\n\n-- Lock tables\nFLUSH TABLES WITH READ LOCK;\n\n-- Get position (note File and Position)\nSHOW MASTER STATUS;\n+------------------+----------+--------------+------------------+\n| File             | Position | Binlog_Do_DB | Binlog_Ignore_DB |\n+------------------+----------+--------------+------------------+\n| mysql-bin.000001 |      154 | mydb         |                  |\n+------------------+----------+--------------+------------------+\n\n-- Export database (in another terminal)\nmysqldump -u root -p --opt mydb > mydb_dump.sql\n\n-- Unlock tables\nUNLOCK TABLES;', 'language': 'sql'},
            {'title': 'Configure Slave Server', 'description': 'Setup slave MySQL server.', 'code': '# Edit MySQL config on SLAVE\nsudo nano /etc/mysql/mysql.conf.d/mysqld.cnf\n\n# Add under [mysqld]:\nserver-id = 2\nrelay_log = /var/log/mysql/mysql-relay-bin.log\nlog_bin = /var/log/mysql/mysql-bin.log\nbinlog_do_db = mydb\n\n# Restart MySQL\nsudo systemctl restart mysql\n\n# Import database\nmysql -u root -p mydb < mydb_dump.sql', 'language': 'bash'},
            {'title': 'Start Replication', 'description': 'Connect slave to master.', 'code': '# On SLAVE\nmysql -u root -p\n\n-- Configure master connection (use values from SHOW MASTER STATUS)\nCHANGE MASTER TO\n    MASTER_HOST=\'master-server-ip\',\n    MASTER_USER=\'repl_user\',\n    MASTER_PASSWORD=\'ReplicationPassword123!\',\n    MASTER_LOG_FILE=\'mysql-bin.000001\',\n    MASTER_LOG_POS=154;\n\n-- Start replication\nSTART SLAVE;\n\n-- Check status\nSHOW SLAVE STATUS\\G\n\n-- Look for:\n-- Slave_IO_Running: Yes\n-- Slave_SQL_Running: Yes', 'language': 'sql'}
        ],
        'postInstallation': {'title': 'Monitoring', 'content': 'Monitor replication lag: SHOW SLAVE STATUS (Seconds_Behind_Master). Setup alerts for replication failures. Consider using MySQL Group Replication for automatic failover.'}
    },
    {
        'title': 'Install MariaDB on CentOS/RHEL',
        'description': 'Install and configure MariaDB database server on CentOS or RHEL.',
        'category': 'database',
        'os': ['centos', 'rhel', 'linux'],
        'difficulty': 'beginner',
        'tags': ['mariadb', 'database', 'centos', 'rhel'],
        'steps': [
            {'title': 'Add MariaDB Repository', 'description': 'Add official MariaDB repository.', 'code': '# Create repo file\nsudo nano /etc/yum.repos.d/MariaDB.repo\n\n[mariadb]\nname = MariaDB\nbaseurl = https://mirrors.gigenet.com/mariadb/yum/11.2/centos/$releasever/$basearch\ngpgkey = https://mirrors.gigenet.com/mariadb/yum/RPM-GPG-KEY-MariaDB\ngpgcheck = 1\nenabled = 1', 'language': 'bash'},
            {'title': 'Install MariaDB', 'description': 'Install MariaDB packages.', 'code': '# Install\nsudo yum install -y MariaDB-server MariaDB-client\n\n# Or on RHEL 8+/CentOS 8+\nsudo dnf install -y MariaDB-server MariaDB-client\n\n# Start and enable\nsudo systemctl start mariadb\nsudo systemctl enable mariadb\n\n# Check status\nsudo systemctl status mariadb', 'language': 'bash'},
            {'title': 'Secure Installation', 'description': 'Run security script.', 'code': 'sudo mysql_secure_installation\n\n# Prompts:\n# Enter current password for root: (press Enter, empty)\n# Switch to unix_socket authentication: n\n# Set root password: Y (enter strong password)\n# Remove anonymous users: Y\n# Disallow root login remotely: Y\n# Remove test database: Y\n# Reload privilege tables: Y', 'language': 'bash'},
            {'title': 'Create Database and User', 'description': 'Setup new database.', 'code': '# Login to MariaDB\nmysql -u root -p\n\n-- Create database\nCREATE DATABASE myapp CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;\n\n-- Create user\nCREATE USER \'myuser\'@\'localhost\' IDENTIFIED BY \'StrongPassword123!\';\n\n-- Grant privileges\nGRANT ALL PRIVILEGES ON myapp.* TO \'myuser\'@\'localhost\';\nFLUSH PRIVILEGES;\n\n-- Verify\nSHOW DATABASES;\nSELECT User, Host FROM mysql.user;', 'language': 'sql'}
        ],
        'postInstallation': {'title': 'Configuration', 'content': 'Config file: /etc/my.cnf.d/server.cnf. MariaDB is a drop-in replacement for MySQL. Use HeidiSQL or DBeaver for GUI management.'}
    }
]

async def seed_database():
    print("=" * 60)
    print("  SEEDING: Database Articles")
    print("=" * 60)
    
    added = 0
    for article in DATABASE_ARTICLES:
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
    
    print(f"\n✓ Added {added} Database articles")
    total = await db.code_snippets.count_documents({'category': 'database'})
    print(f"Total Database articles: {total}")

if __name__ == "__main__":
    asyncio.run(seed_database())
