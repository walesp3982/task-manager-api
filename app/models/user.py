from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

if TYPE_CHECKING:
    from app.models.task import TaskModel
    from app.models.token import TokenModel


class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )
    name: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        index=True,
    )
    email: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        unique=True,
        index=True,
    )
    password: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    tokens: Mapped[list["TokenModel"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )
    tasks: Mapped[list["TaskModel"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )
