from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from api.services.transaction_service import TransactionService
from api.dependencies import get_session
from api.models.transaction import Transaction

router = APIRouter(
    prefix="/transaction",
    responses={404: {"description": "Not found"}},
)


@router.post("/")
def create_transaction(transaction: Transaction, session: Session = Depends(get_session)):
    _service = TransactionService(session)
    return _service.create(transaction)


@router.get("/")
def get_all_transactions(session: Session = Depends(get_session)):
    _service = TransactionService(session)
    return _service.get_all()


@router.get("/{transaction_id}")
def get_transaction_by_id(transaction_id: int, session: Session = Depends(get_session)):
    _service = TransactionService(session)
    return _service.get_by_id(transaction_id)


@router.post("/drop")
def drop_table(session: Session = Depends(get_session)):
    transactions = session.exec(select(Transaction)).all()
    for transaction in transactions:
        session.delete(transaction)
    session.commit()
    return "Table dropped"
