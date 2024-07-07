from fastapi import HTTPException
from sqlmodel import Session
from api.models import Budget, BudgetPublic, BudgetPublicCategory, BudgetUpdate, BudgetCreate
from api.repositories.budget_repository import BudgetRepository


class BudgetService:

    def __init__(self, session: Session):
        self.repository = BudgetRepository(session)

    def get_all_budgets(self, user_id: int) -> list[BudgetPublicCategory]:
        return self.repository.get_all(user_id)

    def get_budget(self, id: int) -> BudgetPublicCategory:
        budget = self.repository.get_one(id)
        if budget is None:
            raise HTTPException(
                status_code=404, detail="Budget not found")
        return budget

    def get_filtered(self, user_id: int, filters: dict) -> list[BudgetPublicCategory]:
        return self.repository.get_filtered(user_id, filters)

    def update(self, budget_id: int, budget: BudgetUpdate) -> BudgetPublicCategory:
        return self.repository.update(budget_id, budget)

    def create(self, budget: BudgetCreate) -> BudgetPublic:
        return self.repository.create(budget)

    def delete(self, budget_id: int) -> BudgetPublic:
        return self.repository.delete(budget_id)
