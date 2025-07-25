import sqlite3

# Connect to or create the database
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Create table if not exists
#cursor.execute('''
#CREATE TABLE IF NOT EXISTS inventory (
#    id INTEGER PRIMARY KEY AUTOINCREMENT,
#    barcode TEXT UNIQUE NOT NULL,
#    product_name TEXT NOT NULL,
#    price REAL NOT NULL,
#    amount INTEGER NOT NULL, 
#    active INTEGER NOT NULL CHECK(active IN (0, 1))
#);
#''')

# Insert admin user (if not exists)
cursor.execute('''
INSERT OR IGNORE INTO inventory (barcode, product_name, price, amount, active)
VALUES (?, ?, ?, ?, ?)
''', ('456', 'goma', 4, 10, 1))

# Commit changes and close connection
conn.commit()
conn.close()

print("✅ Table 'inventory' created successfully.")