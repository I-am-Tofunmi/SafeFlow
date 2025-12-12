-- --------------------------------------------------------
-- SafeFlow Database Schema & Seed Data
-- Run this if you want to manually reset the database.
-- --------------------------------------------------------

-- 1. USERS TABLE
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    phone_number VARCHAR NOT NULL UNIQUE,
    full_name VARCHAR,
    hashed_password VARCHAR,
    trust_score INTEGER DEFAULT 300,
    is_active BOOLEAN DEFAULT 1
);

-- 2. TRANSACTIONS TABLE
CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    amount FLOAT,
    transaction_type VARCHAR, -- 'credit' or 'debit'
    status VARCHAR,           -- 'completed', 'flagged', 'pending'
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(user_id) REFERENCES users(id)
);

-- 3. CONTACTS TABLE (Beneficiaries)
CREATE TABLE IF NOT EXISTS contacts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    name VARCHAR,
    phone_number VARCHAR,
    is_trusted BOOLEAN DEFAULT 0,
    FOREIGN KEY(user_id) REFERENCES users(id)
);

-- 4. LESSONS TABLE (Education)
CREATE TABLE IF NOT EXISTS lessons (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR,
    content VARCHAR,
    language VARCHAR, -- 'english', 'pidgin'
    category VARCHAR, -- 'security', 'savings'
    xp_points INTEGER DEFAULT 10
);

-- 5. USER LESSONS (Tracking Progress)
CREATE TABLE IF NOT EXISTS user_lessons (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    lesson_id INTEGER,
    completed_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(user_id) REFERENCES users(id),
    FOREIGN KEY(lesson_id) REFERENCES lessons(id)
);

-- --------------------------------------------------------
-- SEED DATA (Demo Content)
-- --------------------------------------------------------

-- Insert a Demo User (Password is 'password123' hashed)
-- Note: In real usage, rely on the API to create users so passwords are hashed correctly.

-- Insert Standard Lessons (English & Pidgin)
INSERT INTO lessons (title, content, language, category, xp_points) VALUES 
('Spotting Fake Alerts', 'Always check your app balance. SMS can be fake.', 'english', 'security', 15),
('Why Save Small Small?', 'Saving 100 Naira daily adds up. Consistency is key.', 'english', 'savings', 10),
('No fall maga!', 'If person call you for OTP, cut call. Na thief.', 'pidgin', 'security', 15),
('Credit Score Power', 'Pay back quick to get bigger loans later.', 'pidgin', 'credit', 20);

-- --------------------------------------------------------
-- END OF FILE
-- --------------------------------------------------------