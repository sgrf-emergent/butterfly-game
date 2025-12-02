# MySQL Database Scripts - Butterfly Identification App

Complete database scripts, schema, seed data, and deployment instructions for migrating MySQL to a separate server.

---

## 📁 Files Overview

| File | Purpose | When to Use |
|------|---------|-------------|
| `01_schema.sql` | Database and table creation | Initial setup or schema updates |
| `02_seed_data.sql` | 30 butterfly species data | Initial data population |
| `03_user_and_permissions.sql` | User creation and access control | Security setup |
| `04_backup_restore.sh` | Automated backup/restore | Daily backups and disaster recovery |
| `DEPLOYMENT_GUIDE.md` | Step-by-step deployment | Complete deployment reference |
| `MIGRATION_CHECKLIST.md` | Migration verification | Track deployment progress |

---

## 🚀 Quick Start

### For Fresh Installation

```bash
# 1. Install MySQL/MariaDB on your server
sudo apt-get install mysql-server  # Ubuntu/Debian

# 2. Secure MySQL installation
sudo mysql_secure_installation

# 3. Create database and tables
mysql -u root -p < 01_schema.sql

# 4. Load butterfly data (30 species)
mysql -u root -p butterfly_app < 02_seed_data.sql

# 5. Create application user (EDIT PASSWORDS FIRST!)
mysql -u root -p < 03_user_and_permissions.sql

# 6. Verify installation
mysql -u root -p butterfly_app -e "SELECT COUNT(*) FROM butterflies;"
```

**Expected Output:**
```
+---------+
| COUNT(*)|
+---------+
|      30 |
+---------+
```

### For Migration from Existing Server

```bash
# 1. Export current data
./04_backup_restore.sh backup

# 2. Transfer backup to new server
scp backup.sql.gz user@new-server:/tmp/

# 3. On new server: Install MySQL and create schema
mysql -u root -p < 01_schema.sql

# 4. Restore data
./04_backup_restore.sh restore /tmp/backup.sql.gz

# 5. Update application .env with new server IP
MYSQL_HOST="new_server_ip"
```

---

## 📊 Database Schema

### Tables

#### `butterflies`
Stores butterfly species information for the quiz game.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | INT | PRIMARY KEY, AUTO_INCREMENT | Unique butterfly ID |
| `commonName` | VARCHAR(255) | NOT NULL | Common name (e.g., "Monarch") |
| `latinName` | VARCHAR(255) | NOT NULL | Scientific name |
| `imageUrl` | TEXT | NOT NULL | URL to butterfly image |
| `difficulty` | INT | NOT NULL, DEFAULT 1, CHECK (1-3) | 1=Easy, 2=Medium, 3=Hard |
| `created_at` | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Creation timestamp |
| `updated_at` | TIMESTAMP | ON UPDATE CURRENT_TIMESTAMP | Last update timestamp |

**Indexes:**
- `idx_difficulty` - For fast difficulty filtering
- `idx_commonName` - For search functionality
- `idx_latinName` - For scientific name lookups

#### `scores`
Stores user game scores and history.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | INT | PRIMARY KEY, AUTO_INCREMENT | Unique score ID |
| `username` | VARCHAR(255) | NOT NULL | Player username |
| `score` | INT | NOT NULL, CHECK (score >= 0) | Points earned |
| `total` | INT | NOT NULL | Total possible points |
| `difficulty` | INT | NOT NULL, CHECK (1-3) | Game difficulty level |
| `percentage` | INT | NOT NULL, CHECK (0-100) | Score percentage |
| `date` | DATETIME | NOT NULL | When game was played |
| `created_at` | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Record creation |

**Indexes:**
- `idx_username` - For user score lookups
- `idx_date` - For chronological queries
- `idx_difficulty_score` - For leaderboards
- `idx_username_date` - For user history

---

## 🌱 Seed Data

The database includes **30 butterfly species** distributed by difficulty:

- **Easy (7 species)**: Common, easily recognizable butterflies
- **Medium (11 species)**: Moderately difficult to identify
- **Hard (12 species)**: Challenging species for advanced players

### Butterfly Difficulty Distribution

```sql
SELECT difficulty, COUNT(*) as count
FROM butterflies
GROUP BY difficulty;
```

**Expected:**
```
+------------+-------+
| difficulty | count |
+------------+-------+
|          1 |     7 |
|          2 |    11 |
|          3 |    12 |
+------------+-------+
```

