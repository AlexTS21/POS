import sqlite3

# Connect to or create the database
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Create table if not exists
cursor.execute('''
CREATE TABLE IF NOT EXISTS sales (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    total_price REAL NOT NULL,
    cash REAL NOT NULL,
    change REAL NOT NULL,
    total_products INTEGER NOT NULL, 
    user TEXT NOT NULL,
    date TEXT NOT NULL DEFAULT (datetime('now', 'localtime')),
    active INTEGER NOT NULL CHECK(active IN (0, 1))
);
''')


# Commit changes and close connection
conn.commit()
conn.close()

print("✅ Table 'sales' created successfully.")