from datetime import date

from pydantic import BaseModel


class Reminder(BaseModel):
    id: int
    task_id: int
    trigger_date: date
    done: bool
    timestamp_done: date | None


class CreateReminder(BaseModel):
    task_id: int
    trigger_date: date
