from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from dependencies import get_session
from models.transaction import Transaction

router = APIRouter(
    prefix="/transactions",
    responses={404: {"description": "Not found"}},
)

@router.post("/")
def create_transaction(transaction: Transaction, session: Session = Depends(get_session)):
    session.add(transaction)
    session.commit()
    session.refresh(transaction)
    return transaction


@router.get("/")
def read_heroes(session: Session = Depends(get_session)):
    heroes = session.exec(select(Transaction)).all()
    return heroes


@router.post("/drop")
def drop_table(session: Session = Depends(get_session)):
    transactions = session.exec(select(Transaction)).all()
    for transaction in transactions:
        session.delete(transaction)
    session.commit()
    return "Table dropped"
