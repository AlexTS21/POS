import sqlite3

# Connect to or create the database
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Create table if not exists
cursor.execute('''
CREATE TABLE IF NOT EXISTS corte (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    total REAL NOT NULL,
    user TEXT NOT NULL,
    date TEXT NOT NULL DEFAULT (datetime('now', 'localtime')),
    active INTEGER NOT NULL CHECK(active IN (0, 1))
);
''')


# Commit changes and close connection
conn.commit()
conn.close()

print("✅ Table 'corte' created successfully.")