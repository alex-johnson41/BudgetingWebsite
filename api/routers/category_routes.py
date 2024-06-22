from fastapi import APIRouter, Depends
from sqlmodel import Session

from api.services.category_service import CategoryService
from api.dependencies import get_session
from api.models import Category

router = APIRouter(
    prefix="/category",
    responses={404: {"description": "Not found"}},
)


@router.get("/{user_id}")
def get_all_categories(user_id: int, session: Session = Depends(get_session)):
    _service = CategoryService(session)
    return _service.get_all_categories(user_id)


@router.get("/{user_id}/{category_name}")
def get_category_by_name(user_id: int, category_name: str, session: Session = Depends(get_session)):
    _service = CategoryService(session)
    return _service.get_category_by_name(user_id, category_name)


@router.get("/{user_id}/filter")
def get_filtered_categories(user_id: int, filters: dict, session: Session = Depends(get_session)):
    _service = CategoryService(session)
    return _service.get_filtered(user_id, filters)


@router.post("/")
def create_category(user: Category, session: Session = Depends(get_session)):
    _service = CategoryService(session)
    return _service.create(user)
