# MySQL Database Deployment Guide
## Butterfly Identification App

---

## 📋 Table of Contents
1. [Prerequisites](#prerequisites)
2. [Server Setup](#server-setup)
3. [Database Installation](#database-installation)
4. [Database Setup](#database-setup)
5. [Security Configuration](#security-configuration)
6. [Application Configuration](#application-configuration)
7. [Backup and Maintenance](#backup-and-maintenance)
8. [Troubleshooting](#troubleshooting)

---

## 🔧 Prerequisites

### Server Requirements
- **OS**: Ubuntu 20.04+ / CentOS 7+ / Debian 10+
- **RAM**: Minimum 2GB (4GB+ recommended)
- **Storage**: Minimum 10GB free space
- **MySQL/MariaDB**: Version 5.7+ / 10.3+

### Network Requirements
- Open port **3306** for MySQL connections
- Firewall configured to allow connections from application server

---

## 🖥️ Server Setup

### Option 1: Ubuntu/Debian

```bash
# Update system packages
sudo apt-get update
sudo apt-get upgrade -y

# Install MySQL Server 8.0
sudo apt-get install -y mysql-server

# Start MySQL service
sudo systemctl start mysql
sudo systemctl enable mysql

# Check status
sudo systemctl status mysql
```

### Option 2: CentOS/RHEL

```bash
# Update system packages
sudo yum update -y

# Install MySQL Repository
sudo yum install -y https://dev.mysql.com/get/mysql80-community-release-el7-3.noarch.rpm

# Install MySQL Server
sudo yum install -y mysql-community-server

# Start MySQL service
sudo systemctl start mysqld
sudo systemctl enable mysqld

# Get temporary root password
sudo grep 'temporary password' /var/log/mysqld.log
```

### Option 3: Using MariaDB (Alternative)

```bash
# Ubuntu/Debian
sudo apt-get install -y mariadb-server mariadb-client

# CentOS/RHEL
sudo yum install -y mariadb-server mariadb

# Start service
sudo systemctl start mariadb
sudo systemctl enable mariadb
```

---

## 🔐 Initial MySQL Security

### Secure MySQL Installation

```bash
sudo mysql_secure_installation
```

**Follow the prompts:**
- Set root password
- Remove anonymous users: **Yes**
- Disallow root login remotely: **Yes** (recommended)
- Remove test database: **Yes**
- Reload privilege tables: **Yes**

### Configure MySQL for Remote Access

Edit MySQL configuration file:

```bash
# Ubuntu/Debian
sudo nano /etc/mysql/mysql.conf.d/mysqld.cnf

# CentOS/RHEL
sudo nano /etc/my.cnf
```

**Change bind-address:**
```ini
# Change from:
bind-address = 127.0.0.1

# To (allow all connections):
bind-address = 0.0.0.0

# Or specify application server IP:
bind-address = 192.168.1.100
```

**Restart MySQL:**
```bash
sudo systemctl restart mysql
```

---

## 🗄️ Database Setup

### Step 1: Connect to MySQL

```bash
mysql -u root -p
```

### Step 2: Run Setup Scripts

Execute the provided SQL scripts in order:

#### 1. Create Schema and Tables

```bash
mysql -u root -p < 01_schema.sql
```

Or manually:
```sql
source /path/to/database/01_schema.sql;
```

#### 2. Insert Seed Data (30 Butterflies)

```bash
mysql -u root -p butterfly_app < 02_seed_data.sql
```

#### 3. Create Application User

```bash
mysql -u root -p < 03_user_and_permissions.sql
```

**Important:** Edit this file first to change default passwords!

### Step 3: Verify Installation

```bash
mysql -u root -p butterfly_app -e "SELECT COUNT(*) as butterfly_count FROM butterflies;"
mysql -u root -p butterfly_app -e "SHOW TABLES;"
```

Expected output:
```
+-----------------+
| butterfly_count |
+-----------------+
|              30 |
+-----------------+

+-------------------------+
| Tables_in_butterfly_app |
+-------------------------+
| butterflies             |
| scores                  |
+-------------------------+
```

---

## 🔒 Security Configuration

### 1. Create Dedicated Database User

**For Production**, edit `03_user_and_permissions.sql` and update:

```sql
-- Change default credentials
CREATE USER IF NOT EXISTS 'butterfly_user'@'%' 
    IDENTIFIED BY 'YOUR_STRONG_PASSWORD_HERE';

-- For specific application server IP (more secure)
CREATE USER IF NOT EXISTS 'butterfly_user'@'192.168.1.100' 
    IDENTIFIED BY 'YOUR_STRONG_PASSWORD_HERE';

GRANT ALL PRIVILEGES ON butterfly_app.* TO 'butterfly_user'@'%';
FLUSH PRIVILEGES;
```

### 2. Configure Firewall

**Ubuntu/Debian (UFW):**
```bash
# Allow MySQL from specific IP
sudo ufw allow from 192.168.1.100 to any port 3306

# Or allow from subnet
sudo ufw allow from 192.168.1.0/24 to any port 3306

# Enable firewall
sudo ufw enable
```

**CentOS/RHEL (firewalld):**
```bash
# Allow MySQL service
sudo firewall-cmd --permanent --add-service=mysql

# Or specific IP
sudo firewall-cmd --permanent --add-rich-rule='rule family="ipv4" source address="192.168.1.100/32" port protocol="tcp" port="3306" accept'

# Reload firewall
sudo firewall-cmd --reload
```

### 3. SSL/TLS Configuration (Recommended)

```bash
# Generate SSL certificates
sudo mysql_ssl_rsa_setup

# Verify SSL is enabled
mysql -u root -p -e "SHOW VARIABLES LIKE '%ssl%';"
```

---

## ⚙️ Application Configuration

### Update Backend .env File

On your **application server**, update `/app/backend/.env`:

```bash
# Remote MySQL Server Configuration
MYSQL_HOST="192.168.1.50"          # Database server IP
MYSQL_USER="butterfly_user"         # Database username
MYSQL_PASSWORD="your_password"      # Database password
MYSQL_DATABASE="butterfly_app"      # Database name
MYSQL_PORT="3306"                   # MySQL port (default: 3306)

# Optional: SSL Configuration
MYSQL_SSL_CA="/path/to/ca-cert.pem"
MYSQL_SSL_CERT="/path/to/client-cert.pem"
MYSQL_SSL_KEY="/path/to/client-key.pem"
```

### Test Connection from Application Server

```bash
# Install MySQL client on application server
sudo apt-get install mysql-client  # Ubuntu/Debian
sudo yum install mysql             # CentOS/RHEL

# Test connection
mysql -h 192.168.1.50 -u butterfly_user -p butterfly_app
```

### Update Python Code (if needed)

The connection pool in `server.py` already supports environment variables:

```python
db_pool = await aiomysql.create_pool(
    host=os.environ.get('MYSQL_HOST', 'localhost'),
    port=int(os.environ.get('MYSQL_PORT', 3306)),
    user=os.environ.get('MYSQL_USER', 'root'),
    password=os.environ.get('MYSQL_PASSWORD', 'root'),
    db=os.environ.get('MYSQL_DATABASE', 'testdata'),
    charset='utf8mb4',
    autocommit=True,
    minsize=1,
    maxsize=10
)
```

---

## 💾 Backup and Maintenance

### Setup Automated Backups

#### 1. Make backup script executable

```bash
chmod +x /path/to/database/04_backup_restore.sh
```

#### 2. Edit script configuration

```bash
nano /path/to/database/04_backup_restore.sh
```

Update these variables:
```bash
DB_USER="butterfly_user"
DB_PASSWORD="your_password"
DB_HOST="192.168.1.50"
BACKUP_DIR="/var/backups/mysql/butterfly_app"
```

#### 3. Create backup directory

```bash
sudo mkdir -p /var/backups/mysql/butterfly_app
sudo chown $USER:$USER /var/backups/mysql/butterfly_app
```

#### 4. Test backup

```bash
./04_backup_restore.sh backup
```

#### 5. Setup Cron Job for Daily Backups

```bash
crontab -e
```

Add this line for daily backup at 2 AM:
```cron
0 2 * * * /path/to/database/04_backup_restore.sh backup >> /var/log/butterfly_backup.log 2>&1
```

Weekly cleanup (keep last 30 days):
```cron
0 3 * * 0 /path/to/database/04_backup_restore.sh clean 30 >> /var/log/butterfly_backup.log 2>&1
```

### Manual Backup Commands

```bash
# Full backup
./04_backup_restore.sh backup

# Data only
./04_backup_restore.sh data

# Schema only
./04_backup_restore.sh schema

# Export to CSV
./04_backup_restore.sh csv

# List backups
./04_backup_restore.sh list

# Restore
./04_backup_restore.sh restore /path/to/backup.sql.gz
```

---

## 🔧 Performance Tuning

### MySQL Configuration Optimization

Edit MySQL config (`/etc/mysql/mysql.conf.d/mysqld.cnf`):

```ini
[mysqld]
# Connection Settings
max_connections = 200
connect_timeout = 10
wait_timeout = 600

# Buffer Pool (set to 70% of RAM for dedicated DB server)
innodb_buffer_pool_size = 2G
innodb_log_file_size = 512M

# Query Cache
query_cache_type = 1
query_cache_size = 64M

# Performance Schema
performance_schema = ON

# Logging
slow_query_log = 1
slow_query_log_file = /var/log/mysql/slow-query.log
long_query_time = 2
```

Restart MySQL after changes:
```bash
sudo systemctl restart mysql
```

### Monitor Database Performance

```sql
-- Show current connections
SHOW PROCESSLIST;

-- Show table sizes
SELECT 
    table_name AS 'Table',
    ROUND(((data_length + index_length) / 1024 / 1024), 2) AS 'Size (MB)'
FROM information_schema.TABLES
WHERE table_schema = 'butterfly_app'
ORDER BY (data_length + index_length) DESC;

-- Show slow queries
SELECT * FROM mysql.slow_log ORDER BY start_time DESC LIMIT 10;
```

---

## 🐛 Troubleshooting

### Common Issues

#### 1. Connection Refused

**Problem:** `ERROR 2003: Can't connect to MySQL server`

**Solutions:**
```bash
# Check if MySQL is running
sudo systemctl status mysql

# Check if port 3306 is listening
sudo netstat -tlnp | grep 3306

# Check bind-address in config
grep "bind-address" /etc/mysql/mysql.conf.d/mysqld.cnf

# Check firewall
sudo ufw status  # Ubuntu
sudo firewall-cmd --list-all  # CentOS
```

#### 2. Access Denied

**Problem:** `ERROR 1045: Access denied for user`

**Solutions:**
```bash
# Verify user exists
mysql -u root -p -e "SELECT User, Host FROM mysql.user WHERE User='butterfly_user';"

# Check grants
mysql -u root -p -e "SHOW GRANTS FOR 'butterfly_user'@'%';"

# Reset password if needed
mysql -u root -p -e "ALTER USER 'butterfly_user'@'%' IDENTIFIED BY 'new_password'; FLUSH PRIVILEGES;"
```

#### 3. Too Many Connections

**Problem:** `ERROR 1040: Too many connections`

**Solution:**
```sql
-- Check current connections
SHOW PROCESSLIST;

-- Increase max_connections
SET GLOBAL max_connections = 300;

-- Make permanent in my.cnf
-- max_connections = 300
```

#### 4. Slow Queries

**Solution:**
```sql
-- Add missing indexes
SHOW INDEX FROM butterflies;

-- Analyze slow queries
EXPLAIN SELECT * FROM butterflies WHERE difficulty = 1;

-- Optimize tables
OPTIMIZE TABLE butterflies;
OPTIMIZE TABLE scores;
```

### Check Application Logs

```bash
# Backend logs
tail -f /var/log/supervisor/backend.err.log

# MySQL error log
tail -f /var/log/mysql/error.log

# Check connection pool status (add to server.py for debugging)
# logger.info(f"Pool size: {db_pool.size()}, free: {db_pool.freesize()}")
```

---

## 📊 Monitoring and Health Checks

### Create Health Check Queries

```sql
-- Database health
SELECT 
    'Database' as component,
    IF(COUNT(*) > 0, 'UP', 'DOWN') as status,
    COUNT(*) as butterfly_count
FROM butterflies;

-- Check replication (if configured)
SHOW SLAVE STATUS\G
```

### Setup Monitoring Script

Create `/usr/local/bin/mysql_health_check.sh`:

```bash
#!/bin/bash
mysql -u butterfly_readonly -p'readonly_password' butterfly_app -e "SELECT COUNT(*) FROM butterflies;" > /dev/null 2>&1

if [ $? -eq 0 ]; then
    echo "MySQL: OK"
    exit 0
else
    echo "MySQL: FAILED"
    exit 1
fi
```

---

## 📝 Quick Reference

### Essential Commands

```bash
# Service Management
sudo systemctl start mysql
sudo systemctl stop mysql
sudo systemctl restart mysql
sudo systemctl status mysql

# Connect to Database
mysql -h [host] -u [user] -p [database]

# Import SQL File
mysql -u root -p butterfly_app < file.sql

# Export Database
mysqldump -u root -p butterfly_app > backup.sql

# Show Databases
mysql -u root -p -e "SHOW DATABASES;"

# Show Tables
mysql -u root -p butterfly_app -e "SHOW TABLES;"
```

### Important Files

- **Config**: `/etc/mysql/mysql.conf.d/mysqld.cnf`
- **Error Log**: `/var/log/mysql/error.log`
- **Slow Query Log**: `/var/log/mysql/slow-query.log`
- **Data Directory**: `/var/lib/mysql/`

---

## 📞 Support and Documentation

- MySQL Official Docs: https://dev.mysql.com/doc/
- MariaDB Docs: https://mariadb.com/kb/en/
- Stack Overflow: https://stackoverflow.com/questions/tagged/mysql

---

## ✅ Deployment Checklist

- [ ] MySQL server installed and running
- [ ] Database created (`butterfly_app`)
- [ ] Schema created (tables: `butterflies`, `scores`)
- [ ] Seed data inserted (30 butterflies)
- [ ] Application user created with proper permissions
- [ ] Firewall configured
- [ ] Remote access tested from application server
- [ ] Backend `.env` updated with database credentials
- [ ] Application connection tested
- [ ] Backup script configured and tested
- [ ] Cron jobs setup for automated backups
- [ ] Monitoring in place
- [ ] Performance tuning applied
- [ ] Documentation shared with team

---

**Last Updated**: December 2024  
**Version**: 1.0
