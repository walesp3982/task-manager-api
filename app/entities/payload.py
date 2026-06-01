from pydantic import BaseModel, Field

from app.entities.user import Role


class BuildPayload(BaseModel):
    id: int = Field(ge=1)
    name: str
    role: Role


class Payload(BaseModel):
    sub: int = Field(ge=1)
    name: str
    role: Role
    iat: int
    exp: int
