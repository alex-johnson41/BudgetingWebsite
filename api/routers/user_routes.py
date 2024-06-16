from fastapi import APIRouter, Depends
from sqlmodel import Session

from api.services.user_service import UserService
from api.dependencies import get_session
from api.models.user import User

router = APIRouter(
    prefix="/user",
    responses={404: {"description": "Not found"}},
)


@router.post("/")
def create_user(user: User, session: Session = Depends(get_session)):
    _service = UserService(session)
    return _service.create(user)


@router.get("/{id}")
def get_user(id: int, session: Session = Depends(get_session)):
    _service = UserService(session)
    return _service.get_user(id)
