from abc import ABC

from sqlmodel import Session


class BaseRepository(ABC):
    def __init__(self, session: Session):
        self.session = session
