from datetime import date
from typing import Literal, Protocol

from pydantic import BaseModel, Field

from app.entities import CreateReminder, Reminder


class PaginationReminder(BaseModel):
    offset: int = Field(ge=0)
    limit: int = Field(ge=0)


class FilterReminder(BaseModel):
    """
    - task_id: Filtrado de la tarea respectiva para varias tareas
    - done: Si el recordatorio fue ya registrado
    - min_date: Fecha minima del recordatorio
    - max_date: Fecha máxima del recordatorio
    - order_by: Order respecto al trigger_date
    """

    task_id: set[int] = set()
    done: bool | None = None
    min_date: date | None = None
    max_date: date | None = None
    order_by: Literal["asc", "desc"] = "asc"


class ReminderRepositoryProtocol(Protocol):
    def create(self, reminder: CreateReminder) -> Reminder: ...
    def get_by_id(self, id: int) -> Reminder | None: ...
    def get_all_filter(
        self, filter: FilterReminder, pagination: PaginationReminder
    ) -> list[Reminder]: ...
    def count_all_filter(self, filter: FilterReminder) -> int: ...
    def update(self, reminder: Reminder) -> Reminder | None: ...
    def delete(self, id: int) -> bool: ...
