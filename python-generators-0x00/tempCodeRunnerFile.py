def insert_data(connection, csv_file):
    """Insert data from user_data.csv if not already present"""
    try:
        cursor = connection.cursor()
        with open(csv_file, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                user_id = row.get("user_id") or str(uuid.uuid4())
                name = row["name"]
                email = row["email"]
                age = row["age"]
                cursor.execute('''
                    INSERT IGNORE INTO user_data (user_id, name, email, age)
                    VALUES (%s, %s, %s, %s)
                ''', (user_id, name, email, age))
        connection.commit()
        print("Data inserted successfully")
        cursor.close()
    except FileNotFoundError:
        print(f"CSV file '{csv_file}' not found.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
