from sqlmodel import Session

from api.models.user import User
from api.repositories.user_repository import UserRepository


class UserService:
    def __init__(self, session: Session):
        self.user_reposity = UserRepository(session)

    def get_user(self, id: int) -> User:
        return self.user_reposity.get_user(id)

    def create(self, user: User) -> User:
        return self.user_reposity.create(user)
