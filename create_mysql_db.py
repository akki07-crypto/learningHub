import pymysql

try:
    # Connect to MySQL Server without specifying DB
    connection = pymysql.connect(
        host='127.0.0.1',
        user='root',
        password='akash94655',
        port=3306
    )
    cursor = connection.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS elearn_db CHARACTER SET utf8mb4;")
    print("[SUCCESS] MySQL Database 'elearn_db' created or already exists!")
    cursor.close()
    connection.close()
except Exception as e:
    print(f"[ERROR] Could not connect to MySQL: {e}")
