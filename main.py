import cx_Oracle
import datetime

# Connection details
dsn = cx_Oracle.makedsn("localhost", 1521, service_name="FREEXDB")  # Adjust service_name if needed
username = "system"  # Default username for Oracle
password = "password"  # Password you set

# Connect to the Oracle database
connection = cx_Oracle.connect(user=username, password=password, dsn=dsn)
cursor = connection.cursor()

# Create table
create_table_query = """
CREATE TABLE person (
    person_id INT PRIMARY KEY,
    first_name VARCHAR2(50),
    last_name VARCHAR2(50),
    email VARCHAR2(50),
    ip_address VARCHAR2(20),
    last_updated DATE
)
"""
cursor.execute(create_table_query)

# Insert dummy records
insert_query = """
INSERT INTO person (person_id, first_name, last_name, email, ip_address, last_updated)
VALUES (:1, :2, :3, :4, :5, :6)
"""

records = [
    (1, 'John', 'Doe', 'john.doe@example.com', '192.168.1.1', datetime.datetime.now()),
    (2, 'Jane', 'Smith', 'jane.smith@example.com', '192.168.1.2', datetime.datetime.now()),
    (3, 'Alice', 'Johnson', 'alice.johnson@example.com', '192.168.1.3', datetime.datetime.now()),
    (4, 'Bob', 'Brown', 'bob.brown@example.com', '192.168.1.4', datetime.datetime.now()),
    (5, 'Charlie', 'Davis', 'charlie.davis@example.com', '192.168.1.5', datetime.datetime.now())
]

cursor.executemany(insert_query, records)

# Commit the transaction
connection.commit()

# Query the records
select_query = "SELECT * FROM person"
cursor.execute(select_query)

# Fetch and print the results
for row in cursor.fetchall():
    print(row)

# Close the cursor and connection
cursor.close()
connection.close()

