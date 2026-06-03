import hashlib
import secrets
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone

from pydantic import BaseModel


@dataclass
class Token:
    id: int
    user_id: int
    token: str
    expires_at: datetime

    def is_expired(self):
        return datetime.now(timezone.utc) > self.expires_at

    @staticmethod
    def generate_token() -> str:
        return secrets.token_urlsafe(32)

    @staticmethod
    def encript_token(token: str) -> str:
        return hashlib.sha256(token.encode()).hexdigest()

    @staticmethod
    def get_datetime_expired(minutes: int) -> datetime:
        return datetime.now(timezone.utc) + timedelta(minutes=minutes)


class CreateToken(BaseModel):
    user_id: int
    token: str
    expires_at: datetime
