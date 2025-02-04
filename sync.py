from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()

# Oracle model
class OraclePerson(Base):
    __tablename__ = 'mock_oracle_table'
    PER_ID = Column(Integer, primary_key=True)
    F_NM = Column(String(50))
    L_NM = Column(String(50))
    EM = Column(String(50))
    IP = Column(String(20))
    LST_UPD = Column(Date)

# PER_ID  # person_id
# F_NM  # first_name
# L_NM  # last_name
# EM  # email
# IP  # ip_address
# LST_UPD DATE  # last_update

# PostgreSQL model
class PostgresPerson(Base):
    __tablename__ = 'mock_sql_table'
    person_id = Column(Integer, primary_key=True)
    first_name = Column(String(50))
    last_name = Column(String(50))
    email = Column(String(50))
    ip_address = Column(String(20))
    last_updated = Column(Date)

# Database connection strings
oracle_connection_string = 'oracle+cx_oracle://system:password@localhost:1521/?service_name=FREEXDB'
postgres_connection_string = 'postgresql+psycopg2://postgres:mysecretpassword@localhost:5432/postgres'

# Create engines
oracle_engine = create_engine(oracle_connection_string)
postgres_engine = create_engine(postgres_connection_string)

# Create sessions
OracleSession = sessionmaker(bind=oracle_engine)
PostgresSession = sessionmaker(bind=postgres_engine)

def synchronize_data():
    oracle_session = OracleSession()
    postgres_session = PostgresSession()

    try:
        # Fetch data from Oracle
        oracle_data = oracle_session.query(OraclePerson).all()
        oracle_person_ids = [oracle_person.PER_ID for oracle_person in oracle_data]

        # Process in chunks of 500
        chunk_size = 500
        for i in range(0, len(oracle_person_ids), chunk_size):
            chunk = oracle_person_ids[i:i + chunk_size]
            postgres_people = postgres_session.query(PostgresPerson).filter(PostgresPerson.person_id.in_(chunk)).all()
            postgres_people_dict = {person.person_id: person for person in postgres_people}

            for oracle_person in oracle_data[i:i + chunk_size]:
                postgres_person = postgres_people_dict.get(oracle_person.PER_ID)

                if postgres_person:
                    # Update PostgreSQL if the Oracle record is newer
                    if oracle_person.LST_UPD > postgres_person.last_updated:
                        postgres_person.first_name = oracle_person.F_NM
                        postgres_person.last_name = oracle_person.L_NM
                        postgres_person.email = oracle_person.EM
                        postgres_person.ip_address = oracle_person.IP
                        postgres_person.last_updated = oracle_person.LST_UPD
                        postgres_session.add(postgres_person)
                else:
                    # Insert new record into PostgreSQL
                    new_postgres_person = PostgresPerson(
                        person_id=oracle_person.PER_ID,
                        first_name=oracle_person.F_NM,
                        last_name=oracle_person.L_NM,
                        email=oracle_person.EM,
                        ip_address=oracle_person.IP,
                        last_updated=oracle_person.LST_UPD
                    )
                    postgres_session.add(new_postgres_person)

        postgres_session.commit()

    except Exception as e:
        print(f"An error occurred: {e}")
        postgres_session.rollback()
    finally:
        oracle_session.close()
        postgres_session.close()

if __name__ == "__main__":
    synchronize_data()

