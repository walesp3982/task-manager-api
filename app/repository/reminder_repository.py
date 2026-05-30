from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.entities import CreateReminder, Reminder
from app.models import ReminderModel

from .protocol import reminder


class ReminderRepository:
    def __init__(self, session: Session):
        self._session = session

    def create(self, reminder: CreateReminder) -> Reminder:
        new_reminder = ReminderModel(reminder)

        self._session.add(new_reminder)
        self._session.commit()
        return new_reminder.get_entity()

    def get_by_id(self, id: int) -> Reminder | None:
        reminder = self._session.get(ReminderModel, id)
        return None if reminder is None else reminder.get_entity()

    def get_all_filter(
        self, filter: reminder.FilterReminder, pagination: reminder.PaginationReminder
    ) -> list[Reminder]:
        stmt = select(ReminderModel).limit(pagination.limit).offset(pagination.offset)

        if filter.done is not None:
            if filter.done:
                stmt = stmt.where(ReminderModel.done.is_(True))
            else:
                stmt = stmt.where(ReminderModel.done.is_(False))
        if filter.min_date is not None:
            stmt = stmt.where(ReminderModel.trigger_date >= filter.min_date)
        if filter.max_date is not None:
            stmt = stmt.where(ReminderModel.trigger_date <= filter.max_date)
        if filter.order_by == "asc":
            stmt = stmt.order_by(ReminderModel.trigger_date.asc())
        if filter.order_by == "desc":
            stmt = stmt.order_by(ReminderModel.trigger_date.desc())
        if len(filter.task_id) != 0:
            stmt = stmt.where(ReminderModel.task_id.in_(filter.task_id))

        reminders = self._session.scalars(stmt)
        return [reminder.get_entity() for reminder in reminders]

    def count_all_filter(self, filter: reminder.FilterReminder) -> int:
        stmt = select(func.count()).select_from(ReminderModel)

        if filter.done is not None:
            if filter.done:
                stmt = stmt.where(ReminderModel.done.is_(True))
            else:
                stmt = stmt.where(ReminderModel.done.is_(False))
        if filter.min_date is not None:
            stmt = stmt.where(ReminderModel.trigger_date >= filter.min_date)
        if filter.max_date is not None:
            stmt = stmt.where(ReminderModel.trigger_date <= filter.max_date)
        if filter.order_by == "asc":
            stmt = stmt.order_by(ReminderModel.trigger_date.asc())
        if filter.order_by == "desc":
            stmt = stmt.order_by(ReminderModel.trigger_date.desc())
        if len(filter.task_id) != 0:
            stmt = stmt.where(ReminderModel.task_id.in_(filter.task_id))

        count = self._session.scalar(stmt)

        return 0 if count is None else count

    def update(self, reminder: Reminder) -> Reminder | None:
        reminder_db = self._session.get(ReminderModel, reminder.id)

        if reminder_db is None:
            return reminder_db

        reminder_db.done = reminder.done
        reminder_db.task_id = reminder.task_id
        reminder_db.timestamp_done = reminder.timestamp_done
        reminder_db.trigger_date = reminder.trigger_date

        self._session.commit()
        self._session.refresh(reminder_db)

        return reminder_db.get_entity()

    def delete(self, id: int) -> bool:
        reminder = self._session.get(ReminderModel, id)

        if reminder is None:
            return False

        self._session.delete(reminder)
        self._session.commit()

        return True
