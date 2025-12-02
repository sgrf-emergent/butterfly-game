# Python FastAPI Application Deployment Guide
## After MySQL Migration

Complete guide for deploying and running the Python backend application after migrating MySQL to a separate server.

---

## 📋 Table of Contents
1. [Prerequisites](#prerequisites)
2. [Environment Configuration](#environment-configuration)
3. [Dependencies Installation](#dependencies-installation)
4. [Running the Application](#running-the-application)
5. [Process Management](#process-management)
6. [Testing Deployment](#testing-deployment)
7. [Monitoring & Logs](#monitoring--logs)
8. [Production Deployment](#production-deployment)
9. [Troubleshooting](#troubleshooting)

---

## 🔧 Prerequisites

### System Requirements
- **OS**: Ubuntu 20.04+ / CentOS 7+ / Debian 10+
- **Python**: 3.8+ (3.10+ recommended)
- **RAM**: Minimum 1GB (2GB+ recommended)
- **MySQL Client**: For testing database connection

### MySQL Database Server
- ✅ MySQL server running on separate server
- ✅ Database `butterfly_app` created
- ✅ User `butterfly_user` created with permissions
- ✅ Firewall configured to allow connections
- ✅ Connection tested successfully

---

## ⚙️ Environment Configuration

### Step 1: Update Backend `.env` File

**Location**: `/app/backend/.env`

```bash
cd /app/backend
nano .env
```

**Configuration**:

```bash
# ============================================
# MySQL Database Configuration (REQUIRED)
# ============================================

# Database server IP or hostname
MYSQL_HOST=192.168.1.50

# Database port (default: 3306)
MYSQL_PORT=3306

# Database name
MYSQL_DATABASE=butterfly_app

# Database credentials
MYSQL_USER=butterfly_user
MYSQL_PASSWORD=your_secure_password_here

# ============================================
# Optional: SSL Configuration (Production)
# ============================================

# Uncomment for SSL/TLS connections
# MYSQL_SSL_CA=/etc/ssl/certs/ca-cert.pem
# MYSQL_SSL_CERT=/etc/ssl/certs/client-cert.pem
# MYSQL_SSL_KEY=/etc/ssl/private/client-key.pem

# ============================================
# Application Configuration (Optional)
# ============================================

# Environment
ENVIRONMENT=production  # or development, staging

# API Settings
API_HOST=0.0.0.0
API_PORT=8001

# Connection Pool Settings
DB_POOL_MIN_SIZE=1
DB_POOL_MAX_SIZE=10

# Logging
LOG_LEVEL=INFO  # DEBUG, INFO, WARNING, ERROR
```

### Step 2: Secure Environment File

```bash
# Set proper permissions (readable only by owner)
chmod 600 /app/backend/.env

# Verify
ls -l /app/backend/.env
# Should show: -rw------- (600)
```

### Step 3: Verify Configuration

```bash
# Check environment variables are loaded
cd /app/backend
python3 -c "
from dotenv import load_dotenv
import os
load_dotenv()
print('MYSQL_HOST:', os.getenv('MYSQL_HOST'))
print('MYSQL_DATABASE:', os.getenv('MYSQL_DATABASE'))
print('MYSQL_USER:', os.getenv('MYSQL_USER'))
print('MYSQL_PASSWORD:', '***' if os.getenv('MYSQL_PASSWORD') else 'NOT SET')
"
```

---

## 📦 Dependencies Installation

### Step 1: Check Python Version

```bash
python3 --version
# Should be 3.8 or higher
```

### Step 2: Install System Dependencies

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install -y python3-pip python3-venv python3-dev
sudo apt-get install -y build-essential libssl-dev libffi-dev
sudo apt-get install -y mysql-client  # For testing
```

**CentOS/RHEL:**
```bash
sudo yum update -y
sudo yum install -y python3-pip python3-devel
sudo yum install -y gcc openssl-devel
sudo yum install -y mysql  # For testing
```

### Step 3: Create Virtual Environment (Recommended)

```bash
cd /app/backend

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Verify activation (should show venv path)
which python3
```

### Step 4: Install Python Dependencies

```bash
cd /app/backend

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Verify critical packages
pip list | grep -E "fastapi|uvicorn|aiomysql|pydantic"
```

**Expected Output**:
```
aiomysql      0.2.0
fastapi       0.110.1
pydantic      2.6.4
uvicorn       0.25.0
```

### Step 5: Test Database Connection

Create test script `/app/backend/test_connection.py`:

```python
#!/usr/bin/env python3
"""Test MySQL database connection"""

import asyncio
import aiomysql
import os
from dotenv import load_dotenv

load_dotenv()

async def test_connection():
    try:
        print("🔌 Testing MySQL connection...")
        print(f"Host: {os.getenv('MYSQL_HOST')}")
        print(f"Database: {os.getenv('MYSQL_DATABASE')}")
        print(f"User: {os.getenv('MYSQL_USER')}")
        
        pool = await aiomysql.create_pool(
            host=os.getenv('MYSQL_HOST'),
            port=int(os.getenv('MYSQL_PORT', 3306)),
            user=os.getenv('MYSQL_USER'),
            password=os.getenv('MYSQL_PASSWORD'),
            db=os.getenv('MYSQL_DATABASE'),
            charset='utf8mb4'
        )
        
        async with pool.acquire() as conn:
            async with conn.cursor() as cursor:
                # Test butterflies table
                await cursor.execute("SELECT COUNT(*) FROM butterflies")
                butterfly_count = (await cursor.fetchone())[0]
                
                # Test scores table
                await cursor.execute("SELECT COUNT(*) FROM scores")
                score_count = (await cursor.fetchone())[0]
                
                print(f"✅ Connection successful!")
                print(f"✅ Butterflies: {butterfly_count}")
                print(f"✅ Scores: {score_count}")
        
        pool.close()
        await pool.wait_closed()
        
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(test_connection())
```

**Run test**:
```bash
cd /app/backend
python3 test_connection.py
```

**Expected Output**:
```
🔌 Testing MySQL connection...
Host: 192.168.1.50
Database: butterfly_app
User: butterfly_user
✅ Connection successful!
✅ Butterflies: 30
✅ Scores: 4
```

---

## 🚀 Running the Application

### Option 1: Development Mode (Interactive)

```bash
cd /app/backend

# Activate virtual environment (if using)
source venv/bin/activate

# Run with uvicorn (development server)
uvicorn server:app --host 0.0.0.0 --port 8001 --reload

# Or using python directly
python3 -m uvicorn server:app --host 0.0.0.0 --port 8001 --reload
```

**Flags Explained**:
- `--host 0.0.0.0` - Listen on all network interfaces
- `--port 8001` - Port number
- `--reload` - Auto-reload on code changes (dev only)

**Output**:
```
INFO:     Uvicorn running on http://0.0.0.0:8001
INFO:     Started reloader process [12345]
INFO:     Started server process [12346]
INFO:     Waiting for application startup.
INFO:     MySQL connection pool created
INFO:     Application startup complete.
```

### Option 2: Production Mode (Background)

```bash
cd /app/backend

# Run in background with nohup
nohup uvicorn server:app --host 0.0.0.0 --port 8001 --workers 4 > /var/log/butterfly_app.log 2>&1 &

# Save process ID
echo $! > /var/run/butterfly_app.pid
```

**Production Flags**:
- `--workers 4` - Multiple worker processes (CPU cores)
- No `--reload` - Disabled for production
- `nohup` - Keep running after logout
- `&` - Run in background

### Option 3: Using Gunicorn (Recommended for Production)

```bash
# Install gunicorn
pip install gunicorn

# Run with gunicorn
gunicorn server:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8001 \
  --timeout 120 \
  --access-logfile /var/log/butterfly_access.log \
  --error-logfile /var/log/butterfly_error.log \
  --daemon
```

### Test Application

```bash
# Test API is running
curl http://localhost:8001/api/

# Expected output:
# {"message":"Butterfly Identification API"}

# Test butterflies endpoint
curl http://localhost:8001/api/butterflies | jq length

# Expected output: 30
```

---

## 🔄 Process Management

### Option 1: Systemd Service (Recommended)

Create systemd service file:

```bash
sudo nano /etc/systemd/system/butterfly-api.service
```

**Service Configuration**:

```ini
[Unit]
Description=Butterfly Identification API
After=network.target mysql.service
Requires=network.target

[Service]
Type=notify
User=www-data
Group=www-data
WorkingDirectory=/app/backend
Environment="PATH=/app/backend/venv/bin"
EnvironmentFile=/app/backend/.env

# Use gunicorn for production
ExecStart=/app/backend/venv/bin/gunicorn server:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8001 \
  --timeout 120 \
  --access-logfile /var/log/butterfly_access.log \
  --error-logfile /var/log/butterfly_error.log

# Restart policy
Restart=always
RestartSec=10

# Security
NoNewPrivileges=true
PrivateTmp=true

[Install]
WantedBy=multi-user.target
```

**Enable and Start Service**:

```bash
# Reload systemd
sudo systemctl daemon-reload

# Enable service (start on boot)
sudo systemctl enable butterfly-api

# Start service
sudo systemctl start butterfly-api

# Check status
sudo systemctl status butterfly-api

# View logs
sudo journalctl -u butterfly-api -f
```

**Service Management Commands**:

```bash
# Start
sudo systemctl start butterfly-api

# Stop
sudo systemctl stop butterfly-api

# Restart
sudo systemctl restart butterfly-api

# Status
sudo systemctl status butterfly-api

# Enable auto-start on boot
sudo systemctl enable butterfly-api

# Disable auto-start
sudo systemctl disable butterfly-api

# View logs (follow mode)
sudo journalctl -u butterfly-api -f

# View last 100 lines
sudo journalctl -u butterfly-api -n 100
```

### Option 2: Supervisor (Alternative)

If you're already using Supervisor:

```bash
sudo nano /etc/supervisor/conf.d/butterfly-api.conf
```

**Supervisor Configuration**:

```ini
[program:butterfly-api]
command=/app/backend/venv/bin/uvicorn server:app --host 0.0.0.0 --port 8001 --workers 4
directory=/app/backend
user=www-data
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/var/log/supervisor/butterfly-api.log
environment=PYTHONPATH="/app/backend"
```

**Supervisor Commands**:

```bash
# Reload configuration
sudo supervisorctl reread
sudo supervisorctl update

# Start/Stop/Restart
sudo supervisorctl start butterfly-api
sudo supervisorctl stop butterfly-api
sudo supervisorctl restart butterfly-api

# Check status
sudo supervisorctl status butterfly-api

# View logs
sudo supervisorctl tail -f butterfly-api
```

### Option 3: Docker (Container Deployment)

Create `Dockerfile`:

```dockerfile
FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 8001

# Run application
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8001", "--workers", "4"]
```

**Build and Run**:

```bash
# Build image
docker build -t butterfly-api:latest .

# Run container
docker run -d \
  --name butterfly-api \
  -p 8001:8001 \
  --env-file .env \
  --restart unless-stopped \
  butterfly-api:latest

# View logs
docker logs -f butterfly-api

# Stop container
docker stop butterfly-api

# Start container
docker start butterfly-api
```

---

## 🧪 Testing Deployment

### Health Check Script

Create `/app/backend/health_check.sh`:

```bash
#!/bin/bash

echo "🏥 Health Check - Butterfly API"
echo "================================"

# Test API root
echo -n "✓ API Root: "
curl -s http://localhost:8001/api/ | grep -q "Butterfly" && echo "✅ OK" || echo "❌ FAILED"

# Test butterflies endpoint
echo -n "✓ Butterflies Endpoint: "
BUTTERFLY_COUNT=$(curl -s http://localhost:8001/api/butterflies | jq length)
if [ "$BUTTERFLY_COUNT" -eq 30 ]; then
    echo "✅ OK ($BUTTERFLY_COUNT butterflies)"
else
    echo "❌ FAILED (Expected 30, got $BUTTERFLY_COUNT)"
fi

# Test quiz endpoint
echo -n "✓ Quiz Endpoint (Easy): "
curl -s http://localhost:8001/api/quiz/question?difficulty=1 | grep -q "correctAnswer" && echo "✅ OK" || echo "❌ FAILED"

# Test admin endpoint
echo -n "✓ Admin Endpoint: "
ADMIN_COUNT=$(curl -s http://localhost:8001/api/admin/butterflies | jq length)
if [ "$ADMIN_COUNT" -eq 30 ]; then
    echo "✅ OK ($ADMIN_COUNT butterflies)"
else
    echo "❌ FAILED (Expected 30, got $ADMIN_COUNT)"
fi

echo ""
echo "================================"
echo "Health Check Complete!"
```

**Run Health Check**:

```bash
chmod +x /app/backend/health_check.sh
./health_check.sh
```

### API Testing with curl

```bash
# Test all endpoints

# 1. Root endpoint
curl http://localhost:8001/api/

# 2. Get all butterflies
curl http://localhost:8001/api/butterflies

# 3. Get quiz question (Easy)
curl http://localhost:8001/api/quiz/question?difficulty=1

# 4. Get quiz question (Medium)
curl http://localhost:8001/api/quiz/question?difficulty=2

# 5. Get quiz question (Hard)
curl http://localhost:8001/api/quiz/question?difficulty=3

# 6. Admin - Get all butterflies
curl http://localhost:8001/api/admin/butterflies

# 7. Admin - Create butterfly
curl -X POST http://localhost:8001/api/admin/butterfly \
  -H "Content-Type: application/json" \
  -d '{
    "commonName": "Test Butterfly",
    "latinName": "Testus butterflii",
    "imageUrl": "https://example.com/test.jpg",
    "difficulty": 1
  }'

# 8. Save score
curl -X POST http://localhost:8001/api/scores \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "score": 8,
    "total": 10,
    "difficulty": 1,
    "percentage": 80,
    "date": "2024-12-02T12:00:00"
  }'

# 9. Get user scores
curl http://localhost:8001/api/scores/testuser
```

### Load Testing (Optional)

```bash
# Install Apache Bench
sudo apt-get install apache2-utils

# Test with 1000 requests, 10 concurrent
ab -n 1000 -c 10 http://localhost:8001/api/butterflies

# Or use wrk
sudo apt-get install wrk
wrk -t4 -c100 -d30s http://localhost:8001/api/butterflies
```

---

## 📊 Monitoring & Logs

### Application Logs

**Systemd Service Logs**:
```bash
# Follow logs in real-time
sudo journalctl -u butterfly-api -f

# View last 100 lines
sudo journalctl -u butterfly-api -n 100

# View logs since today
sudo journalctl -u butterfly-api --since today

# View errors only
sudo journalctl -u butterfly-api -p err
```

**Log Files** (if using file logging):
```bash
# Application logs
tail -f /var/log/butterfly_error.log
tail -f /var/log/butterfly_access.log

# Supervisor logs (if using supervisor)
tail -f /var/log/supervisor/butterfly-api.log
```

### Performance Monitoring

Create monitoring script `/usr/local/bin/butterfly_monitor.sh`:

```bash
#!/bin/bash

echo "📊 Butterfly API Monitoring"
echo "============================"
echo ""

# Check if process is running
if pgrep -f "server:app" > /dev/null; then
    echo "✅ Application Status: RUNNING"
    PID=$(pgrep -f "server:app")
    echo "   Process ID: $PID"
else
    echo "❌ Application Status: STOPPED"
    exit 1
fi

# Check API response
RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8001/api/)
if [ "$RESPONSE" -eq 200 ]; then
    echo "✅ API Response: OK (HTTP $RESPONSE)"
else
    echo "❌ API Response: FAILED (HTTP $RESPONSE)"
fi

# Check database connection
DB_TEST=$(curl -s http://localhost:8001/api/butterflies | jq length)
if [ "$DB_TEST" -eq 30 ]; then
    echo "✅ Database Connection: OK ($DB_TEST butterflies)"
else
    echo "⚠️  Database Connection: Warning ($DB_TEST butterflies)"
fi

# Memory usage
MEM_USAGE=$(ps aux | grep "server:app" | grep -v grep | awk '{sum+=$6} END {print sum/1024}')
echo "📈 Memory Usage: ${MEM_USAGE} MB"

# CPU usage
CPU_USAGE=$(ps aux | grep "server:app" | grep -v grep | awk '{sum+=$3} END {print sum}')
echo "⚡ CPU Usage: ${CPU_USAGE}%"

# Active connections (if netstat available)
if command -v netstat &> /dev/null; then
    CONNECTIONS=$(netstat -an | grep ":8001" | grep ESTABLISHED | wc -l)
    echo "🔌 Active Connections: $CONNECTIONS"
fi

echo ""
echo "Last check: $(date)"
```

**Setup Cron Monitoring** (check every 5 minutes):

```bash
chmod +x /usr/local/bin/butterfly_monitor.sh

crontab -e
# Add:
*/5 * * * * /usr/local/bin/butterfly_monitor.sh >> /var/log/butterfly_monitor.log 2>&1
```

---

## 🌐 Production Deployment

### Reverse Proxy with Nginx

**Install Nginx**:
```bash
sudo apt-get install nginx
```

**Configure Nginx** (`/etc/nginx/sites-available/butterfly-api`):

```nginx
upstream butterfly_api {
    server 127.0.0.1:8001;
}

server {
    listen 80;
    server_name api.yourdomain.com;

    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;

    # Client body size limit
    client_max_body_size 10M;

    # Proxy settings
    location /api/ {
        proxy_pass http://butterfly_api;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # Timeouts
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }

    # Health check endpoint
    location /health {
        proxy_pass http://butterfly_api/api/;
        access_log off;
    }
}
```

**Enable and Test**:

```bash
# Enable site
sudo ln -s /etc/nginx/sites-available/butterfly-api /etc/nginx/sites-enabled/

# Test configuration
sudo nginx -t

# Restart nginx
sudo systemctl restart nginx

# Test through nginx
curl http://localhost/api/
```

### SSL/TLS with Let's Encrypt

```bash
# Install certbot
sudo apt-get install certbot python3-certbot-nginx

# Get certificate
sudo certbot --nginx -d api.yourdomain.com

# Auto-renewal (certbot does this automatically)
sudo certbot renew --dry-run
```

### Environment Variables for Production

```bash
# /app/backend/.env (Production)
MYSQL_HOST=db.production.com
MYSQL_PORT=3306
MYSQL_DATABASE=butterfly_app
MYSQL_USER=butterfly_user
MYSQL_PASSWORD=complex_secure_password_here

# Environment
ENVIRONMENT=production

# Workers (2-4 per CPU core)
WORKERS=4

# Logging
LOG_LEVEL=INFO

# Security
ALLOWED_HOSTS=api.yourdomain.com

# Connection Pool
DB_POOL_MIN_SIZE=2
DB_POOL_MAX_SIZE=20
```

---

## 🐛 Troubleshooting

### Application Won't Start

```bash
# Check Python version
python3 --version

# Check dependencies
pip list | grep -E "fastapi|uvicorn|aiomysql"

# Test imports manually
python3 -c "import fastapi, uvicorn, aiomysql; print('OK')"

# Check .env file exists
ls -l /app/backend/.env

# Test database connection
python3 /app/backend/test_connection.py

# Check if port is already in use
sudo netstat -tlnp | grep 8001
```

### Database Connection Errors

```bash
# Test MySQL connection from app server
mysql -h <DB_HOST> -u butterfly_user -p butterfly_app

# Test with telnet
telnet <DB_HOST> 3306

# Check firewall on DB server
sudo ufw status

# Check MySQL logs
sudo tail -f /var/log/mysql/error.log

# Verify user permissions
mysql -u root -p -e "SHOW GRANTS FOR 'butterfly_user'@'%';"
```

### API Returns 500 Errors

```bash
# Check application logs
sudo journalctl -u butterfly-api -n 50

# Check for database errors
tail -50 /var/log/butterfly_error.log

# Test database queries manually
mysql -h <DB_HOST> -u butterfly_user -p butterfly_app -e "SELECT COUNT(*) FROM butterflies;"

# Check connection pool
# Add debug logging to server.py temporarily
```

### High Memory Usage

```bash
# Check memory usage
ps aux | grep python | awk '{sum+=$6} END {print "Total Memory: " sum/1024 " MB"}'

# Reduce workers
# In systemd service or command line: --workers 2

# Monitor memory over time
watch -n 5 'ps aux | grep python'

# Restart application
sudo systemctl restart butterfly-api
```

---

## 📚 Quick Reference

### Start/Stop Commands

```bash
# Systemd
sudo systemctl start butterfly-api
sudo systemctl stop butterfly-api
sudo systemctl restart butterfly-api
sudo systemctl status butterfly-api

# Manual (background)
cd /app/backend
nohup uvicorn server:app --host 0.0.0.0 --port 8001 &

# Stop manual process
pkill -f "server:app"
```

### Log Commands

```bash
# View logs
sudo journalctl -u butterfly-api -f

# Search logs
sudo journalctl -u butterfly-api | grep "ERROR"

# Clear old logs
sudo journalctl --vacuum-time=7d
```

### Health Check

```bash
# Quick check
curl http://localhost:8001/api/

# Full health check
./health_check.sh

# Monitor
./butterfly_monitor.sh
```

---

## ✅ Post-Deployment Checklist

- [ ] Python 3.8+ installed
- [ ] Dependencies installed from requirements.txt
- [ ] .env file configured with MySQL credentials
- [ ] Database connection tested successfully
- [ ] Application starts without errors
- [ ] All API endpoints return expected results
- [ ] Process manager configured (systemd/supervisor)
- [ ] Application auto-starts on boot
- [ ] Logs are accessible and monitored
- [ ] Health checks passing
- [ ] Nginx reverse proxy configured (production)
- [ ] SSL/TLS certificate installed (production)
- [ ] Firewall configured
- [ ] Monitoring in place
- [ ] Backup procedures tested

---

**Application is ready for production!** 🚀

For database management, see the files in `/app/database/`
