import sqlite3

conn = sqlite3.connect("app.db")

tables = conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
print("Tables:", tables)

cur = conn.execute("SELECT * FROM users LIMIT 3")
print("Columns:", cur.description)
print("Rows:", cur.fetchall())