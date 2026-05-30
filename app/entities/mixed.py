from app.entities.reminder import Reminder
from app.entities.task import Task
from app.entities.token import Token
from app.entities.user import User


class UserWithTask(User):
    tasks: list[Task]


class TokenWithUser(Token):
    user: User


class ReminderWithTask(Reminder):
    task: Task


class TaskWithUser(Task):
    user: User


class TaskWithReminders(Task):
    reminders: list[Reminder]


class TaskWithUserAndReminders(Task):
    user: User
    reminders: list[Reminder]
