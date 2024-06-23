from fastapi import HTTPException
from sqlmodel import Session
from api.models import Category, CategoryPublic, CategoryPublicUser, CategoryUpdate
from api.repositories.category_repository import CategoryRepository


class CategoryService:

    def __init__(self, session: Session):
        self.repository = CategoryRepository(session)

    def get_all_categories(self, user_id: int) -> list[CategoryPublic]:
        return self.repository.get_all(user_id)

    def get_category(self, id: int) -> CategoryPublicUser:
        category = self.repository.get_one(id)
        if category is None:
            raise HTTPException(
                status_code=404, detail="Category not found")
        return category

    def get_filtered(self, user_id: int, filters: dict) -> list[CategoryPublicUser]:
        return self.repository.get_filtered(user_id, filters)

    def update(self, category_id: int, category: CategoryUpdate) -> CategoryPublic:
        return self.repository.update(category_id, category)

    def create(self, category: Category) -> CategoryPublic:
        return self.repository.create(category)

    def delete(self, category_id: int) -> CategoryPublic:
        return self.repository.delete(category_id)
