#!/bin/bash

# ============================================
# Butterfly Identification App
# Database Backup and Restore Scripts
# ============================================

# Configuration
DB_NAME="butterfly_app"
DB_USER="root"
DB_PASSWORD="your_password_here"
DB_HOST="localhost"
DB_PORT="3306"
BACKUP_DIR="/var/backups/mysql/butterfly_app"
DATE=$(date +%Y%m%d_%H%M%S)

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# ============================================
# Function: Create Full Backup
# ============================================
backup_database() {
    echo -e "${YELLOW}Creating database backup...${NC}"
    
    # Create backup directory if it doesn't exist
    mkdir -p "$BACKUP_DIR"
    
    # Backup filename
    BACKUP_FILE="$BACKUP_DIR/butterfly_app_backup_$DATE.sql"
    
    # Create backup with compression
    mysqldump -h "$DB_HOST" \
              -P "$DB_PORT" \
              -u "$DB_USER" \
              -p"$DB_PASSWORD" \
              --databases "$DB_NAME" \
              --single-transaction \
              --routines \
              --triggers \
              --events \
              --set-gtid-purged=OFF \
              | gzip > "$BACKUP_FILE.gz"
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ Backup created successfully: $BACKUP_FILE.gz${NC}"
        echo -e "${GREEN}  Size: $(du -h "$BACKUP_FILE.gz" | cut -f1)${NC}"
    else
        echo -e "${RED}✗ Backup failed!${NC}"
        exit 1
    fi
}

# ============================================
# Function: Create Data-Only Backup
# ============================================
backup_data_only() {
    echo -e "${YELLOW}Creating data-only backup...${NC}"
    
    mkdir -p "$BACKUP_DIR"
    BACKUP_FILE="$BACKUP_DIR/butterfly_app_data_$DATE.sql"
    
    mysqldump -h "$DB_HOST" \
              -P "$DB_PORT" \
              -u "$DB_USER" \
              -p"$DB_PASSWORD" \
              --no-create-info \
              --skip-triggers \
              "$DB_NAME" \
              | gzip > "$BACKUP_FILE.gz"
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ Data backup created: $BACKUP_FILE.gz${NC}"
    else
        echo -e "${RED}✗ Data backup failed!${NC}"
        exit 1
    fi
}

# ============================================
# Function: Create Schema-Only Backup
# ============================================
backup_schema_only() {
    echo -e "${YELLOW}Creating schema-only backup...${NC}"
    
    mkdir -p "$BACKUP_DIR"
    BACKUP_FILE="$BACKUP_DIR/butterfly_app_schema_$DATE.sql"
    
    mysqldump -h "$DB_HOST" \
              -P "$DB_PORT" \
              -u "$DB_USER" \
              -p"$DB_PASSWORD" \
              --no-data \
              "$DB_NAME" \
              > "$BACKUP_FILE"
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ Schema backup created: $BACKUP_FILE${NC}"
    else
        echo -e "${RED}✗ Schema backup failed!${NC}"
        exit 1
    fi
}

# ============================================
# Function: Restore Database
# ============================================
restore_database() {
    if [ -z "$1" ]; then
        echo -e "${RED}✗ Please provide backup file path${NC}"
        echo "Usage: $0 restore <backup_file.sql.gz>"
        exit 1
    fi
    
    RESTORE_FILE="$1"
    
    if [ ! -f "$RESTORE_FILE" ]; then
        echo -e "${RED}✗ Backup file not found: $RESTORE_FILE${NC}"
        exit 1
    fi
    
    echo -e "${YELLOW}Restoring database from: $RESTORE_FILE${NC}"
    echo -e "${RED}WARNING: This will overwrite existing data!${NC}"
    read -p "Are you sure? (yes/no): " confirm
    
    if [ "$confirm" != "yes" ]; then
        echo "Restore cancelled."
        exit 0
    fi
    
    # Restore based on file extension
    if [[ "$RESTORE_FILE" == *.gz ]]; then
        gunzip < "$RESTORE_FILE" | mysql -h "$DB_HOST" \
                                         -P "$DB_PORT" \
                                         -u "$DB_USER" \
                                         -p"$DB_PASSWORD"
    else
        mysql -h "$DB_HOST" \
              -P "$DB_PORT" \
              -u "$DB_USER" \
              -p"$DB_PASSWORD" \
              < "$RESTORE_FILE"
    fi
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ Database restored successfully${NC}"
    else
        echo -e "${RED}✗ Restore failed!${NC}"
        exit 1
    fi
}

