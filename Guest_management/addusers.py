import sqlite3


username = 'yarden'
password = '1234'
email = 'example@example.com'

with sqlite3.connect("flask_useres.db") as conn:
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO flask_useres (username, password, email) VALUES (?, ?, ?)", 
        (username, password, email),
    )
