from sqlmodel import select
from sqlalchemy.sql import extract

from api.models import Transaction, TransactionPublic, TransactionCreate, TransactionPublicCategory, TransactionUpdate
from api.repositories.base_repository import BaseRepository


class TransactionRepository(BaseRepository):

    def get_all(self, user_id: int) -> list[TransactionPublicCategory]:
        return self.session.exec(select(Transaction).where(Transaction.user_id == user_id)).all()

    def get_by_id(self, transaction_id: int) -> TransactionPublicCategory:
        return self.session.get(Transaction, transaction_id)

    def get_filtered(self, user_id: int, filters: dict) -> list[TransactionPublicCategory]:
        query = select(Transaction).where(Transaction.user_id == user_id)
        if filters['year'] is not None:
            query = query.where(
                extract('year', Transaction.date) == int(filters['year']))
        if filters['month'] is not None:
            query = query.where(
                extract('month', Transaction.date) == int(filters['month']))
        if filters['day'] is not None:
            query = query.where(
                extract('day', Transaction.date) <= int(filters['day']))
        if filters['category_id'] is not None:
            query = query.where(Transaction.category_id ==
                                filters['category_id'])
        if filters['amount_greater_than'] is not None:
            query = query.where(Transaction.amount >
                                filters['amount_greater_than'])
        if filters['amount_less_than'] is not None:
            query = query.where(Transaction.amount <
                                filters['amount_less_than'])
        if filters['amount_equal_to'] is not None:
            query = query.where(Transaction.amount ==
                                filters['amount_equal_to'])

        return self.session.exec(query).all()

    def update(self, transaction_id: int, transaction: TransactionUpdate) -> TransactionPublic:
        updated_transaction = self.get_by_id(transaction_id)
        for key, value in transaction.model_dump().items():
            setattr(updated_transaction, key, value)
        self.session.commit()
        self.session.refresh(updated_transaction)
        return updated_transaction

    def create(self, transaction: TransactionCreate) -> TransactionPublic:
        transaction = Transaction.model_validate(transaction)
        self.session.add(transaction)
        self.session.commit()
        self.session.refresh(transaction)
        return TransactionPublic.model_validate(transaction)

    def delete(self, transaction_id: int) -> TransactionPublic:
        transaction = self.session.get(Transaction, transaction_id)
        self.session.delete(transaction)
        self.session.commit()
        return TransactionPublic.model_validate(transaction)
