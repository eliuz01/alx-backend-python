# alx-backend-python
# 0x00. Python - Generators

## Task 0: Getting Started with Python Generators

### Objective

To implement a Python generator that streams rows from a MySQL database one by one, demonstrating the use of generators to efficiently handle large datasets without loading everything into memory at once.

---

### Features Implemented

- **MySQL Connection Setup**
  - Connects to the MySQL server using `mysql.connector`.
  - Creates a database called `ALX_prodev` if it does not already exist.

- **Table Creation**
  - Creates a table `user_data` with the following fields:
    - `user_id` (UUID, Primary Key)
    - `name` (string)
    - `email` (string)
    - `age` (decimal)

- **CSV Data Insertion**
  - Parses a CSV file (`user_data.csv`) containing name, email, and age.
  - Generates a unique UUID for each user.
  - Inserts the data into the `user_data` table.

- **Data Streaming Generator**
  - A generator function `stream_user_data()` yields one row at a time from the `user_data` table.
  - Efficient for memory usage — especially with large datasets.

---

### Files

- `seed.py`: Contains all core functions:
  - `connect_db()`
  - `create_database()`
  - `connect_to_prodev()`
  - `create_table()`
  - `insert_data()`
  - `stream_user_data()` ← the main generator

- `user_data.csv`: Sample dataset containing user information (name, email, age).

- `0-main.py`: Sample test file that demonstrates how to use the generator to stream data row-by-row.

---

### Usage

To run the setup and test the generator:

```bash
python seed.py
