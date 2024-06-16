from sqlmodel import Field, SQLModel


class Transaction(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    userID: int | None = Field(default=None)
    date: str
    amount: int
    category: str
