from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from app.api.depends.services import JwtServiceDep
from app.entities import Payload
from app.exceptions.auth_exception import AuthorizationExpired

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_payload(
    token: Annotated[str, Depends(oauth2_scheme)], jwt_service: JwtServiceDep
) -> Payload:
    try:
        payload = jwt_service.decode(token)
        return payload
    except AuthorizationExpired:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Access Token expired",
        )


PayloadDep = Annotated[Payload, Depends(get_payload)]
