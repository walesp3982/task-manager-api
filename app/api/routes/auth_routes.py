from typing import Annotated, Literal

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr

from app.api.depends.services import AuthServiceDep
from app.entities import CreateUserDTO, Role, User
from app.exceptions.auth_exception import InvalidCredencials
from app.exceptions.token_exception import TokenExpired, TokenNotFound
from app.exceptions.user_exceptions import DuplicateUser, UserNotFoundByEmail

router = APIRouter(prefix="/auth")


class RegisterClient(BaseModel):
    name: str
    email: EmailStr
    password: str

    def get_create_user_dto(self) -> CreateUserDTO:
        return CreateUserDTO(
            email=self.email,
            name=self.name,
            password=self.password,
            role=Role.client,
        )


class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    role: Role

    @classmethod
    def from_entity(cls, user: User):
        return cls(id=user.id, name=user.name, email=user.email, role=user.role)


@router.post("/register")
def register_client(client: RegisterClient, service: AuthServiceDep) -> UserResponse:
    try:
        user = service.register_new_user(client.get_create_user_dto())

        return UserResponse.from_entity(user)

    except DuplicateUser:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="cannot creating user, email has exist in the system",
        )


class LoginResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: Literal["bearer"]


@router.post("/login")
def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], service: AuthServiceDep
) -> LoginResponse:
    try:
        (access_token, refresh_token) = service.login(
            form_data.username, form_data.password
        )
        return LoginResponse(
            access_token=access_token, refresh_token=refresh_token, token_type="bearer"
        )
    except (UserNotFoundByEmail, InvalidCredencials):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )


class RefreshRequest(BaseModel):
    token: str


class RefreshResponse(BaseModel):
    token: str


@router.post("/refresh")
def get_another_refresh_token(token: str, service: AuthServiceDep) -> RefreshResponse:
    try:
        new_refresh_token = service.generate_access_token(token)
        return RefreshResponse(token=new_refresh_token)
    except (TokenNotFound, TokenExpired):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Access Token invalid",
        )


class AccessTokenResquest(BaseModel):
    token: str


@router.post("/logout")
def logout_user_session(request: AccessTokenResquest, service: AuthServiceDep) -> None:
    try:
        service.logout(request.token)
        return None
    except TokenNotFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Access Token not found"
        )
