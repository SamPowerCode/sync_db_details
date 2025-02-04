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
        # Fetch data from PostgreSQL
        postgres_data = postgres_session.query(PostgresPerson).all()

        # Fetch corresponding data from Oracle
        for pg_person in postgres_data:
            oracle_person = oracle_session.query(OraclePerson).filter_by(person_id=pg_person.person_id).first()

            if oracle_person:
                # Update Oracle if the PostgreSQL record is newer
                if pg_person.last_updated > oracle_person.last_updated:
                    oracle_person.first_name = pg_person.first_name
                    oracle_person.last_name = pg_person.last_name
                    oracle_person.email = pg_person.email
                    oracle_person.ip_address = pg_person.ip_address
                    oracle_person.last_updated = pg_person.last_updated
                    oracle_session.add(oracle_person)
            else:
                # Insert new record into Oracle
                new_oracle_person = OraclePerson(
                    person_id=pg_person.person_id,
                    first_name=pg_person.first_name,
                    last_name=pg_person.last_name,
                    email=pg_person.email,
                    ip_address=pg_person.ip_address,
                    last_updated=pg_person.last_updated
                )
                oracle_session.add(new_oracle_person)

        oracle_session.commit()

    except Exception as e:
        print(f"An error occurred: {e}")
        oracle_session.rollback()
    finally:
        oracle_session.close()
        postgres_session.close()

if __name__ == "__main__":
    synchronize_data()