---

## 🔐 Security Best Practices

### 1. Change Default Passwords

**⚠️ CRITICAL:** Edit `03_user_and_permissions.sql` before running:

```sql
-- Replace these with strong passwords:
CREATE USER 'butterfly_user'@'%' IDENTIFIED BY 'YOUR_STRONG_PASSWORD_HERE';
CREATE USER 'butterfly_readonly'@'%' IDENTIFIED BY 'ANOTHER_STRONG_PASSWORD';
```

### 2. Restrict Host Access

Instead of `'%'` (allow all hosts), use specific IPs:

```sql
-- Only allow from application server
CREATE USER 'butterfly_user'@'192.168.1.100' IDENTIFIED BY 'password';
```

### 3. Use Environment Variables

**Never hardcode credentials!** Use `.env` file:

```bash
MYSQL_HOST=192.168.1.50
MYSQL_USER=butterfly_user
MYSQL_PASSWORD=secure_password_here
MYSQL_DATABASE=butterfly_app
MYSQL_PORT=3306
```

### 4. Enable SSL/TLS

For production, require encrypted connections:

```sql
ALTER USER 'butterfly_user'@'%' REQUIRE SSL;
```

---

## 💾 Backup Strategy

### Automated Daily Backups

```bash
# Make script executable
chmod +x 04_backup_restore.sh

# Edit configuration
nano 04_backup_restore.sh
# Update: DB_USER, DB_PASSWORD, DB_HOST, BACKUP_DIR

# Test backup
./04_backup_restore.sh backup

# Setup cron job (daily at 2 AM)
crontab -e
# Add: 0 2 * * * /path/to/04_backup_restore.sh backup >> /var/log/butterfly_backup.log 2>&1
```

### Backup Types

```bash
# Full backup (schema + data)
./04_backup_restore.sh backup

# Data only (for migrations)
./04_backup_restore.sh data

# Schema only (for version control)
./04_backup_restore.sh schema

# Export to CSV (for analytics)
./04_backup_restore.sh csv

# List all backups
./04_backup_restore.sh list

# Clean old backups (keep last 30 days)
./04_backup_restore.sh clean 30
```

### Restore from Backup

```bash
./04_backup_restore.sh restore /path/to/backup.sql.gz
```

---

## 🔧 Configuration Examples

### Development Environment

```bash
# .env
MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=root
MYSQL_DATABASE=butterfly_app
```

### Production Environment

```bash
# .env
MYSQL_HOST=db.production.com
MYSQL_USER=butterfly_user
MYSQL_PASSWORD=x8Kp#mQ2$nL9wR
MYSQL_DATABASE=butterfly_app
MYSQL_PORT=3306
# Optional SSL
MYSQL_SSL_CA=/etc/ssl/certs/ca-cert.pem
MYSQL_SSL_CERT=/etc/ssl/certs/client-cert.pem
MYSQL_SSL_KEY=/etc/ssl/private/client-key.pem
```

### Staging Environment

```bash
# .env
MYSQL_HOST=staging-db.internal
MYSQL_USER=butterfly_staging
MYSQL_PASSWORD=staging_password
MYSQL_DATABASE=butterfly_app_staging
```

---

## 📈 Performance Optimization

### Recommended MySQL Configuration

```ini
# /etc/mysql/mysql.conf.d/mysqld.cnf

[mysqld]
# Connection settings
max_connections = 200
connect_timeout = 10

# Buffer settings (70% of available RAM for dedicated DB server)
innodb_buffer_pool_size = 2G
innodb_log_file_size = 512M

# Query cache
query_cache_type = 1
query_cache_size = 64M

# Performance monitoring
performance_schema = ON
```

### Index Optimization

All necessary indexes are created by `01_schema.sql`:
- Difficulty-based queries are optimized
- Username lookups are fast
- Date-range queries for scores are efficient

### Query Performance Tips

```sql
-- Use EXPLAIN to check query plans
EXPLAIN SELECT * FROM butterflies WHERE difficulty = 1;

-- Analyze table statistics
ANALYZE TABLE butterflies;
ANALYZE TABLE scores;

-- Optimize tables periodically
OPTIMIZE TABLE butterflies;
OPTIMIZE TABLE scores;
```

---

## 🧪 Testing Database Setup

### Verify Installation

