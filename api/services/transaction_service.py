from fastapi import HTTPException
from sqlmodel import Session
from api.models import TransactionCreate, TransactionPublic, TransactionPublicCategory, TransactionUpdate
from api.repositories.transaction_repository import TransactionRepository


class TransactionService:

    def __init__(self, session: Session):
        self.repository = TransactionRepository(session)

    def get_all(self, user_id: int) -> list[TransactionPublicCategory]:
        return self.repository.get_all(user_id)

    def get_filtered(self, user_id: int, filters: dict) -> list[TransactionPublicCategory]:
        return self.repository.get_filtered(user_id, filters)

    def get_by_id(self, transaction_id: int) -> TransactionPublicCategory:
        transaction = self.repository.get_by_id(transaction_id)
        if transaction == None:
            raise HTTPException(
                status_code=404, detail="Transaction not found")
        return transaction

    def create(self, transaction: TransactionCreate) -> TransactionPublic:
        return self.repository.create(transaction)

    def update(self, transaction_id: int, transaction: TransactionUpdate) -> TransactionPublicCategory:
        transaction = self.repository.update(transaction_id, transaction)
        if transaction == None:
            raise HTTPException(
                status_code=404, detail="Transaction not found")
        return transaction

    def delete(self, transaction_id: int) -> TransactionPublic:
        transaction = self.repository.delete(transaction_id)
        if transaction == None:
            raise HTTPException(
                status_code=404, detail="Transaction not found")
        return transaction
