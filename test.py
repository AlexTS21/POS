import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

cursor.execute("DROP TABLE IF EXISTS inventory")  # Borra toda la tabla
conn.commit()
conn.close()
