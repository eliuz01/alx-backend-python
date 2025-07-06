import mysql.connector

def stream_users_in_batches(batch_size):
    """Generator to stream users in batches"""
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="E#koyi@2025",
            database="ALX_prodev"
        )
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM user_data;")
        
        while True:
            batch = cursor.fetchmany(batch_size)
            if not batch:
                break
            yield batch
        
        cursor.close()
        connection.close()
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return

def batch_processing(batch_size):
    """Processes each batch, yielding users over age 25"""
    for batch in stream_users_in_batches(batch_size):
        for user in batch:
            if user['age'] > 25:
                yield user
