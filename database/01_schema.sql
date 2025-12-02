-- ============================================
-- Butterfly Identification App - Database Schema
-- Database: MySQL/MariaDB 5.7+
-- ============================================

-- Create Database
CREATE DATABASE IF NOT EXISTS butterfly_app
  DEFAULT CHARACTER SET utf8mb4
  DEFAULT COLLATE utf8mb4_unicode_ci;

USE butterfly_app;

-- ============================================
-- Table: butterflies
-- Stores all butterfly species information
-- ============================================
CREATE TABLE IF NOT EXISTS butterflies (
    id INT AUTO_INCREMENT PRIMARY KEY,
    commonName VARCHAR(255) NOT NULL,
    latinName VARCHAR(255) NOT NULL,
    imageUrl TEXT NOT NULL,
    difficulty INT NOT NULL DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    -- Constraints
    CONSTRAINT chk_difficulty CHECK (difficulty IN (1, 2, 3)),
    
    -- Indexes
    INDEX idx_difficulty (difficulty),
    INDEX idx_commonName (commonName),
    INDEX idx_latinName (latinName)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================
-- Table: scores
-- Stores user game scores and history
-- ============================================
CREATE TABLE IF NOT EXISTS scores (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    score INT NOT NULL,
    total INT NOT NULL,
    difficulty INT NOT NULL,
    percentage INT NOT NULL,
    date DATETIME NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Constraints
    CONSTRAINT chk_score_difficulty CHECK (difficulty IN (1, 2, 3)),
    CONSTRAINT chk_score_range CHECK (score >= 0 AND score <= total),
    CONSTRAINT chk_percentage_range CHECK (percentage >= 0 AND percentage <= 100),
    
    -- Indexes
    INDEX idx_username (username),
    INDEX idx_date (date),
    INDEX idx_difficulty_score (difficulty, percentage DESC),
    INDEX idx_username_date (username, date DESC)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================
-- Add comments to tables and columns
-- ============================================
ALTER TABLE butterflies COMMENT = 'Stores butterfly species data for the identification game';
ALTER TABLE scores COMMENT = 'Stores user game scores and statistics';
