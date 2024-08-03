from sqlmodel import select

from api.models import Budget, BudgetCreate, BudgetPublic, BudgetPublicCategory, BudgetUpdate
from api.repositories.base_repository import BaseRepository


class BudgetRepository(BaseRepository):

    def get_all(self, user_id: int) -> list[BudgetPublicCategory]:
        return self.session.exec(select(Budget).where(Budget.user_id == user_id)).all()

    def get_one(self, id: int) -> BudgetPublicCategory:
        return self.session.get(Budget, id)

    def get_filtered(self, user_id: int, filters: dict) -> list[BudgetPublicCategory]:
        query = select(Budget).where(Budget.user_id == user_id)
        if filters['year'] is not None:
            query = query.where(Budget.year == filters['year'])
        if filters['month'] is not None:
            query = query.where(Budget.month == filters['month'])
        return self.session.exec(query).all()

    def update(self, id: int, budget: BudgetUpdate) -> BudgetPublic:
        updated_budget = self.session.get(Budget, id)
        for key, value in budget.model_dump(exclude_unset=True).items():
            setattr(updated_budget, key, value)
        self.session.add(updated_budget)
        self.session.commit()
        self.session.refresh(updated_budget)
        return updated_budget

    def create(self, budget: BudgetCreate) -> BudgetPublic:
        budget = Budget.model_validate(budget)
        self.session.add(budget)
        self.session.commit()
        self.session.refresh(budget)
        return budget

    def create_many(self, budgets: list[BudgetCreate]) -> list[BudgetPublicCategory]:
        created_budgets = []
        for budget in budgets:
            created_budget = self.create(budget)
            created_budgets.append(created_budget)
        return created_budgets

    def delete(self, budget_id: int) -> BudgetPublic:
        budget = self.session.get(Budget, budget_id)
        self.session.delete(budget)
        self.session.commit()
        return BudgetPublic.model_validate(budget)
