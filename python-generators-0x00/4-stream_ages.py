import seed

def stream_user_ages():
    """Generator that yields user ages one by one"""
    try:
        connection = seed.connect_to_prodev()
        cursor = connection.cursor()
        cursor.execute("SELECT age FROM user_data")
        for row in cursor:  #Loop 1
            yield row[0]  # age is the first and only column in SELECT
        cursor.close()
        connection.close()
    except Exception as e:
        print(f"Error: {e}")
        return

def calculate_average_age():
    """Uses the generator to compute average age efficiently"""
    total = 0
    count = 0
    for age in stream_user_ages():  #Loop 2
        total += float(age)
        count += 1
    if count > 0:
        avg = total / count
        print(f"Average age of users: {avg:.2f}")
    else:
        print("No users in the database.")


if __name__ == "__main__":
    calculate_average_age()
