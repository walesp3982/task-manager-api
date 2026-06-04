from datetime import date
from typing import TYPE_CHECKING, Optional

from sqlalchemy import Date, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.entities.task import CreateTask, StatusTask, Task
from app.models.base import Base

if TYPE_CHECKING:
    from app.models.reminder import ReminderModel
    from app.models.user import UserModel


class TaskModel(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(
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
    date_limit: Mapped[Optional[date]] = mapped_column(
        Date(),
        index=True,
        nullable=True,
    )
    status: Mapped[StatusTask] = mapped_column(
        Enum(StatusTask),
        default=StatusTask.pending,
        nullable=False,
    )
    user: Mapped["UserModel"] = relationship(back_populates="tasks")
    reminders: Mapped[list["ReminderModel"]] = relationship(
        back_populates="task",
        cascade="all, delete-orphan",
    )

    def __init__(self, dto: CreateTask):
        self.user_id = dto.user_id
        self.date_limit = dto.date_limit
        self.name = dto.name
        self.status = dto.status

    def get_entity(self):
        return Task(
            id=self.id,
            name=self.name,
            user_id=self.user_id,
            date_limit=self.date_limit,
            status=self.status,
        )
