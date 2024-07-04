from fastapi import Depends, FastAPI
from fastapi.concurrency import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware

from api.dependencies import get_session
from api.routers import transaction_routes, user_routes, category_routes
from api.database import database


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        database.create_db_and_tables()
        yield
    finally:
        pass

origins = [
    "*",
]


app = FastAPI(
    dependencies=[Depends(get_session)],
    lifespan=lifespan
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(transaction_routes.router)
app.include_router(user_routes.router)
app.include_router(category_routes.router)
