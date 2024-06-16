from sqlmodel import Field, SQLModel


class Transaction(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user_id: int | None = Field(default=None, foreign_key="user.id")
    date: str
    amount: int
    category: str
