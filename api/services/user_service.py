from fastapi import HTTPException
from sqlmodel import Session
from api.models import UserCreate, UserPublic
from api.repositories.user_repository import UserRepository


class UserService:

    def __init__(self, session: Session) -> None:
        self.repository = UserRepository(session)

    def get_user(self, id: int) -> UserPublic:
        user = self.repository.get_user(id)
        if user is None:
            raise HTTPException(
                status_code=404, detail="User not found")
        return user

    def get_all(self) -> list[UserPublic]:
        return self.repository.get_all()

    def create(self, user: UserCreate) -> UserPublic:
        return self.repository.create(user)

    def delete(self, user_id: int) -> UserPublic:
        user = self.repository.delete(user_id)
        if user is None:
            raise HTTPException(
                status_code=404, detail="User not found")
        return user
