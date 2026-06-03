from datetime import datetime, timedelta, timezone

from pydantic import BaseModel

from app.entities.user import Role


class Payload(BaseModel):
    sub: str
    name: str
    role: Role
    iat: int
    exp: int

    @classmethod
    def create(cls, sub: str, name: str, role: Role, minutes_expired: int):
        return cls(
            sub=sub,
            name=name,
            role=role,
            iat=cls.get_expired_datetime(minutes_expired),
            exp=cls.get_actual_datetime(),
        )

    @staticmethod
    def get_expired_datetime(minutes: int):
        datetime_expired = datetime.now(timezone.utc) + timedelta(minutes=minutes)

        return int(datetime_expired.timestamp())

    @staticmethod
    def get_actual_datetime():
        now_datetime = datetime.now(timezone.utc)

        return int(now_datetime.timestamp())
