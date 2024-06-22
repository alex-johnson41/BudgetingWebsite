from sqlmodel import select

from api.models import User, UserCreate, UserPublic
from api.repositories.base_repository import BaseRepository


class UserRepository(BaseRepository):

    def get_user(self, id: int) -> UserPublic:
        return self.session.exec(select(User).where(User.id == id)).first()

    def create(self, user: UserCreate) -> User:
        new_user = User.model_validate(user)
        self.session.add(new_user)
        self.session.commit()
        self.session.refresh(new_user)
        return new_user
