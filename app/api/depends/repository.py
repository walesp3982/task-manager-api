from typing import Annotated, Generator

from fastapi import Depends
from sqlalchemy.orm import Session

from app.models import engine
from app.repository import (
    ReminderRepository,
    TaskRepository,
    TokenRepository,
    UserRepository,
)
from app.repository.protocol import reminder, task, token, user


def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]


def get_user_repository(session: SessionDep) -> user.UserRepositoryProtocol:
    return UserRepository(session)


UserRepositoryDep = Annotated[user.UserRepositoryProtocol, Depends(get_user_repository)]


def get_task_repository(session: SessionDep) -> task.TaskRepositoryProtocol:
    return TaskRepository(session)


TaskRepositoryDep = Annotated[task.TaskRepositoryProtocol, Depends(get_task_repository)]


def get_token_repository(session: SessionDep) -> token.TokenRepositoryProtocol:
    return TokenRepository(session)


TokenRepositoryDep = Annotated[
    token.TokenRepositoryProtocol, Depends(get_token_repository)
]


def get_reminder_repository(session: SessionDep) -> reminder.ReminderRepositoryProtocol:
    return ReminderRepository(session)


ReminderRepositoryDep = Annotated[
    reminder.ReminderRepositoryProtocol, Depends(get_reminder_repository)
]
