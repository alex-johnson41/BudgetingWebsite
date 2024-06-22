from sqlmodel import Session
from api.models import Category
from api.repositories.category_repository import CategoryRepository


class CategoryService:

    def __init__(self, session: Session):
        self.repository = CategoryRepository(session)

    def get_all_categories(self, user_id: int) -> list[Category]:
        return self.repository.get_all(user_id)

    def get_category_by_name(self, user_id: int, category_name: str) -> Category:
        return self.repository.get_by_name(user_id, category_name)

    def get_filtered(self, user_id: int, filters: dict) -> list[Category]:
        return self.repository.get_filtered(user_id, filters)

    def create(self, category: Category) -> Category:
        return self.repository.create(category)
