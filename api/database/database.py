from sqlmodel import SQLModel, create_engine
from api import secrets

engine = create_engine(secrets.connection_string)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
