from sqlalchemy import create_engine, Column, Integer, String, Date, Sequence
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import date

# Define the base class
Base = declarative_base()

# Define the PostgreSQL model
class PostgresPerson(Base):
    __tablename__ = 'mock_sql_table'
    person_id = Column(Integer, Sequence('person_id_seq'), primary_key=True)
    first_name = Column(String(50))
    last_name = Column(String(50))
    email = Column(String(50))
    ip_address = Column(String(20))
    last_updated = Column(Date)

# Database connection string
postgres_connection_string = 'postgresql+psycopg2://postgres:mysecretpassword@localhost:5432/postgres'

# Create engine
engine = create_engine(postgres_connection_string)

# Create the table
Base.metadata.create_all(engine)

# Create a session
Session = sessionmaker(bind=engine)
session = Session()

# Dummy data
dummy_data = [
    PostgresPerson(first_name='John', last_name='Doe', email='john.doe@example.com', ip_address='192.168.1.1', last_updated=date(2025, 1, 1)),
    PostgresPerson(first_name='Jane', last_name='Smith', email='jane.smith@example.com', ip_address='192.168.1.2', last_updated=date(2025, 1, 2)),
    PostgresPerson(first_name='Alice', last_name='Johnson', email='alice.johnson@example.com', ip_address='192.168.1.3', last_updated=date(2025, 1, 3)),
    PostgresPerson(first_name='Bob', last_name='Brown', email='bob.brown@example.com', ip_address='192.168.1.4', last_updated=date(2025, 1, 4)),
    PostgresPerson(first_name='Charlie', last_name='Davis', email='charlie.davis@example.com', ip_address='192.168.1.5', last_updated=date(2025, 1, 5))
]

# Insert dummy data
session.add_all(dummy_data)
session.commit()

# Close the session
session.close()

print("Data inserted successfully!")

