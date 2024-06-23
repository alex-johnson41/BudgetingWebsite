from fastapi import APIRouter, Depends
from sqlmodel import Session

from api.services.user_service import UserService
from api.dependencies import get_session
from api.models import UserCreate, UserPublic

router = APIRouter(
    prefix="/user",
    responses={404: {"description": "Not found"}},
)


@router.get("/{id}", response_model=UserPublic)
def get_user(id: int, session: Session = Depends(get_session)) -> UserPublic:
    _service = UserService(session)
    return _service.get_user(id)


@router.get("/", response_model=list[UserPublic])
def get_all_users(session: Session = Depends(get_session)) -> list[UserPublic]:
    _service = UserService(session)
    return _service.get_all()


@router.post("/", response_model=UserPublic)
def create_user(user: UserCreate, session: Session = Depends(get_session)) -> UserPublic:
    _service = UserService(session)
    return _service.create(user)


@router.delete("/{id}", response_model=UserPublic)
def delete_user(id: int, session: Session = Depends(get_session)) -> UserPublic:
    _service = UserService(session)
    return _service.delete(id)
