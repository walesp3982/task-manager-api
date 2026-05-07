from datetime import date

from sqlalchemy import Column, Date, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.entities.task import StatusTask
from app.models.base import Base
from app.models.reminder import Reminder
from app.models.user import User


class Task(Base):
    __tablename__ = "tasks"

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        index=True,
        nullable=False,
    )
    name: Mapped[str] = mapped_column(
        String(30),
        index=True,
        nullable=False,
    )
    date_limit: Mapped[date] = mapped_column(
        Date(),
        index=True,
        nullable=True,
    )
    status: Mapped[StatusTask] = mapped_column(
        Enum(StatusTask),
        default=StatusTask.pending,
        nullable=False,
    )
    user: Mapped["User"] = relationship(back_populates="tasks")
    reminder: Mapped["Reminder"] = relationship(
        back_populates="task",
        cascade="all, delete-orphan",
    )
