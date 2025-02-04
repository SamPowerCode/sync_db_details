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

    def __repr__(self):
        return f"person_id: {self.PER_ID}, fullname: {self.F_NM} {self.L_NM}, email: {self.EM}"

# PostgreSQL model
class PostgresPerson(Base):
    __tablename__ = 'mock_sql_table'
    person_id = Column(Integer, primary_key=True)
    first_name = Column(String(50))
    last_name = Column(String(50))
    email = Column(String(50))
    ip_address = Column(String(20))
    last_updated = Column(Date)

    def __repr__(self):
        return f"person_id: {self.person_id}, fullname: {self.first_name} {self.last_name}, email: {self.email}"

# Database connection strings
oracle_connection_string = 'oracle+cx_oracle://system:password@localhost:1521/?service_name=FREEXDB'
postgres_connection_string = 'postgresql+psycopg2://postgres:mysecretpassword@localhost:5432/postgres'

# Create engines
oracle_engine = create_engine(oracle_connection_string)
postgres_engine = create_engine(postgres_connection_string)

# Create sessions
OracleSession = sessionmaker(bind=oracle_engine)
PostgresSession = sessionmaker(bind=postgres_engine)


if __name__ == "__main__":
    oracle_session = OracleSession()
    postgres_session = PostgresSession()
    # print(PostgresSession.query(PostgresPerson).all())
    print('----------   POST    ----------')
    for post_person in postgres_session.query(PostgresPerson).all():
        print(post_person)
    print()
    print('----------   ORAC    ----------')
    for orac_person in oracle_session.query(OraclePerson).all():
        print(post_person)
