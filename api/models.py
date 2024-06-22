from typing import List, Optional

from sqlmodel import Field, Relationship, SQLModel


class TransactionBase(SQLModel):
    user_id: int | None = Field(default=None, foreign_key="user.id")
    category_id: int | None = Field(default=None, foreign_key="category.id")
    date: str
    amount: float


class Transaction(TransactionBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

    user: Optional["User"] = Relationship(
        back_populates="transactions")
    category: Optional["Category"] = Relationship(
        back_populates="transactions")


class TransactionPublic(TransactionBase):
    id: int


class TransactionCreate(TransactionBase):
    pass


class TransactionUpdate(SQLModel):
    date: str | None = None
    amount: float | None = None
    user_id: str | None = None
    category_id: Optional[int] = None


class UserBase(SQLModel):
    username: str


class User(UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

    transactions: List["Transaction"] = Relationship(
        back_populates="user")
    categories: List["Category"] = Relationship(back_populates="user")


class UserPublic(UserBase):
    id: int
    transactions: List[Transaction] = []


class UserCreate(UserBase):
    pass


class Category(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user_id: int | None = Field(default=None, foreign_key="user.id")
    name: str = Field()
    is_income: bool = Field(default=False)

    user: Optional["User"] = Relationship(back_populates="categories")
    transactions: List["Transaction"] = Relationship(
        back_populates="category")
