# Quick Start Guide - MySQL Database Setup
## Butterfly Identification App

This is a **quick reference** for setting up the MySQL database on a separate server.

For detailed instructions, see **DEPLOYMENT_GUIDE.md**

---

## ⚡ 5-Minute Setup (Development)

```bash
# 1. Install MySQL
sudo apt-get update
sudo apt-get install -y mysql-server

# 2. Start MySQL
sudo systemctl start mysql
sudo systemctl enable mysql

# 3. Create database and tables
cd /app/database
mysql -u root -p < 01_schema.sql

# 4. Load 30 butterflies
mysql -u root -p butterfly_app < 02_seed_data.sql

# 5. Create app user (EDIT PASSWORDS FIRST!)
mysql -u root -p < 03_user_and_permissions.sql

# 6. Verify
mysql -u root -p butterfly_app -e "SELECT COUNT(*) FROM butterflies;"
# Should show: 30

# 7. Update app .env
nano /app/backend/.env
# Set: MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DATABASE

# 8. Restart backend
sudo supervisorctl restart backend
```

**Done!** ✅

---

## 📁 File Guide

| File | Use It For |
|------|-----------|
| `01_schema.sql` | Create database structure |
| `02_seed_data.sql` | Add 30 butterfly species |
| `03_user_and_permissions.sql` | Create database users |
| `04_backup_restore.sh` | Daily backups |
| `README.md` | Quick reference |
| `DEPLOYMENT_GUIDE.md` | Full instructions |
| `MIGRATION_CHECKLIST.md` | Track progress |

---

## 🔒 Security Essentials

### 1. Change Passwords!

Edit `03_user_and_permissions.sql` **before** running it:

```sql
-- Line 12: Change this password!
CREATE USER 'butterfly_user'@'%' IDENTIFIED BY 'YOUR_STRONG_PASSWORD_HERE';
```

### 2. Configure Firewall

```bash
# Ubuntu
sudo ufw allow from <APP_SERVER_IP> to any port 3306
sudo ufw enable

# CentOS
sudo firewall-cmd --permanent --add-rich-rule='rule family="ipv4" source address="<APP_SERVER_IP>/32" port="tcp" port="3306" accept'
sudo firewall-cmd --reload
```

### 3. Update Application

Edit `/app/backend/.env`:

```bash
MYSQL_HOST=192.168.1.50        # Your DB server IP
MYSQL_USER=butterfly_user
MYSQL_PASSWORD=your_password    # Must match step 1
MYSQL_DATABASE=butterfly_app
```

---

## 🧪 Quick Test

```bash
# Test from application server
mysql -h <DB_SERVER_IP> -u butterfly_user -p butterfly_app

# In MySQL shell:
SELECT COUNT(*) FROM butterflies;  -- Should return 30
SELECT * FROM butterflies LIMIT 1;
exit
```

---

## 💾 Setup Daily Backups

```bash
# Make script executable
chmod +x /app/database/04_backup_restore.sh

# Edit configuration (lines 14-17)
nano /app/database/04_backup_restore.sh

# Test backup
./04_backup_restore.sh backup

# Add to cron (runs daily at 2 AM)
crontab -e
# Add this line:
0 2 * * * /app/database/04_backup_restore.sh backup >> /var/log/butterfly_backup.log 2>&1
```

---

## 📊 Database Schema

### `butterflies` Table (30 rows)
- `id` - Auto-increment integer
- `commonName` - Butterfly name
- `latinName` - Scientific name  
- `imageUrl` - Image URL
- `difficulty` - 1=Easy, 2=Medium, 3=Hard

### `scores` Table
- `id` - Auto-increment integer
- `username` - Player name
- `score` - Points earned
- `total` - Total possible
- `difficulty` - Game difficulty
- `percentage` - Score %
- `date` - When played

---

## 🆘 Troubleshooting

### Can't connect to MySQL

```bash
# Check if MySQL is running
sudo systemctl status mysql

# Check if port is open
sudo netstat -tlnp | grep 3306

# Check firewall
sudo ufw status
```

### Access denied

```bash
# Reset password
mysql -u root -p
ALTER USER 'butterfly_user'@'%' IDENTIFIED BY 'new_password';
FLUSH PRIVILEGES;
```

### Backend can't connect

```bash
# Check backend logs
tail -f /var/log/supervisor/backend.err.log

# Test from application server
mysql -h <DB_IP> -u butterfly_user -p butterfly_app
```

---

## 📞 Need Help?

1. **Full Instructions**: Read `DEPLOYMENT_GUIDE.md`
2. **Step-by-Step Checklist**: Use `MIGRATION_CHECKLIST.md`
3. **Common Queries**: See `README.md`

---

## ✅ Verification Checklist

After setup, verify:

- [ ] MySQL is running: `sudo systemctl status mysql`
- [ ] Database exists: `mysql -e "SHOW DATABASES LIKE 'butterfly_app';"`
- [ ] 30 butterflies loaded: `mysql butterfly_app -e "SELECT COUNT(*) FROM butterflies;"`
- [ ] App user works: `mysql -u butterfly_user -p butterfly_app`
- [ ] Backend connects: Check logs for "MySQL connection pool created"
- [ ] API works: `curl http://localhost:8001/api/butterflies`
- [ ] Backup tested: `./04_backup_restore.sh backup`

---

## 🎯 Quick Commands

```bash
# Connect to database
mysql -u root -p butterfly_app

# Show tables
mysql -u root -p butterfly_app -e "SHOW TABLES;"

# Count butterflies
mysql -u root -p butterfly_app -e "SELECT COUNT(*) FROM butterflies;"

# Backup database
./04_backup_restore.sh backup

# Restore database
./04_backup_restore.sh restore /path/to/backup.sql.gz

# List backups
./04_backup_restore.sh list

# View logs
tail -f /var/log/mysql/error.log
tail -f /var/log/supervisor/backend.err.log
```

---

**Ready in 5 minutes!** 🚀

For production deployment, follow the complete **DEPLOYMENT_GUIDE.md**
