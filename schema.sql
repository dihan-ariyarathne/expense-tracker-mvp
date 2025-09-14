-- Users table
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL CHECK(length(name) >= 1 AND length(name) <= 80),
    age INTEGER NOT NULL CHECK(age >= 13),
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Transactions table
CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    t_type TEXT NOT NULL CHECK(t_type IN ('income', 'expense')),
    category TEXT NOT NULL,
    amount NUMERIC NOT NULL CHECK(amount > 0),
    note TEXT,
    ts DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
);

-- Indexes for better performance
CREATE INDEX IF NOT EXISTS idx_tx_user_ts ON transactions (user_id, ts DESC);
CREATE INDEX IF NOT EXISTS idx_tx_user_type ON transactions (user_id, t_type);
CREATE INDEX IF NOT EXISTS idx_tx_user_category ON transactions (user_id, category);
CREATE INDEX IF NOT EXISTS idx_tx_user_date ON transactions (user_id, DATE(ts));
