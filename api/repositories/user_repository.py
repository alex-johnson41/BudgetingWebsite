from sqlmodel import Session, select

from api.models.user import User


class UserRepository:

    def __init__(self, session: Session):
        self.session = session

    def get_user(self, id: int) -> User:
        return self.session.exec(select(User).where(User.id == id)).all()

    def create(self, user: User) -> User:
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user
