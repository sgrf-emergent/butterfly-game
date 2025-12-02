-- ============================================
-- Butterfly Identification App - User & Permissions Setup
-- Create application user with appropriate permissions
-- ============================================

-- ============================================
-- 1. Create Application User
-- ============================================

-- Create user for the application (change password in production!)
CREATE USER IF NOT EXISTS 'butterfly_user'@'%' IDENTIFIED BY 'butterfly_password_2024';

-- For specific host/IP (recommended for production)
-- CREATE USER IF NOT EXISTS 'butterfly_user'@'192.168.1.100' IDENTIFIED BY 'butterfly_password_2024';

-- ============================================
-- 2. Grant Permissions
-- ============================================

-- Grant all privileges on butterfly_app database
GRANT ALL PRIVILEGES ON butterfly_app.* TO 'butterfly_user'@'%';

-- Or grant specific permissions (more secure - recommended for production)
-- GRANT SELECT, INSERT, UPDATE, DELETE ON butterfly_app.* TO 'butterfly_user'@'%';

-- ============================================
-- 3. Create Read-Only User (for reporting/analytics)
-- ============================================

CREATE USER IF NOT EXISTS 'butterfly_readonly'@'%' IDENTIFIED BY 'readonly_password_2024';
GRANT SELECT ON butterfly_app.* TO 'butterfly_readonly'@'%';

-- ============================================
-- 4. Apply Changes
-- ============================================

FLUSH PRIVILEGES;

-- ============================================
-- 5. Verify Users and Permissions
-- ============================================

SELECT User, Host FROM mysql.user WHERE User LIKE 'butterfly%';

SHOW GRANTS FOR 'butterfly_user'@'%';
SHOW GRANTS FOR 'butterfly_readonly'@'%';

-- ============================================
-- SECURITY NOTES:
-- ============================================
-- 1. Change default passwords immediately in production
-- 2. Use '%' for wildcard host access, or specify exact IPs for better security
-- 3. Consider using SSL/TLS for MySQL connections
-- 4. Regularly rotate passwords
-- 5. Use environment variables to store credentials, never hardcode
-- 6. Enable MySQL audit logging for production environments
-- ============================================
