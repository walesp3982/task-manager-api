from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.entities import CreateTask, Task
from app.models import TaskModel

from .protocol import task


class TaskRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def create(self, task: CreateTask) -> Task:
        new_task = TaskModel(task)

        self._session.add(new_task)
        self._session.commit()
        self._session.refresh(new_task)
        return new_task.get_entity()

    def get_by_id(self, id: int) -> Task | None:
        task = self._session.get(TaskModel, id)
        return None if task is None else task.get_entity()

    def get_by_filter(
        self, filter: task.FilterTask, pagination: task.PaginationTask
    ) -> list[Task]:
        stmt = select(TaskModel).limit(pagination.limit).offset(pagination.offset)

        # Starting the filtering
        if len(filter.user_id) != 0:
            stmt = stmt.where(TaskModel.user_id.in_(filter.user_id))
        if filter.name is not None:
            stmt = stmt.where(TaskModel.name.ilike(f"%{filter.name}%"))
        if len(filter.status) != 0:
            stmt = stmt.where(TaskModel.status._in(filter.status))
        if filter.date_filter is not None:
            if filter.date_filter.order_by == "newest":
                stmt = stmt.order_by(TaskModel.date_limit.desc())
            else:
                stmt = stmt.order_by(TaskModel.date_limit.asc())

        tasks = self._session.scalars(stmt)
        return [task.get_entity() for task in tasks]

    def get_count_filter(self, filter: task.FilterTask) -> int:
        stmt = select(func.count()).select_from(TaskModel)

        # Starting the filtering
        if len(filter.user_id) != 0:
            stmt = stmt.where(TaskModel.user_id.in_(filter.user_id))
        if filter.name is not None:
            stmt = stmt.where(TaskModel.name.ilike(f"%{filter.name}%"))
        if len(filter.status) != 0:
            stmt = stmt.where(TaskModel.status._in(filter.status))
        if filter.date_filter is not None:
            if filter.date_filter.order_by == "newest":
                stmt = stmt.order_by(TaskModel.date_limit.desc())
            else:
                stmt = stmt.order_by(TaskModel.date_limit.asc())

        count = self._session.scalar(stmt)

        return 0 if count is None else count

    def update(self, task: Task) -> Task | None:
        task_db = self._session.get(TaskModel, task.id)

        if task_db is None:
            return None

        task_db.date_limit = task.date_limit
        task_db.name = task.name
        task_db.status = task.status
        task_db.user_id = task.user_id

        self._session.commit()
        self._session.refresh(task_db)
        return task_db.get_entity()

    def delete(self, id: int) -> bool:
        task = self._session.get(TaskModel, id)

        if task is None:
            return False

        self._session.delete(task)
        self._session.commit()
        return True
