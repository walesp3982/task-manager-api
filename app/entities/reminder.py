from datetime import date

from pydantic import BaseModel

from app.entities.task import Task


class Reminder(BaseModel):
    id: int
    task_id: int
    trigger_date: date
    done: bool
    timestamp_done: date | None


class CreateReminder(BaseModel):
    task_id: int
    trigger_date: date


class ReminderWithTask(Reminder):
    task: Task
