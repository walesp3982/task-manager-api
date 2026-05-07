from datetime import datetime
from typing import TYPE_CHECKING

from pydantic import BaseModel

if TYPE_CHECKING:
    from app.entities.user import User


class Token(BaseModel):
    id: int
    user_id: int
    token: str
    expires_at: datetime


class CreateToken(BaseModel):
    user_id: int
    token: str
    expires_at: datetime


class TokenWithUser(Token):
    user: User
