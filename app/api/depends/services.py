from typing import Annotated

from fastapi import Depends

from app.services import JWTService
from app.settings.jwt import JWTSettings


def jwt_service() -> JWTService:
    settings = JWTSettings()
    return JWTService(secret=settings.SECRET)


JwtServiceDep = Annotated[JWTService, Depends(jwt_service)]
