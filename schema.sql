-- Create database
CREATE DATABASE IF NOT EXISTS profit_vault;
USE profit_vault;

-- Users Table
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    mobile VARCHAR(20) NOT NULL,
    password_hash TEXT NOT NULL,
    transaction_pin_hash TEXT NOT NULL,
    referral_code VARCHAR(20) UNIQUE,
    referred_by VARCHAR(20),
    is_admin BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Profiles Table (1-to-1 with users)
CREATE TABLE profiles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT UNIQUE,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    gender ENUM('Male', 'Female', 'Other'),
    country VARCHAR(50),
    state VARCHAR(50),
    profile_picture TEXT,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Wallet Settings (Admin-set USDT address)
CREATE TABLE wallet_settings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usdt_wallet_address TEXT NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Investment Plans Table
CREATE TABLE investment_plans (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    min_amount DECIMAL(20, 2) NOT NULL,
    max_amount DECIMAL(20, 2) NOT NULL,
    period_in_days INT NOT NULL,
    monthly_roi DECIMAL(5, 2) NOT NULL,
    annual_roi DECIMAL(5, 2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- User Investments Table
CREATE TABLE user_investments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    plan_id INT,
    amount_invested DECIMAL(20, 2),
    profit_earned DECIMAL(20, 2) DEFAULT 0.00,
    start_date DATETIME,
    end_date DATETIME,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (plan_id) REFERENCES investment_plans(id)
);

-- Deposit Requests
CREATE TABLE deposits (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    network VARCHAR(50),
    amount DECIMAL(20, 2),
    transaction_id VARCHAR(100),
    status ENUM('pending', 'approved', 'rejected') DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Withdrawal Requests
CREATE TABLE withdrawals (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    network VARCHAR(50),
    wallet_address TEXT,
    amount DECIMAL(20, 2),
    fee DECIMAL(20, 2) DEFAULT 0.00,
    status ENUM('pending', 'approved', 'rejected') DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Referral Bonuses
CREATE TABLE referral_bonuses (
    id INT AUTO_INCREMENT PRIMARY KEY,
    referrer_id INT,
    referred_user_id INT,
    amount DECIMAL(20, 2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (referrer_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (referred_user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Transaction History (Unified log)
CREATE TABLE transactions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    type ENUM('deposit', 'withdrawal', 'investment', 'referral'),
    amount DECIMAL(20, 2),
    reference_id INT,
    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- JWT Token Blacklist
CREATE TABLE token_blacklist (
    id INT AUTO_INCREMENT PRIMARY KEY,
    jti VARCHAR(255) NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
