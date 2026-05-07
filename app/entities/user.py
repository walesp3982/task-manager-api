from typing import TYPE_CHECKING

from pydantic import BaseModel

if TYPE_CHECKING:
    from app.entities.task import Task


class User(BaseModel):
    id: int
    name: str
    email: str
    password: str


class UserWithTask(User):
    tasks: list[Task]


class CreateUser(BaseModel):
    name: str
    email: str
    password: str
