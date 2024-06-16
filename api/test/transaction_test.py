from unittest.mock import Mock
from sqlmodel import Session, select
from api.models.transaction import Transaction
from api.repositories.transaction_repository import TransactionRepository

class TestTransactionRepository:

    def setup_method(self):
        self.session = Mock(spec=Session)
        self.repository = TransactionRepository(self.session)

    def test_get_all(self):
        user_id = 1
        expected_query = self.session.exec.return_value
        expected_query.all.return_value = []

        result = self.repository.get_all(user_id)

        assert result == []
        self.session.exec.assert_called_once_with(
            select(Transaction).where(Transaction.user_id == user_id))
        expected_query.all.assert_called_once()

    def test_get_by_id(self):
        transaction_id = 1
        expected_query = self.session.get.return_value

        result = self.repository.get_by_id(transaction_id)

        assert result == expected_query
        self.session.get.assert_called_once_with(Transaction, transaction_id)

    def test_get_filtered(self):
        user_id = 1
        filters = {'year': '2022', 'category': 'Food'}
        expected_query = self.session.exec.return_value
        expected_query.all.return_value = []

        result = self.repository.get_filtered(user_id, filters)

        assert result == []
        self.session.exec.assert_called_once_with(
            select(Transaction).where(Transaction.user_id == user_id)
            .where(Transaction.date.split("-")[0] == filters['year'])
            .where(Transaction.category == filters['category'])
        )
        expected_query.all.assert_called_once()

    def test_create(self):
        transaction = Transaction(
            user_id=1, date="2022-01-01", category="Food", amount=10.0)
        expected_transaction = Transaction(
            id=1, user_id=1, date="2022-01-01", category="Food", amount=10.0)
        self.session.add.return_value = None
        self.session.commit.return_value = None
        self.session.refresh.return_value = None

        result = self.repository.create(transaction)

        assert result == expected_transaction
        self.session.add.assert_called_once_with(transaction)
        self.session.commit.assert_called_once()
        self.session.refresh.assert_called_once_with(transaction)

    def test_update(self):
        transaction_id = 1
        transaction = Transaction(
            user_id=1, date="2022-01-01", category="Food", amount=10.0)
        updated_transaction = Transaction(
            id=1, user_id=1, date="2022-01-01", category="Food", amount=10.0)
        self.repository.get_by_id.return_value = updated_transaction
        self.session.commit.return_value = None
        self.session.refresh.return_value = None

        result = self.repository.update(transaction_id, transaction)

        assert result == updated_transaction
        self.repository.get_by_id.assert_called_once_with(transaction_id)
        self.session.commit.assert_called_once()
        self.session.refresh.assert_called_once_with(updated_transaction)

    def test_delete(self):
        transaction_id = 1
        transaction = Transaction(
            id=1, user_id=1, date="2022-01-01", category="Food", amount=10.0)
        self.repository.get_by_id.return_value = transaction
        self.session.commit.return_value = None

        result = self.repository.delete(transaction_id)

        assert result == transaction
        self.repository.get_by_id.assert_called_once_with(transaction_id)
        self.session.delete.assert_called_once_with(transaction)
        self.session.commit.assert_called_once()
