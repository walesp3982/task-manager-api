from typing import Protocol

from pydantic import BaseModel, Field

from app.entities import CreateUserDTO, User


class FilterUser(BaseModel):
    query_name: str | None = None
    query_email: str | None = None


class PaginationUser(BaseModel):
    """
    The pagination is OFFSET/LIMIT
    """

    limit: int = Field(ge=0)
    offset: int = Field(ge=0)


class UserRepositoryProtocol(Protocol):
    def create(self, user: CreateUserDTO) -> User: ...
    def get_by_id(self, id: int) -> User | None: ...
    def get_by_email(self, email: str) -> User | None: ...
    def get_by_filter(
        self, filter: FilterUser, pagination: PaginationUser
    ) -> list[User]: ...
    def count_by_filter(self, filter: FilterUser) -> int: ...
    def update(self, user: User) -> User | None: ...
    def delete(self, id: int) -> bool: ...
