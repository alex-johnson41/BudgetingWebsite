from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from api.services.transaction_service import TransactionService
from api.dependencies import get_session
from api.models import TransactionCreate, TransactionPublic

router = APIRouter(
    prefix="/transaction",
    responses={404: {"description": "Not found"}},
)


@router.get("/user/{user_id}", response_model=list[TransactionPublic])
def get_all_transactions(user_id: int, session: Session = Depends(get_session)):
    _service = TransactionService(session)
    return _service.get_all(user_id)


@router.get("/{user_id}/filter", response_model=list[TransactionPublic])
def get_filtered_transactions(user_id: int, filters: dict, session: Session = Depends(get_session)):
    _service = TransactionService(session)
    return _service.get_filtered(user_id, filters)


@router.get("/{transaction_id}", response_model=TransactionPublic)
def get_transaction_by_id(transaction_id: int, session: Session = Depends(get_session)):
    _service = TransactionService(session)
    return _service.get_by_id(transaction_id)


@router.post("/", response_model=TransactionPublic)
def create_transaction(transaction: TransactionCreate, session: Session = Depends(get_session)) -> TransactionPublic:
    _service = TransactionService(session)
    return _service.create(transaction)


@router.delete("/{transaction_id}", response_model=TransactionPublic)
def delete_transaction(transaction_id: int, session: Session = Depends(get_session)):
    _service = TransactionService(session)
    return _service.delete(transaction_id)