# ============================================
# Function: List Backups
# ============================================
list_backups() {
    echo -e "${YELLOW}Available backups in $BACKUP_DIR:${NC}"
    
    if [ ! -d "$BACKUP_DIR" ]; then
        echo -e "${RED}No backup directory found${NC}"
        exit 1
    fi
    
    ls -lh "$BACKUP_DIR" | grep butterfly_app
}

# ============================================
# Function: Clean Old Backups
# ============================================
clean_old_backups() {
    DAYS=${1:-30}  # Default: keep backups for 30 days
    
    echo -e "${YELLOW}Cleaning backups older than $DAYS days...${NC}"
    
    find "$BACKUP_DIR" -name "butterfly_app_*.sql.gz" -mtime +$DAYS -delete
    
    echo -e "${GREEN}✓ Old backups cleaned${NC}"
}

# ============================================
# Function: Export to CSV
# ============================================
export_to_csv() {
    echo -e "${YELLOW}Exporting tables to CSV...${NC}"
    
    CSV_DIR="$BACKUP_DIR/csv_exports_$DATE"
    mkdir -p "$CSV_DIR"
    
    # Export butterflies table
    mysql -h "$DB_HOST" \
          -P "$DB_PORT" \
          -u "$DB_USER" \
          -p"$DB_PASSWORD" \
          -e "SELECT * FROM butterflies" \
          "$DB_NAME" \
          | sed 's/\t/","/g;s/^/"/;s/$/"/;s/\n//g' > "$CSV_DIR/butterflies.csv"
    
    # Export scores table
    mysql -h "$DB_HOST" \
          -P "$DB_PORT" \
          -u "$DB_USER" \
          -p"$DB_PASSWORD" \
          -e "SELECT * FROM scores" \
          "$DB_NAME" \
          | sed 's/\t/","/g;s/^/"/;s/$/"/;s/\n//g' > "$CSV_DIR/scores.csv"
    
    echo -e "${GREEN}✓ CSV exports created in: $CSV_DIR${NC}"
}

# ============================================
# Main Script Logic
# ============================================

case "$1" in
    backup|full)
        backup_database
        ;;
    data)
        backup_data_only
        ;;
    schema)
        backup_schema_only
        ;;
    restore)
        restore_database "$2"
        ;;
    list)
        list_backups
        ;;
    clean)
        clean_old_backups "$2"
        ;;
    csv)
        export_to_csv
        ;;
    *)
        echo "Butterfly App Database Backup/Restore Tool"
        echo ""
        echo "Usage: $0 {backup|data|schema|restore|list|clean|csv}"
        echo ""
        echo "Commands:"
        echo "  backup     - Create full database backup (schema + data)"
        echo "  data       - Create data-only backup"
        echo "  schema     - Create schema-only backup"
        echo "  restore    - Restore from backup file"
        echo "  list       - List available backups"
        echo "  clean      - Clean backups older than N days (default: 30)"
        echo "  csv        - Export tables to CSV files"
        echo ""
        echo "Examples:"
        echo "  $0 backup"
        echo "  $0 restore /var/backups/mysql/butterfly_app/butterfly_app_backup_20241202.sql.gz"
        echo "  $0 clean 7"
        echo ""
        exit 1
        ;;
esac

exit 0
