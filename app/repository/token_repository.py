from datetime import date

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.entities import CreateToken, Token
from app.models import TokenModel

from .protocol import token


class TokenRepository:
    def __init__(self, session: Session):
        self._session = session

    def create(self, token: CreateToken) -> Token:
        new_token = TokenModel(token)

        self._session.add(new_token)
        self._session.commit()
        self._session.refresh(new_token)
        return new_token.get_entity()

    def get_by_id(self, id: int) -> Token | None:
        token = self._session.get(TokenModel, id)
        return None if token is None else token.get_entity()

    def get_by_token(self, token_str: str) -> Token | None:
        stmt = select(TokenModel).where(TokenModel.token == token_str)

        token = self._session.scalar(stmt)

        return None if token is None else token.get_entity()

    def get_all_expired(
        self, date_now: date, pagination: token.PaginationToken
    ) -> list[Token]:
        stmt = (
            select(TokenModel)
            .where(TokenModel.expires_at < date_now)
            .limit(pagination.limit)
            .offset(pagination.offset)
        )

        tokens = self._session.scalars(stmt)

        return [token.get_entity() for token in tokens]

    def count_all_expired(self, date_now: date) -> int:
        stmt = (
            select(func.count())
            .select_from(TokenModel)
            .where(TokenModel.expires_at < date_now)
        )

        count = self._session.scalar(stmt)

        return 0 if count is None else count

    def update(self, token: Token) -> Token | None:
        token_db = self._session.get(TokenModel, token.id)

        if token_db is None:
            return None

        token_db.user_id = token.user_id
        token_db.expires_at = token.expires_at
        token_db.token = token.token

        self._session.commit()
        self._session.refresh(token_db)

        return token_db.get_entity()

    def delete(self, id: int) -> bool:
        token = self._session.get(TokenModel, id)

        if token is None:
            return False

        self._session.delete(token)
        self._session.commit()

        return True
