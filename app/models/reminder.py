from datetime import date, datetime
from typing import TYPE_CHECKING, Optional

from sqlalchemy import DateTime, ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.entities import CreateReminder, Reminder
from app.models.base import Base

if TYPE_CHECKING:
    from app.models.task import TaskModel


class ReminderModel(Base):
    __tablename__ = "reminders"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )
    task_id: Mapped[int] = mapped_column(
        ForeignKey("tasks.id"),
        index=True,
        nullable=False,
    )
    trigger_date: Mapped[date] = mapped_column(
        DateTime,
        nullable=False,
        index=True,
    )
    done: Mapped[bool] = mapped_column(
        default=False,
        index=True,
        nullable=False,
    )
    timestamp_done: Mapped[Optional[datetime]] = mapped_column(
        DateTime,
        nullable=True,
        index=True,
    )
    task: Mapped["TaskModel"] = relationship("Task", back_populates="reminders")
    __table_args__ = (Index("idx_done", "done", "timestamp_done"),)

    def __init__(self, reminder: CreateReminder):
        self.task_id = reminder.task_id
        self.trigger_date = reminder.trigger_date

    def get_entity(self) -> Reminder:
        return Reminder(
            id=self.id,
            done=self.done,
            task_id=self.task_id,
            timestamp_done=self.timestamp_done,
            trigger_date=self.trigger_date,
        )
