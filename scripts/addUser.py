import sqlite3

# Connect to or create the database
conn = sqlite3.connect('database.db')
cursor = conn.cursor()



# Insert admin user (if not exists)
cursor.execute('''
INSERT OR IGNORE INTO users (username, password, fullname, phone, type, active)
VALUES (?, ?, ?, ?, ?, ?)
''', ('cuit', '1234', 'Cuitlahuac Tejeda', '5551234567', 1, 1))

# Commit changes and close connection
conn.commit()
conn.close()

print("✅ Table 'users' created successfully.")