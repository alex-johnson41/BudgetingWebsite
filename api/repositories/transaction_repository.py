from sqlmodel import Session, select

from api.models.transaction import Transaction


class TransactionRepository:

    def __init__(self, session: Session):
        self.session = session

    def get_all(self, user_id: int) -> list[Transaction]:
        return self.session.exec(select(Transaction).where(Transaction.user_id == user_id)).all()

    def get_by_id(self, transaction_id: int) -> Transaction:
        return self.session.get(Transaction, transaction_id)

    def get_filtered(self, user_id: int, filters: dict) -> list[Transaction]:
        query = select(Transaction).where(Transaction.user_id == user_id)
        if 'year' in filters:
            query = query.where(Transaction.date.split("-")
                                [0] == filters['year'])
        if 'month' in filters:
            query = query.where(Transaction.date.split("-")
                                [1] == filters['month'])
        if 'day' in filters:
            query = query.where(Transaction.date.split("-")
                                [2] == filters['day'])
        if 'category' in filters:
            query = query.where(Transaction.category == filters['category'])
        if 'amount_greater_than' in filters:
            query = query.where(Transaction.amount >
                                filters['amount_greater_than'])
        if 'amount_less_than' in filters:
            query = query.where(Transaction.amount <
                                filters['amount_less_than'])
        if 'amount_equal_to' in filters:
            query = query.where(Transaction.amount ==
                                filters['amount_equal_to'])

        return self.session.exec(query).all()

    def create(self, transaction: Transaction) -> Transaction:
        self.session.add(transaction)
        self.session.commit()
        self.session.refresh(transaction)
        return transaction

    def update(self, transaction_id: int, transaction: Transaction) -> Transaction:
        updated_transaction = self.get_by_id(transaction_id)
        for key, value in transaction.model_dump().items():
            setattr(updated_transaction, key, value)
        self.session.commit()
        self.session.refresh(updated_transaction)
        return updated_transaction

    def delete(self, transaction_id: int) -> Transaction:
        transaction = self.get_by_id(transaction_id)
        self.session.delete(transaction)
        self.session.commit()
        return transaction
