import os
import sqlite3

conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()
try:
    cursor.execute("SELECT id, username, date_joined FROM auth_user ORDER BY id DESC;")
    rows = cursor.fetchall()
    print("USERS FOUND IN DB.SQLITE3:")
    for r in rows:
        print(f"ID: {r[0]}, Username: {r[1]}, Date: {r[2]}")
except Exception as e:
    print(f"Error: {e}")
conn.close()
