from datetime import datetime, timedelta, timezone

import pytest

from app.entities import Payload, Role
from app.exceptions import auth
from app.services import JWTService

"""
Fixture necessary for this unit testing
"""


@pytest.fixture(scope="module")
def get_jwt_service() -> JWTService:
    from secrets import token_hex

    return JWTService(secret=token_hex(32))


"""
Function built-in for create payload
"""


def built_payload(iat: datetime, exp: datetime) -> Payload:
    return Payload(
        sub="1",
        exp=exp,
        iat=iat,
        name="Jhon",
        role=Role.client,
    )


def normalize_dt(dt: datetime) -> datetime:
    """Trunca microsegundos y normaliza tzinfo a timezone.utc"""
    return dt.replace(microsecond=0, tzinfo=timezone.utc)


def built_actual_payload() -> Payload:
    """
    Create a payload actual
    """
    now = datetime.now(timezone.utc)
    later = now + timedelta(days=3)

    return built_payload(now, later)


def build_expired_payload() -> Payload:
    """
    Create a expired payload
    """
    later = datetime.now(timezone.utc) - timedelta(days=2)
    more_later = later - timedelta(days=4)

    return built_payload(more_later, later)


"""
Starting unit testing
"""


def test_jwt_process(get_jwt_service: JWTService):
    """
    This test work verify the process work correctly

    PROCESS TESTING:
    Payload -> encode -> str -> decode -> Payload

    """
    jwt_service = get_jwt_service

    payload = built_actual_payload()

    token_jwt = jwt_service.encode(payload)

    assert isinstance(token_jwt, str)
    assert len(token_jwt) > 0

    # Starting decode
    # Get a old_payload respectly
    old_payload = jwt_service.decode(encode=token_jwt)

    # Compare the payload before/after of decode
    assert normalize_dt(payload.exp) == normalize_dt(old_payload.exp)
    assert normalize_dt(payload.iat) == normalize_dt(old_payload.iat)


def test_old_jwt(get_jwt_service: JWTService):
    """
    Test if decode method of JWTService work the exception AuthorizationExpired
    exception
    """
    old_payload = build_expired_payload()

    jwt_service = get_jwt_service

    token = jwt_service.encode(old_payload)

    with pytest.raises(auth.AuthorizationExpired):
        jwt_service.decode(token)
