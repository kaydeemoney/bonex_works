-- Create database
CREATE DATABASE IF NOT EXISTS new_profit_vault;
USE new_profit_vault;

-- Users Table
CREATE TABLE user (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    mobile VARCHAR(20) NOT NULL,
    password_hash TEXT NOT NULL,
    transaction_pin_hash TEXT NOT NULL,
    registration_referral_id VARCHAR(100) UNIQUE,
    is_admin BOOLEAN DEFAULT FALSE,
    user_id INT UNIQUE,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    gender ENUM('Male', 'Female', 'Other'),
    country VARCHAR(50),
    state VARCHAR(50),
    profile_picture_id TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);



-- Wallet Settings (Admin-set USDT address)

CREATE TABLE wallet_settings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usdt_wallet_address TEXT NOT NULL,
	current_wallet_address TEXT NOT NULL,
	former_wallet_address TEXT NOT NULL,
	destination_wallet_address TEXT NOT NULL,
	user_id INT UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
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
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    
);

-- Deposit Requests
CREATE TABLE deposits (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    network VARCHAR(50),
    amount DECIMAL(20, 2),
    transaction_id VARCHAR(100),
    status ENUM('pending', 'approved', 'rejected') DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    
);

-- Withdrawal Requests
CREATE TABLE withdrawal (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    network VARCHAR(50),
    wallet_address TEXT,
    amount DECIMAL(20, 2),
    fee DECIMAL(20, 2) DEFAULT 0.00,
    status ENUM('pending', 'approved', 'rejected') DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
   
);

-- Referral Bonuses
CREATE TABLE Referral (
    id INT AUTO_INCREMENT PRIMARY KEY,
    referrer_id INT,
    referred_user_id INT,
    commission DECIMAL(20, 2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    
);

-- Transaction History (Unified log)
CREATE TABLE transaction (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    transaction_type ENUM('deposit', 'withdrawal', 'investment', 'referral'),
    amount DECIMAL(20, 2),
    reference_id INT,
    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE USER 'bonex1'@'localhost' IDENTIFIED BY 'bonexproject';

GRANT ALL PRIVILEGES ON new_profit_vault TO 'bonex1'@'localhost';

GRANT SELECT, INSERT, UPDATE, DELETE, DROP, CREATE ON `new_profit_vault`.* TO 'bonex1'@'localhost';
GRANT ALL PRIVILEGES ON `new_profit_vault`.* TO 'bonex1'@'localhost';
FLUSH PRIVILEGES;


FLUSH PRIVILEGES;


SHOW GRANTS FOR 'bonex1'@'localhost';
