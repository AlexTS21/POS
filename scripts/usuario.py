import sqlite3

# Connect to or create the database
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Create table if not exists
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    fullname TEXT,
    phone TEXT,
    type INTEGER NOT NULL CHECK(type IN (0, 1)),   
    active INTEGER NOT NULL CHECK(active IN (0, 1))
);
''')

# Insert admin user (if not exists)
cursor.execute('''
INSERT OR IGNORE INTO users (username, password, fullname, phone, type, active)
VALUES (?, ?, ?, ?, ?, ?)
''', ('admin', '1234', 'Alejandro Tejeda', '5551234567', 0, 1))

# Commit changes and close connection
conn.commit()
conn.close()

print("✅ Table 'users' created successfully.")