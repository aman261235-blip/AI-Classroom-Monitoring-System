from app.src.database import get_connection, close_connection

# Connect to MySQL
connection = get_connection()

if connection:
    cursor = connection.cursor()

    # Check which database is selected
    cursor.execute("SELECT DATABASE();")

    result = cursor.fetchone()

    print("Current Database:", result)

    cursor.close()

    close_connection(connection)

else:
    print("Database connection failed.")