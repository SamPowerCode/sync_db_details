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

# PER_ID  # person_id
# F_NM  # first_name
# L_NM  # last_name
# EM  # email
# IP  # ip_address
# LST_UPD DATE  # last_update

create_table_query = """
CREATE TABLE mock_oracle_table (
    PER_ID INT PRIMARY KEY,
    F_NM VARCHAR2(50),
    L_NM VARCHAR2(50),
    EM VARCHAR2(50),
    IP VARCHAR2(20),
    LST_UPD DATE
)
"""
cursor.execute(create_table_query)

# Insert dummy records
insert_query = """
INSERT INTO mock_oracle_table (PER_ID, F_NM, L_NM, EM, IP, LST_UPD)
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
select_query = "SELECT * FROM mock_oracle_table"
cursor.execute(select_query)

# Fetch and print the results
for row in cursor.fetchall():
    print(row)

# Close the cursor and connection
cursor.close()
connection.close()

