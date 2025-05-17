import csv
import mysql.connector
from datetime import datetime

def insert_data(csv_file):
    try:
        connection = mysql.connector.connect(
            host='127.0.0.1',
            user='root',
            password='Pavilion227',
            database='citibike'
        )
        cursor = connection.cursor()

        with open(csv_file, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                cursor.execute("""
                    INSERT INTO station_status (
                        timestamp, station_name, station_id, longitude,
                        latitude, capacity, bikes_available, percent_filled, percent_empty
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (
                    row['timestamp'],
                    row['station_name'],
                    row['station_id'],
                    float(row['longitude']),
                    float(row['latitude']),
                    int(row['capacity']),
                    int(row['bikes_available']),
                    float(row['percent_filled']),
                    float(row['percent_empty']),
                ))
        connection.commit()
        print("✅ Data inserted successfully.")
    except mysql.connector.Error as err:
        print(f"❌ Error: {err}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

if __name__ == "__main__":
    insert_data("data/parsed_station_data.csv")  # Update path if needed
