from sqlmodel import SQLModel, create_engine


file_name = "api/database/database.db"
sqlite_url = f"sqlite:///{file_name}"
engine = create_engine(sqlite_url)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