```bash
# Check database exists
mysql -u root -p -e "SHOW DATABASES LIKE 'butterfly_app';"

# Check tables
mysql -u root -p butterfly_app -e "SHOW TABLES;"

# Check butterfly count
mysql -u root -p butterfly_app -e "SELECT COUNT(*) as total FROM butterflies;"

# Check data distribution
mysql -u root -p butterfly_app -e "SELECT difficulty, COUNT(*) FROM butterflies GROUP BY difficulty;"

# Verify indexes
mysql -u root -p butterfly_app -e "SHOW INDEX FROM butterflies;"
```

### Test Application User

```bash
# Test connection
mysql -h [host] -u butterfly_user -p butterfly_app

# Test read access
mysql -u butterfly_user -p butterfly_app -e "SELECT * FROM butterflies LIMIT 1;"

# Test write access
mysql -u butterfly_user -p butterfly_app -e "INSERT INTO scores (username, score, total, difficulty, percentage, date) VALUES ('testuser', 8, 10, 1, 80, NOW());"
```

### Test from Application Server

```python
# Python connection test
import aiomysql
import asyncio

async def test_connection():
    pool = await aiomysql.create_pool(
        host='your_db_host',
        user='butterfly_user',
        password='your_password',
        db='butterfly_app',
        charset='utf8mb4'
    )
    async with pool.acquire() as conn:
        async with conn.cursor() as cursor:
            await cursor.execute("SELECT COUNT(*) FROM butterflies")
            result = await cursor.fetchone()
            print(f"✓ Connection successful! Butterflies: {result[0]}")
    pool.close()
    await pool.wait_closed()

asyncio.run(test_connection())
```

---

## 📋 Common Queries

### Get all butterflies by difficulty

```sql
SELECT * FROM butterflies WHERE difficulty = 1 ORDER BY commonName;
```

### Get user's personal best scores

```sql
SELECT 
    difficulty,
    MAX(percentage) as best_percentage,
    MAX(score) as best_score
FROM scores 
WHERE username = 'john_doe' 
GROUP BY difficulty;
```

### Get recent high scores

```sql
SELECT 
    username,
    score,
    percentage,
    difficulty,
    date
FROM scores 
WHERE percentage >= 80
ORDER BY date DESC 
LIMIT 10;
```

### Get butterfly statistics

```sql
SELECT 
    difficulty,
    COUNT(*) as count,
    CASE difficulty
        WHEN 1 THEN 'Easy'
        WHEN 2 THEN 'Medium'
        WHEN 3 THEN 'Hard'
    END as level_name
FROM butterflies
GROUP BY difficulty;
```

---

## 🆘 Troubleshooting

### Connection Issues

```bash
# Check MySQL is running
sudo systemctl status mysql

# Check if port 3306 is open
sudo netstat -tlnp | grep 3306

# Test from application server
telnet db_host 3306

# Check firewall
sudo ufw status
sudo iptables -L -n
```

### Permission Issues

```sql
-- Show user grants
SHOW GRANTS FOR 'butterfly_user'@'%';

-- Reset user password
ALTER USER 'butterfly_user'@'%' IDENTIFIED BY 'new_password';
FLUSH PRIVILEGES;
```

### Performance Issues

```sql
-- Check slow queries
SELECT * FROM mysql.slow_log ORDER BY start_time DESC LIMIT 10;

-- Check current connections
SHOW PROCESSLIST;

-- Check table sizes
SELECT 
    table_name,
    ROUND(((data_length + index_length) / 1024 / 1024), 2) AS 'Size (MB)'
FROM information_schema.TABLES
WHERE table_schema = 'butterfly_app';
```

---

## 📚 Additional Resources

- **Full Deployment Guide**: See `DEPLOYMENT_GUIDE.md`
- **Migration Checklist**: See `MIGRATION_CHECKLIST.md`
- **MySQL Documentation**: https://dev.mysql.com/doc/
- **aiomysql Documentation**: https://aiomysql.readthedocs.io/

---

## 📞 Support

For issues or questions:
1. Check `DEPLOYMENT_GUIDE.md` for detailed instructions
2. Review `MIGRATION_CHECKLIST.md` for deployment verification
3. Test backup/restore procedures regularly
4. Monitor database logs for errors

---

**Version**: 1.0  
**Last Updated**: December 2024  
**Database**: MySQL 5.7+ / MariaDB 10.3+  
**Application**: Butterfly Identification Game
