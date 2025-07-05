import mysql.connector
import csv
import os
import uuid

def connect_db():
    """Connect to MySQL server (without specifying a DB)"""
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="E#koyi@2025"  
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

def create_database(connection):
    """Create the ALX_prodev database if it doesn't exist"""
    try:
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev;")
        print("Database ALX_prodev checked/created successfully")
        cursor.close()
    except mysql.connector.Error as err:
        print(f"Error: {err}")

def connect_to_prodev():
    """Connect directly to ALX_prodev database"""
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="E#koyi@2025",  
            database="ALX_prodev"
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

def create_table(connection):
    """Create user_data table if not exists"""
    try:
        cursor = connection.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_data (
                user_id VARCHAR(36) PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL,
                age DECIMAL NOT NULL,
                INDEX(user_id)
            );
        ''')
        connection.commit()
        print("Table user_data created successfully")
        cursor.close()
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    
def insert_data(connection, csv_file):
    """Insert data into user_data table from CSV without user_id column"""
    try:
        cursor = connection.cursor()
        print(f"Opening file: {os.path.abspath(csv_file)}")  # NEW
        with open(csv_file, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            rows_inserted = 0
            for row in reader:
                try:
                    user_id = str(uuid.uuid4())  # Generate new UUID
                    name = row["name"]
                    email = row["email"]
                    age = row["age"]
                    cursor.execute('''
                        INSERT INTO user_data (user_id, name, email, age)
                        VALUES (%s, %s, %s, %s)
                    ''', (user_id, name, email, age))
                    rows_inserted += 1
                except Exception as row_error:
                    print(f"Error on row {row}: {row_error}")
            connection.commit()
            print(f"✅ Inserted {rows_inserted} rows successfully.")  # NEW
            cursor.close()
    except Exception as e:
        print(f"Error inserting data: {e}")

if __name__ == "__main__":
    connection = connect_db()
    if connection:
        create_database(connection)
        connection.close()
        print("Initial connection successful.")

        connection = connect_to_prodev()
        if connection:
            create_table(connection)
            insert_data(connection, 'user_data.csv')  # <--- important!
            connection.close()

def stream_user_data(connection):
    """Generator that yields one row at a time from user_data"""
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM user_data;")
        while True:
            row = cursor.fetchone()
            if row is None:
                break
            yield row
        cursor.close()
    except mysql.connector.Error as err:
        print(f"Error streaming data: {err}")
