import sqlite3





with sqlite3.connect('people.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT id FROM people')
        myresulet = cursor.fetchall()
print(myresulet[-1][0])

