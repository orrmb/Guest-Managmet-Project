import sqlite3
        
with sqlite3.connect('people.db') as conn:
        cursor = conn.cursor()
    
        # Fetch all the number of guests and sum them up
        cursor.execute('SELECT number_guests FROM people')
        myresulet = cursor.fetchall()
        total_guest = sum(i[0] for i in myresulet)
    
        # Fetch the number of guests where side is 'כלה' and relationship is 'משפחה קרובה'
        cursor.execute("SELECT number_guests FROM people WHERE side = 'כלה' AND relationship = 'משפחה קרובה'")
        filtered_result = cursor.fetchall()
        bride_closeFamily = sum(i[0] for i in filtered_result)

        cursor.execute("SELECT number_guests FROM people WHERE side = 'חתן' AND relationship = 'משפחה קרובה'")
        filtered_result = cursor.fetchall()
        groom_closeFamily = sum(i[0] for i in filtered_result)
conn.close

print(total_guest)
print('{}:מוזמנים צד כלה משפחה קרובה'.format(bride_closeFamily))
print('{}:מוזמנים צד חתן משפחה קרובה'.format(groom_closeFamily))
