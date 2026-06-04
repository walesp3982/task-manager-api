from typing import Annotated

from fastapi import Depends

from app.api.depends.repository import TokenRepositoryDep, UserRepositoryDep
from app.services import AuthService, JWTService
from app.services.user_service import UserService
from app.settings.app import AppSettings
from app.settings.jwt import JWTSettings


def jwt_service() -> JWTService:
    settings = JWTSettings()
    return JWTService(secret=settings.SECRET)


JwtServiceDep = Annotated[JWTService, Depends(jwt_service)]


def get_auth_service(
    token_repo: TokenRepositoryDep,
    user_repo: UserRepositoryDep,
    jwt_service: JwtServiceDep,
) -> AuthService:
    app_settings = AppSettings()
    return AuthService(
        jwt_service=jwt_service,
        token_repository=token_repo,
        user_repository=user_repo,
        token_session_time=app_settings.TIME_USER_TOKEN,
        user_session_time=app_settings.TIME_USER_SESSION,
    )


AuthServiceDep = Annotated[AuthService, Depends(get_auth_service)]


def get_user_service(user_repo: UserRepositoryDep) -> UserService:
    return UserService(user_repo)


UserServiceDep = Annotated[UserService, Depends(get_user_service)]
