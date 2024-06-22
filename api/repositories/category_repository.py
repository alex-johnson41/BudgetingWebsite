from sqlmodel import select

from api.models import Category
from api.repositories.base_repository import BaseRepository


class CategoryRepository(BaseRepository):

    def get_all(self, user_id: int) -> list[Category]:
        return self.session.get(Category, user_id)

    def get_by_id(self, category_id: int) -> Category:
        return self.session.get(Category, category_id)

    def get_by_name(self, user_id: int, category_name: str) -> Category:
        return self.session.exec(select(Category).where(Category.user_id == user_id).where(Category.name == category_name)).first()

    def get_filtered(self, user_id: int, filters: dict) -> list[Category]:
        query = select(Category).where(Category.user_id == user_id)
        if 'name' in filters:
            query = query.where(Category.name == filters['name'])
        if 'income' in filters:
            query = query.where(Category.is_income)
        if 'expense' in filters:
            query = query.where(not Category.is_income)
        return self.session.exec(query).all()

    def create(self, category: Category) -> Category:
        self.session.add(category)
        self.session.commit()
        self.session.refresh(category)
        return category

    def delete(self, category_id: int) -> Category:
        category = self.session.get(Category, category_id)
        self.session.delete(category)
        self.session.commit()
        return category
