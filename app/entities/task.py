from datetime import date
from enum import StrEnum

from pydantic import BaseModel


class StatusTask(StrEnum):
    pending = "pending"
    progress = "progress"
    done = "done"


class Task(BaseModel):
    id: int
    user_id: int
    name: str
    date_limit: date | None
    status: StatusTask


class CreateTask(BaseModel):
    user_id: int
    name: str
    date_limit: date | None
    status: StatusTask = StatusTask.pending
