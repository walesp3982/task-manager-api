from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.models import Base, engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield
    # Next line only debug schema
    # Base.metadata.drop_all(bind=engine)


app = FastAPI(lifespan=lifespan)
