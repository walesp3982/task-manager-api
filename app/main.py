from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.routes import auth, user
from app.models import Base, engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield
    # Next line only debug schema
    # Base.metadata.drop_all(bind=engine)


app = FastAPI(lifespan=lifespan)
app.include_router(auth.router)
app.include_router(user.router)
