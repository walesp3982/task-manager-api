from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

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
    trigger_date: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        index=True,
    )
    done: Mapped[bool] = mapped_column(
        default=False,
        index=True,
        nullable=False,
    )
    timestamp_done: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=True,
        index=True,
    )
    task: Mapped["TaskModel"] = relationship("Task", back_populates="reminders")
    __table_args__ = (Index("idx_done", "done", "timestamp_done"),)
