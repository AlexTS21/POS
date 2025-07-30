import sqlite3

# Connect to or create the database
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Create table if not exists
cursor.execute('''
CREATE TABLE IF NOT EXISTS salesDetail (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_sale INTEGER NOT NULL,
    product_name TEXT NOT NULL,
    price REAL NOT NULL,
    amount INTEGER NOT NULL,
    active INTEGER NOT NULL CHECK(active IN (0, 1))
);
''')
#cursor.execute("DELETE FROM salesDetail;")

# Commit changes and close connection
conn.commit()
conn.close()

print("✅ Table 'salesDetail' created successfully.")