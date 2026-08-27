import psycopg2



try:

    conn=psycopg2.connect(
        dbname="todo_db",
        user="prabhat",
        password="centralexchange_123",
        host="localhost"

    )
    print("connected succesfully")

    cursor = conn.cursor()
    cursor.execute("SELECT current_database(), current_user;")

    result = cursor.fetchone()
    print("Database:", result[0])
    print("User:", result[1])

    cursor.close()
    conn.close()


except Exception as e:
    print("Connection failed ",e)


