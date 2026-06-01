from pydantic import BaseModel, Field

from app.entities.user import Role


class Payload(BaseModel):
    sub: str = Field(min_length=1)
    name: str
    role: Role
    iat: int
    exp: int
