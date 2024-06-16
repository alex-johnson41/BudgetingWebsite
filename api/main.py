from fastapi import Depends, FastAPI
from fastapi.concurrency import asynccontextmanager

from dependencies import get_session
from routers import transactions
from database import database


app = FastAPI(
    dependencies=[Depends(get_session)]
)
app.include_router(transactions.router)

@asynccontextmanager
async def lifespan(app: FastAPI):
    database.create_db_and_tables()