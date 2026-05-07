from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel

from app.entities.reminder import Reminder
from app.entities.user import User


class StatusTask(StrEnum):
    pending = "pending"
    progress = "progress"
    done = "done"


class Task(BaseModel):
    id: int
    user_id: int
    name: str
    date_limit: datetime | None
    status: StatusTask


class CreateTask(BaseModel):
    name: str
    date_limit: datetime | None
    status: StatusTask = StatusTask.pending


class TaskWithUser(Task):
    user: User


class TaskWithReminders(Task):
    reminders: list[Reminder]


class TaskWithUserAndReminders(Task):
    user: User
    reminders: list[Reminder]
