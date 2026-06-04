from dataclasses import dataclass
from enum import StrEnum

from pwdlib import PasswordHash
from pydantic import BaseModel


class Role(StrEnum):
    client = "client"
    admin = "admin"


@dataclass
class User:
    id: int
    name: str
    email: str
    password: str
    role: Role

    def verify_password(self, plain_password: str) -> bool:
        password_hash = PasswordHash.recommended()
        return password_hash.verify(plain_password, self.password)

    @staticmethod
    def hash_password(password: str) -> str:
        password_hash = PasswordHash.recommended()
        return password_hash.hash(password)


class CreateUserDTO(BaseModel):
    name: str
    email: str
    password: str
    role: Role
