from enum import StrEnum

from pydantic import BaseModel


class Role(StrEnum):
    client = "client"
    admin = "admin"


class User(BaseModel):
    id: int
    name: str
    email: str
    password: str
    role: Role


class CreateUser(BaseModel):
    name: str
    email: str
    password: str
    role: Role
