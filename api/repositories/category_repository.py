from sqlmodel import select

from api.models import Category, CategoryCreate, CategoryPublic, CategoryPublicUser
from api.repositories.base_repository import BaseRepository


class CategoryRepository(BaseRepository):

    def get_all(self, user_id: int) -> list[CategoryPublic]:
        return self.session.exec(select(Category).where(Category.user_id == user_id)).all()

    def get_one(self, id: int) -> CategoryPublicUser:
        return self.session.get(Category, id)

    def get_filtered(self, user_id: int, filters: dict) -> list[CategoryPublicUser]:
        query = select(Category).where(Category.user_id == user_id)
        if filters['name'] is not None:
            query = query.where(Category.name == filters['name'])
        if filters['income'] is not None:
            if filters['income']:
                query = query.where(Category.is_income)
            else:
                query = query.where(Category.is_income == False)
        return self.session.exec(query).all()

    def create(self, category: CategoryCreate) -> Category:
        category = Category.model_validate(category)
        self.session.add(category)
        self.session.commit()
        self.session.refresh(category)
        return category

    def delete(self, category_id: int) -> CategoryPublic:
        category = self.session.get(Category, category_id)
        self.session.delete(category)
        self.session.commit()
        return category
