from fastapi import APIRouter, Depends
from sqlmodel import Session

from api.services.category_service import CategoryService
from api.dependencies import get_session
from api.models import CategoryCreate, CategoryPublic, CategoryPublicTransactions, CategoryPublicUser, CategoryUpdate

router = APIRouter(
    prefix="/category",
    responses={404: {"description": "Not found"}},
)


@router.get("/user/{user_id}", response_model=list[CategoryPublic])
def get_all_categories(user_id: int, session: Session = Depends(get_session)):
    _service = CategoryService(session)
    return _service.get_all_categories(user_id)


@router.get("/{id}", response_model=CategoryPublicUser)
def get_category(id: int, session: Session = Depends(get_session)):
    _service = CategoryService(session)
    return _service.get_category(id)


@router.get("/{user_id}/filter", response_model=list[CategoryPublicUser])
def get_filtered_categories(user_id: int, name: str | None = None, income: bool | None = None, session: Session = Depends(get_session)):
    _service = CategoryService(session)
    return _service.get_filtered(user_id, {"name": name, "income": income})


@router.patch("/{id}", response_model=CategoryPublic)
def update_category(id: int, category: CategoryUpdate, session: Session = Depends(get_session)):
    _service = CategoryService(session)
    return _service.update(id, category)


@router.post("/", response_model=CategoryPublic)
def create_category(category: CategoryCreate, session: Session = Depends(get_session)):
    _service = CategoryService(session)
    return _service.create(category)


@router.delete("/{id}", response_model=CategoryPublic)
def delete_category(id: int, session: Session = Depends(get_session)):
    _service = CategoryService(session)
    return _service.delete(id)
