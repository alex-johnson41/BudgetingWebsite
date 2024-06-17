from typing import TYPE_CHECKING, Optional
from sqlmodel import Field, Relationship, SQLModel
from sqlalchemy.orm import Mapped


if TYPE_CHECKING:
    from api.models.user import User, UserPublic
    # from api.models.category import Category


class TransactionBase(SQLModel):
    user_id: int | None = Field(default=None, foreign_key="user.id")
    # category_id: int | None = Field(default=None, foreign_key="category.id")
    date: str
    amount: int


class Transaction(TransactionBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

    user: Mapped[Optional["User"]] = Relationship(
        back_populates="transactions")
    # category: Optional["Category"] = Relationship(
    #     back_populates="transactions")


class TransactionPublic(TransactionBase):
    id: int


class TransactionCreate(TransactionBase):
    pass


class TransactionUpdate(SQLModel):
    date: str | None = None
    amount: str | None = None
    user_id: str | None = None
    # category_id: Optional[int] = None
