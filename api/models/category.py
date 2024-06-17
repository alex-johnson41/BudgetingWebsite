from __future__ import annotations
from typing import TYPE_CHECKING, Optional, List
from sqlmodel import Field, Relationship, SQLModel

from api.models.transaction import Transaction

if TYPE_CHECKING:
    from api.models.user import User


class Category(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user_id: int | None = Field(default=None, foreign_key="user.id")
    name: str = Field()
    is_income: bool = Field(default=False)

    # user: Optional["User"] = Relationship(back_populates="categories")
    # transactions: List["Transaction"] = Relationship(back_populates="category")
