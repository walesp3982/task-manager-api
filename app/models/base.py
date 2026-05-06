from sqlalchemy import URL, create_engine
from sqlalchemy.orm import DeclarativeBase

from app.settings.database import DatabaseSettings

db_settings = DatabaseSettings()  # pyright: ignore[reportCallIssue]


url = URL.create(
    drivername="postgresql",
    username=db_settings.user,
    password=db_settings.password,
    host=db_settings.host,
    port=db_settings.port,
    database=db_settings.name,
)

engine = create_engine(url)


class Base(DeclarativeBase):
    pass
