from datetime import datetime

from pydantic import BaseModel


class Token(BaseModel):
    id: int
    user_id: int
    token: str
    expires_at: datetime


class CreateToken(BaseModel):
    user_id: int
    token: str
    expires_at: datetime
