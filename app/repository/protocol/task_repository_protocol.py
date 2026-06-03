from datetime import date
from typing import Literal, Protocol

from pydantic import BaseModel, Field

from app.entities import CreateTask, StatusTask, Task


class DateFilter(BaseModel):
    order_by: Literal["newest", "oldest"]
    as_date: date


class FilterTask(BaseModel):
    user_id: set[int] = set()
    name: str | None = None
    date_filter: DateFilter | None = None
    status: set[StatusTask] = set()


class PaginationTask(BaseModel):
    limit: int = Field(ge=0)
    offset: int = Field(ge=0)


class TaskRepositoryProtocol(Protocol):
    def create(self, task: CreateTask) -> Task: ...
    def get_by_id(self, id: int) -> Task | None: ...
    def get_by_filter(
        self,
        filter: FilterTask,
        pagination: PaginationTask,
    ) -> list[Task]: ...
    def get_count_filter(self, filter: FilterTask) -> int: ...
    def update(self, task: Task) -> Task | None: ...
    def delete(self, id: int) -> bool: ...
