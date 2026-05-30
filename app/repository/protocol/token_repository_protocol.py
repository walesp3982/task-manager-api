from datetime import date
from typing import Protocol

from pydantic import BaseModel, Field

from app.entities import CreateToken, Token


class PaginationToken(BaseModel):
    limit: int = Field(ge=0)
    offset: int = Field(ge=0)


class TokenRepositoryProtocol(Protocol):
    def create(self, token: CreateToken) -> Token: ...
    def get_by_id(self, id: int) -> Token | None: ...
    def get_by_token(self, token_str: str) -> Token | None: ...
    def get_all_expired(
        self,
        date_now: date,
        pagination: PaginationToken,
    ) -> list[Token]: ...

    def count_all_expired(self, date_now: date) -> int: ...
    def update(self, token: Token) -> Token | None: ...
    def delete(self, id: int) -> bool: ...
