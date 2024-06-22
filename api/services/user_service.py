from sqlmodel import Session
from api.models import UserCreate, UserPublic
from api.repositories.user_repository import UserRepository


class UserService:

    def __init__(self, session: Session) -> None:
        self.repository = UserRepository(session)

    def get_user(self, id: int) -> UserPublic:
        return self.repository.get_user(id)

    def create(self, user: UserCreate) -> UserPublic:
        return self.repository.create(user)
