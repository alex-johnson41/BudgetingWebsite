from sqlmodel import Session
from api.models import Category, CategoryPublic, CategoryPublicTransactions, CategoryPublicUser
from api.repositories.category_repository import CategoryRepository


class CategoryService:

    def __init__(self, session: Session):
        self.repository = CategoryRepository(session)

    def get_all_categories(self, user_id: int) -> list[CategoryPublic]:
        return self.repository.get_all(user_id)

    def get_category(self, id: int) -> CategoryPublicUser:
        return self.repository.get_one(id)

    def get_filtered(self, user_id: int, filters: dict) -> list[CategoryPublicUser]:
        return self.repository.get_filtered(user_id, filters)

    def create(self, category: Category) -> CategoryPublic:
        return self.repository.create(category)

    def delete(self, category_id: int) -> CategoryPublic:
        return self.repository.delete(category_id)
