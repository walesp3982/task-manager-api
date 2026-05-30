from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.entities import CreateUser, User
from app.models import UserModel

from .protocol import user


class UserRepository:
    def __init__(self, session: Session):
        self._session = session

    def create(self, user: CreateUser) -> User:
        new_user = UserModel(user)
        self._session.add(new_user)
        self._session.commit()
        return new_user.get_entity()

    def get_by_id(self, id: int) -> User | None:
        stmt = select(UserModel).where(UserModel.id == id)
        user = self._session.scalar(stmt)
        return None if user is None else user.get_entity()

    def get_by_email(self, email: str) -> User | None:
        stmt = select(UserModel).where(UserModel.email == email)
        user = self._session.scalar(stmt)
        return None if user is None else user.get_entity()

    def get_by_filter(
        self, filter: user.FilterUser, pagination: user.PaginationUser
    ) -> list[User]:
        stmt = (
            select(UserModel)
            .where(
                UserModel.name.ilike(
                    "%" if filter.query_name is None else f"%{filter.query_name}%"
                ),
                UserModel.email.ilike(
                    "%" if filter.query_email is None else f"%{filter.query_email}%"
                ),
            )
            .limit(pagination.limit)
            .offset(pagination.offset)
        )

        users = self._session.scalars(stmt)

        return [user.get_entity() for user in users]

    def count_by_filter(self, filter: user.FilterUser) -> int:
        stmt = (
            select(func.count())
            .select_from(UserModel)
            .where(
                UserModel.name.ilike(
                    "%" if filter.query_name is None else f"%{filter.query_name}%"
                ),
                UserModel.email.ilike(
                    "%" if filter.query_email is None else f"%{filter.query_name}%"
                ),
            )
        )

        count = self._session.scalar(stmt)
        return 0 if count is None else count

    def update(self, user: User) -> User | None:
        user_db = self._session.get(UserModel, user.id)

        if user_db is None:
            return None

        user_db.name = user.name
        user_db.email = user.email
        user_db.password = user.password
        self._session.commit()
        self._session.refresh(user_db)
        return user_db.get_entity()

    def delete(self, id: int) -> bool:
        user = self._session.get(UserModel, id)

        if not user:
            return False

        self._session.delete(user)
        self._session.commit()

        return True
