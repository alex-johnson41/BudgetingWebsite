from sqlmodel import Session

from api.models.transaction import Transaction
from api.repositories.transaction_repository import TransactionRepository


class TransactionService:
    def __init__(self, session: Session):
        self.transaction_repository = TransactionRepository(session)

    def get_all(self) -> list[Transaction]:
        return self.transaction_repository.get_all()
    
    def get_filtered(self, filters: dict) -> list[Transaction]:
        return self.transaction_repository.get_filtered(filters)
    
    def get_by_id(self, transaction_id: int) -> Transaction:
        return self.transaction_repository.get_by_id(transaction_id)
    
    def create(self, transaction: Transaction) -> Transaction:
        return self.transaction_repository.create(transaction)
    
    def update(self, transaction_id: int, transaction: Transaction) -> Transaction:
        return self.transaction_repository.update(transaction_id, transaction)
    
    def delete(self, transaction_id: int) -> Transaction:
        return self.transaction_repository.delete(transaction_id)