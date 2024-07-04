from typing import List, Optional

from sqlmodel import Field, Relationship, SQLModel

"""
################################################################################################
                ALL MODELS MUST BE DEFINED HERE TO AVOID CIRCULAR IMPORTS
################################################################################################
"""


"""
################################################################################################
################################################################################################
                                    TRANSACTION MODELS
################################################################################################
################################################################################################
"""


class TransactionBase(SQLModel):
    user_id: int | None = Field(default=None, foreign_key="user.id")
    category_id: int | None = Field(default=None, foreign_key="category.id")
    date: str
    amount: float
    description: str | None = Field(default=None)


class Transaction(TransactionBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

    user: Optional["User"] = Relationship(
        back_populates="transactions")
    category: Optional["Category"] = Relationship(
        back_populates="transactions")


class TransactionPublic(TransactionBase):
    id: int


class TransactionPublicUserCategory(TransactionBase):
    id: int
    user: Optional["UserPublic"] = None
    category: Optional["CategoryPublic"] = None


class TransactionPublicUser(TransactionBase):
    id: int
    user: Optional["UserPublic"] = None


class TransactionPublicCategory(TransactionBase):
    id: int
    category: Optional["CategoryPublic"] = None


class TransactionCreate(TransactionBase):
    pass


class TransactionUpdate(SQLModel):
    date: str | None = None
    amount: float | None = None
    user_id: str | None = None
    category_id: int | None = None


"""
################################################################################################
################################################################################################
                                    USER MODELS
################################################################################################
################################################################################################
"""


class UserBase(SQLModel):
    username: str


class User(UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

    transactions: List["Transaction"] = Relationship(
        back_populates="user")
    categories: List["Category"] = Relationship(back_populates="user")


class UserPublic(UserBase):
    id: int


class UserPublicCategories(UserBase):
    id: int
    categories: List["Category"] = []


class UserPublicTransactions(UserBase):
    id: int
    transactions: List["Transaction"] = []


class UserCreate(UserBase):
    pass


"""
################################################################################################
################################################################################################
                                    CATEGORY MODELS
################################################################################################
################################################################################################                                   
"""


class CategoryBase(SQLModel):
    user_id: int | None = Field(default=None, foreign_key="user.id")
    name: str = Field()
    is_income: bool = Field(default=False)


class Category(CategoryBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

    user: Optional["User"] = Relationship(back_populates="categories")
    transactions: List["Transaction"] = Relationship(
        back_populates="category")


class CategoryPublic(CategoryBase):
    id: int


class CategoryPublicUser(CategoryBase):
    id: int
    user: Optional["UserPublic"] = None


class CategoryPublicTransactions(CategoryBase):
    id: int
    transactions: List["Transaction"] = []


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(SQLModel):
    name: str | None = None
    user_id: int | None = None
    is_income: bool | None = None
