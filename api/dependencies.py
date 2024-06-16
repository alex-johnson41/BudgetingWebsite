from sqlmodel import Session

from api.database.database import engine


def get_session():
    with Session(engine) as session:
        yield session
