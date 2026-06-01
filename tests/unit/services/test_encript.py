import pytest

from app.services import EncriptService


@pytest.fixture
def encript_service() -> EncriptService:
    return EncriptService()


def test_encript(encript_service: EncriptService):
    password = "password1234"

    # Work the encriptation
    hash = encript_service.encript(password)

    assert len(hash) > 0
    assert isinstance(hash, str)

    # Verify the encriptation
    assert encript_service.verify(hash, password)
