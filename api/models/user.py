from typing import TYPE_CHECKING, List
from sqlmodel import Field, Relationship, SQLModel
from api.models.transaction import Transaction
from sqlalchemy.orm import Mapped


if TYPE_CHECKING:
    # from api.models.category import Category
    from api.models.transaction import Transaction


class UserBase(SQLModel):
    username: str


class User(UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

    transactions: Mapped[list[Transaction]
                         ] = Relationship(back_populates="user")


class UserPublic(UserBase):
    id: int
    transactions: list[Transaction] = []


class UserCreate(UserBase):
    pass
