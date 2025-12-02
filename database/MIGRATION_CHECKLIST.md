# MySQL Database Migration Checklist
## Butterfly Identification App

Use this checklist to track your database migration progress.

---

## 📋 Pre-Migration Planning

- [ ] **Review current database size and usage patterns**
  - Current data volume: _____ MB
  - Average queries per second: _____
  - Peak usage times: _____

- [ ] **Select target server**
  - Server type: [ ] Dedicated [ ] VPS [ ] Cloud (AWS/GCP/Azure)
  - OS: [ ] Ubuntu [ ] CentOS [ ] Debian
  - RAM: _____ GB
  - Storage: _____ GB

- [ ] **Plan migration window**
  - Scheduled date/time: _____
  - Estimated downtime: _____
  - Rollback plan prepared: [ ] Yes [ ] No

- [ ] **Backup current database**
  - Full backup created: [ ] Yes - Date: _____
  - Backup verified: [ ] Yes
  - Backup location: _____

---

## 🖥️ Target Server Setup

### MySQL Installation

- [ ] **Install MySQL/MariaDB**
  ```bash
  sudo apt-get install mysql-server  # or mariadb-server
  ```

- [ ] **Secure MySQL installation**
  ```bash
  sudo mysql_secure_installation
  ```
  - [ ] Root password set
  - [ ] Anonymous users removed
  - [ ] Root login remotely disallowed
  - [ ] Test database removed

- [ ] **Configure MySQL for remote access**
  - [ ] Edit `/etc/mysql/mysql.conf.d/mysqld.cnf`
  - [ ] Set `bind-address = 0.0.0.0` (or specific IP)
  - [ ] MySQL service restarted

- [ ] **Verify MySQL is running**
  ```bash
  sudo systemctl status mysql
  ```

---

## 🗄️ Database Creation

- [ ] **Create database**
  ```bash
  mysql -u root -p < 01_schema.sql
  ```

- [ ] **Verify schema creation**
  ```sql
  USE butterfly_app;
  SHOW TABLES;
  ```
  - [ ] Table `butterflies` created
  - [ ] Table `scores` created

- [ ] **Verify indexes**
  ```sql
  SHOW INDEX FROM butterflies;
  SHOW INDEX FROM scores;
  ```
  - [ ] Indexes on `difficulty` column
  - [ ] Indexes on `username` column
  - [ ] Other indexes created

---

## 🌱 Data Migration

- [ ] **Load seed data (30 butterflies)**
  ```bash
  mysql -u root -p butterfly_app < 02_seed_data.sql
  ```

- [ ] **OR restore from backup**
  ```bash
  ./04_backup_restore.sh restore /path/to/backup.sql.gz
  ```

- [ ] **Verify butterfly count**
  ```sql
  SELECT COUNT(*) FROM butterflies;
  -- Expected: 30
  ```

- [ ] **Verify data distribution**
  ```sql
  SELECT difficulty, COUNT(*) FROM butterflies GROUP BY difficulty;
  -- Easy: 7, Medium: 11, Hard: 12
  ```

- [ ] **Verify scores data** (if migrating existing data)
  ```sql
  SELECT COUNT(*) FROM scores;
  ```

---

## 🔐 Security Configuration

- [ ] **Create application database user**
  - [ ] Edit `03_user_and_permissions.sql` with strong passwords
  - [ ] Run script: `mysql -u root -p < 03_user_and_permissions.sql`

- [ ] **Verify user creation**
  ```sql
  SELECT User, Host FROM mysql.user WHERE User LIKE 'butterfly%';
  ```
  - [ ] User `butterfly_user` created
  - [ ] User `butterfly_readonly` created (optional)

- [ ] **Verify permissions**
  ```sql
  SHOW GRANTS FOR 'butterfly_user'@'%';
  ```

- [ ] **Test user connection**
  ```bash
  mysql -h localhost -u butterfly_user -p butterfly_app
  ```

- [ ] **Configure firewall**
  - [ ] Port 3306 opened for application server IP
  - [ ] Other unnecessary ports closed
  ```bash
  sudo ufw allow from <APP_SERVER_IP> to any port 3306
  sudo ufw enable
  ```

---

## ⚙️ Application Configuration

- [ ] **Update backend .env file**
  ```bash
  MYSQL_HOST=<DB_SERVER_IP>
  MYSQL_USER=butterfly_user
  MYSQL_PASSWORD=<STRONG_PASSWORD>
  MYSQL_DATABASE=butterfly_app
  MYSQL_PORT=3306
  ```

- [ ] **Test connection from application server**
  ```bash
  # Install MySQL client on app server
  sudo apt-get install mysql-client
  
  # Test connection
  mysql -h <DB_SERVER_IP> -u butterfly_user -p butterfly_app
  ```

- [ ] **Restart application backend**
  ```bash
  sudo supervisorctl restart backend
  ```

- [ ] **Check backend logs for connection**
  ```bash
  tail -f /var/log/supervisor/backend.err.log
  # Look for: "MySQL connection pool created"
  ```

---

## 🧪 Testing & Verification

### Backend API Tests

- [ ] **Test GET /api/butterflies**
  ```bash
  curl http://localhost:8001/api/butterflies
  # Should return 30 butterflies
  ```

- [ ] **Test GET /api/quiz/question?difficulty=1**
  ```bash
  curl http://localhost:8001/api/quiz/question?difficulty=1
  # Should return quiz question with 5 options
  ```

- [ ] **Test GET /api/admin/butterflies**
  ```bash
  curl http://localhost:8001/api/admin/butterflies
  # Should return all butterflies with admin fields
  ```

