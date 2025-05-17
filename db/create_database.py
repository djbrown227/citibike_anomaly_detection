import mysql.connector

def create_database():
    try:
        connection = mysql.connector.connect(
            host='127.0.0.1',
            user='root',
            port=3306,
            password='Pavilion227'
        )
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS citibike;")
        print("✅ Database 'citibike' created or already exists.")
    except mysql.connector.Error as err:
        print(f"❌ Error: {err}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

if __name__ == "__main__":
    create_database()
