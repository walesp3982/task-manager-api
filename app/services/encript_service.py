from pwdlib import PasswordHash


class EncriptService:
    def __init__(self):
        self._password_hash = PasswordHash.recommended()

    def encript(self, content: str) -> str:
        return self._password_hash.hash(content)

    def verify(self, hashed: str, content: str) -> bool:
        return self._password_hash.verify(hashed, content)
