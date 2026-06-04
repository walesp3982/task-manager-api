from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

from app.api.depends.services import UserServiceDep
from app.api.depends.user import PayloadDep
from app.entities import Role, User
from app.exceptions.user_exceptions import UserNotFoundById

router = APIRouter()


class UserInfo(BaseModel):
    id: int
    name: str
    email: str
    role: Role

    @classmethod
    def from_entity(cls, user: User) -> "UserInfo":
        return cls(
            id=user.id,
            name=user.name,
            email=user.email,
            role=user.role,
        )


@router.get("/me")
def user_info(payload: PayloadDep, service: UserServiceDep) -> UserInfo:
    try:
        user = service.get_by_id(int(payload.sub))
        return UserInfo.from_entity(user=user)

    except UserNotFoundById:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
