from fastapi import APIRouter, Depends
from sqlmodel import Session

from api.services.budget_service import BudgetService
from api.dependencies import get_session
from api.models import BudgetPublic, BudgetCreate, BudgetPublicCategory, BudgetUpdate

router = APIRouter(
    prefix="/budget",
    responses={404: {"description": "Not found"}},
)


@router.get("/user/{user_id}", response_model=list[BudgetPublicCategory])
def get_all_budgets(user_id: int, session: Session = Depends(get_session)):
    _service = BudgetService(session)
    return _service.get_all_budgets(user_id)


@router.get("/{id}", response_model=BudgetPublicCategory)
def get_budget(id: int, session: Session = Depends(get_session)):
    _service = BudgetService(session)
    return _service.get_budget(id)


@router.get("/user/{user_id}/filter", response_model=list[BudgetPublicCategory])
def get_filtered_budgets(user_id: int, year: int | None = None, month: int | None = None, session: Session = Depends(get_session)):
    _service = BudgetService(session)
    return _service.get_filtered(user_id, {"year": year, "month": month})


@router.patch("/{id}", response_model=BudgetPublicCategory)
def update_budget(id: int, budget: BudgetUpdate, session: Session = Depends(get_session)):
    _service = BudgetService(session)
    return _service.update(id, budget)


@router.post("/", response_model=BudgetPublic)
def create_budget(budget: BudgetCreate, session: Session = Depends(get_session)):
    _service = BudgetService(session)
    return _service.create(budget)


@router.post("/many", response_model=list[BudgetPublicCategory])
def create_many_budgets(budgets: list[BudgetCreate], session: Session = Depends(get_session)):
    _service = BudgetService(session)
    return _service.create_many(budgets)


@router.delete("/{id}", response_model=BudgetPublicCategory)
def delete_budget(id: int, session: Session = Depends(get_session)):
    _service = BudgetService(session)
    return _service.delete(id)
