import mysql.connector

def create_tables():
    try:
        connection = mysql.connector.connect(
            host='127.0.0.1',
            user='root',
            password='Pavilion227',
            database='citibike'
        )
        cursor = connection.cursor()
        with open("db/db_schema.sql", "r") as f:
            schema_sql = f.read()
            for stmt in schema_sql.strip().split(';'):
                if stmt.strip():
                    cursor.execute(stmt)
        print("✅ Tables created successfully.")
    except mysql.connector.Error as err:
        print(f"❌ Error: {err}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

if __name__ == "__main__":
    create_tables()