- [ ] **Test POST /api/admin/butterfly** (create)
  ```bash
  curl -X POST http://localhost:8001/api/admin/butterfly \
    -H "Content-Type: application/json" \
    -d '{"commonName":"Test Butterfly","latinName":"Testus butterflii","imageUrl":"https://example.com/test.jpg","difficulty":1}'
  ```

- [ ] **Test PUT /api/admin/butterfly/{id}** (update)

- [ ] **Test DELETE /api/admin/butterfly/{id}** (delete)

- [ ] **Test POST /api/scores** (save score)
  ```bash
  curl -X POST http://localhost:8001/api/scores \
    -H "Content-Type: application/json" \
    -d '{"username":"testuser","score":8,"total":10,"difficulty":1,"percentage":80,"date":"2024-12-02T12:00:00"}'
  ```

- [ ] **Test GET /api/scores/{username}** (get user scores)
  ```bash
  curl http://localhost:8001/api/scores/testuser
  ```

### Frontend Tests

- [ ] **Home screen loads**
- [ ] **Game starts and loads questions**
- [ ] **Questions show butterfly images**
- [ ] **Score submission works**
- [ ] **Personal scores display correctly**
- [ ] **Admin panel loads butterfly list**
- [ ] **Admin can add new butterfly**
- [ ] **Admin can edit butterfly**
- [ ] **Admin can delete butterfly**

---

## 💾 Backup Setup

- [ ] **Configure backup script**
  - [ ] Make script executable: `chmod +x 04_backup_restore.sh`
  - [ ] Edit script with database credentials
  - [ ] Set backup directory path

- [ ] **Test manual backup**
  ```bash
  ./04_backup_restore.sh backup
  ```
  - [ ] Backup file created
  - [ ] File size reasonable
  - [ ] Compression working (.gz file)

- [ ] **Test manual restore**
  ```bash
  ./04_backup_restore.sh restore /path/to/backup.sql.gz
  ```

- [ ] **Setup automated backups (cron)**
  ```bash
  crontab -e
  # Add: 0 2 * * * /path/to/04_backup_restore.sh backup >> /var/log/butterfly_backup.log 2>&1
  ```
  - [ ] Daily backup scheduled
  - [ ] Log file location configured
  - [ ] Backup retention policy set (e.g., 30 days)

- [ ] **Setup backup monitoring**
  - [ ] Email notifications configured (optional)
  - [ ] Backup size monitoring
  - [ ] Failed backup alerts

---

## 📊 Performance Optimization

- [ ] **Review MySQL configuration**
  - [ ] `max_connections` set appropriately
  - [ ] `innodb_buffer_pool_size` configured (70% of RAM)
  - [ ] Query cache enabled

- [ ] **Verify indexes are being used**
  ```sql
  EXPLAIN SELECT * FROM butterflies WHERE difficulty = 1;
  EXPLAIN SELECT * FROM scores WHERE username = 'testuser';
  ```

- [ ] **Enable slow query log**
  ```ini
  slow_query_log = 1
  long_query_time = 2
  ```

- [ ] **Analyze tables**
  ```sql
  ANALYZE TABLE butterflies;
  ANALYZE TABLE scores;
  ```

---

## 📝 Documentation

- [ ] **Update application documentation**
  - [ ] New database server IP/hostname
  - [ ] Database connection details
  - [ ] Backup procedures

- [ ] **Document credentials**
  - [ ] Store in secure password manager
  - [ ] Share with authorized team members only

- [ ] **Create runbook for common operations**
  - [ ] How to restart MySQL
  - [ ] How to create backup
  - [ ] How to restore backup
  - [ ] How to check database status

---

## 🔄 Post-Migration

- [ ] **Monitor application for 24 hours**
  - [ ] No connection errors
  - [ ] Response times acceptable
  - [ ] No data inconsistencies

- [ ] **Monitor database server**
  - [ ] CPU usage normal
  - [ ] Memory usage acceptable
  - [ ] Disk I/O within limits
  - [ ] Connection count stable

- [ ] **Verify backup jobs ran successfully**
  ```bash
  ls -lh /var/backups/mysql/butterfly_app/
  cat /var/log/butterfly_backup.log
  ```

- [ ] **Review logs for errors**
  ```bash
  tail -f /var/log/mysql/error.log
  tail -f /var/log/supervisor/backend.err.log
  ```

- [ ] **Performance baseline established**
  - [ ] Average query response time: _____ ms
  - [ ] Peak connections: _____
  - [ ] Daily backup size: _____ MB

---

## 🆘 Rollback Procedures

**If migration fails:**

- [ ] **Revert application .env to old database**
  ```bash
  MYSQL_HOST=old_db_server
  ```

- [ ] **Restart backend**
  ```bash
  sudo supervisorctl restart backend
  ```

- [ ] **Verify old database is working**

- [ ] **Document what went wrong**

- [ ] **Plan re-migration with fixes**

---

## ✅ Migration Sign-Off

**Completed by:** _____________________

**Date:** _____________________

**Verified by:** _____________________

**Issues encountered:** 

_________________________________________

_________________________________________

**Notes:**

_________________________________________

_________________________________________

---

## 📞 Emergency Contacts

**Database Administrator:** _____________________

**Backend Developer:** _____________________

**DevOps Engineer:** _____________________

**On-call Support:** _____________________

---

## 📚 Reference Files

- `01_schema.sql` - Database schema
- `02_seed_data.sql` - Butterfly seed data
- `03_user_and_permissions.sql` - User setup
- `04_backup_restore.sh` - Backup/restore scripts
- `DEPLOYMENT_GUIDE.md` - Detailed instructions
- `README.md` - Quick reference

---

**Version:** 1.0  
**Last Updated:** December 2024
