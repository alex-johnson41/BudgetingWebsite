from fastapi import APIRouter, Depends
from sqlmodel import Session

from api.services.transaction_service import TransactionService
from api.dependencies import get_session
from api.models import TransactionCreate, TransactionPublic, TransactionPublicCategory

router = APIRouter(
    prefix="/transaction",
    responses={404: {"description": "Not found"}},
)


@router.get("/user/{user_id}", response_model=list[TransactionPublicCategory])
def get_all_transactions(user_id: int, session: Session = Depends(get_session)):
    _service = TransactionService(session)
    return _service.get_all(user_id)


@router.get("/{user_id}/filter", response_model=list[TransactionPublicCategory])
def get_filtered_transactions(
    user_id: int,
    year: int | None = None,
    month: int | None = None,
    day: int | None = None,
    category_id: int | None = None,
    amount_greater_than: float | None = None,
    amount_less_than: float | None = None,
    amount_equal_to: float | None = None,
    session: Session = Depends(get_session)
):
    _service = TransactionService(session)
    filters = {
        "year": year,
        "month": month,
        "day": day,
        "category_id": category_id,
        "amount_greater_than": amount_greater_than,
        "amount_less_than": amount_less_than,
        "amount_equal_to": amount_equal_to
    }
    return _service.get_filtered(user_id, filters)


@router.get("/{transaction_id}", response_model=TransactionPublicCategory)
def get_transaction_by_id(transaction_id: int, session: Session = Depends(get_session)):
    _service = TransactionService(session)
    return _service.get_by_id(transaction_id)


@router.patch("/{transaction_id}", response_model=TransactionPublicCategory)
def update_transaction(transaction_id: int, transaction: TransactionCreate, session: Session = Depends(get_session)):
    _service = TransactionService(session)
    return _service.update(transaction_id, transaction)


@router.post("/", response_model=TransactionPublic)
def create_transaction(transaction: TransactionCreate, session: Session = Depends(get_session)) -> TransactionPublic:
    _service = TransactionService(session)
    return _service.create(transaction)


@router.delete("/{transaction_id}", response_model=TransactionPublic)
def delete_transaction(transaction_id: int, session: Session = Depends(get_session)):
    _service = TransactionService(session)
    return _service.delete(transaction_id)
