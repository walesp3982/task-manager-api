import jwt

from app.entities import Payload
from app.exceptions import auth


class JWTService:
    def __init__(self, secret: str):
        self._secret = secret

    def encode(self, payload: Payload) -> str:
        encoded = jwt.encode(payload.model_dump(), self._secret, algorithm="HS256")
        return encoded

    def decode(self, encode: str) -> Payload:
        try:
            decode = jwt.decode(encode, self._secret, algorithms=["HS256"], leeway=10)
            return Payload(**decode)
        except jwt.ExpiredSignatureError:
            raise auth.AuthorizationExpired()
