from datetime import datetime, timedelta, timezone
from unittest.mock import MagicMock, Mock, create_autospec, patch

import pytest

from app.entities import CreateUserDTO, Role, Token, User
from app.exceptions.auth_exception import InvalidCredencials
from app.exceptions.token_exception import TokenExpired, TokenNotFound
from app.exceptions.user_exceptions import DuplicateUser, UserNotFoundByEmail
from app.repository.protocol.token_repository_protocol import TokenRepositoryProtocol
from app.repository.protocol.user_repository_interface import UserRepositoryProtocol
from app.services import JWTService
from app.services.auth_service import AuthService


@pytest.fixture
def user_repo() -> Mock:
    return create_autospec(UserRepositoryProtocol)


@pytest.fixture
def token_repo() -> Mock:
    return create_autospec(TokenRepositoryProtocol)


@pytest.fixture
def jwt_service() -> Mock:
    return create_autospec(JWTService)


@pytest.fixture
def service(
    user_repo: MagicMock,
    token_repo: MagicMock,
    jwt_service: MagicMock,
) -> AuthService:
    return AuthService(
        user_repository=user_repo,
        token_repository=token_repo,
        jwt_service=jwt_service,
        token_session_time=30,
        user_session_time=30,
    )


@patch("app.services.auth_service.Token.get_datetime_expired")
@patch("app.services.auth_service.Token.encript_token")
@patch("app.services.auth_service.Token.generate_token")
def test_generate_access_token(
    mock_generate: MagicMock,
    mock_encript: MagicMock,
    mock_get_datetime: MagicMock,
    service: AuthService,
    token_repo: MagicMock,
):
    user = User(
        id=1, name="jhon", email="jhon@gmail.com", password="password", role=Role.client
    )

    fake_datetime = datetime(2025, 1, 1, tzinfo=timezone.utc)
    mock_generate.return_value = "raw_token_123"
    mock_encript.return_value = "hashed_token_abc"
    mock_get_datetime.return_value = fake_datetime

    result = service.generate_refresh_token(user)

    assert result == "raw_token_123"
    mock_generate.assert_called_once()
    mock_encript.assert_called_once_with("raw_token_123")
    mock_get_datetime.assert_called_once_with(service._user_session_minutes)

    token_repo.create.assert_called_once()

    created_token = token_repo.create.call_args[0][0]
    assert created_token.token == "hashed_token_abc"
    assert created_token.user_id == 1


@patch("app.entities.Token.encript_token")
def test_generate_refresh_token(
    encript_token: MagicMock,
    token_repo: MagicMock,
    service: AuthService,
    user_repo: MagicMock,
    jwt_service: Mock,
):
    encript_token.return_value = "hash_token"

    token_repo.get_by_token.return_value = Token(
        expires_at=(datetime.now(timezone.utc) + timedelta(days=3)),
        id=1,
        token="hash_token",
        user_id=1,
    )

    user_repo.get_by_id.return_value = User(
        email="jhon@gmail.com",
        name="Jhon",
        id=1,
        password="password",
        role=Role.client,
    )

    jwt_service.encode.return_value = "token_jwt"
    result = service.generate_access_token("token")
    assert result == "token_jwt"


@patch("app.entities.Token.encript_token")
def test_generate_refresh_token_not_found_access_token(
    encript_token: MagicMock,
    token_repo: MagicMock,
    service: AuthService,
    user_repo: MagicMock,
):
    encript_token.return_value = "hash_token"

    token_repo.get_by_token.return_value = None

    with pytest.raises(TokenNotFound):
        service.generate_access_token("token")

    user_repo.get_by_id.assert_not_called()


@patch("app.entities.Token.encript_token")
def test_generate_refresh_token_if_access_token_is_expired(
    encript_token: MagicMock, service: AuthService, token_repo: Mock
):
    encript_token.return_value = "hash_token"

    # Create a token expired with 5 minutes
    token_repo.get_by_token.return_value = Token(
        id=1,
        user_id=1,
        token="hash_token",
        expires_at=datetime.now(timezone.utc) - timedelta(minutes=5),
    )

    with pytest.raises(TokenExpired):
        service.generate_access_token("token_str")


def test_logout(service: AuthService, token_repo: Mock):
    token_repo.get_by_token.return_value = Token(
        id=1,
        expires_at=datetime.now(timezone.utc) + timedelta(minutes=5),
        token="my_hash_token",
        user_id=1,
    )

    token_repo.delete.return_value = True

    service.logout("my_token")


def test_login_process(service: AuthService, user_repo: Mock):
    mock_user = create_autospec(User, instance=True)
    mock_user.verify_password.return_value = True

    user_repo.get_by_email.return_value = mock_user

    with (
        patch.object(
            service, "generate_access_token", return_value="fake_token_access"
        ) as mock_access,
        patch.object(
            service, "generate_refresh_token", return_value="fake_token_refresh"
        ) as mock_refresh,
    ):
        access, refresh = service.login("j@gmail.com", "password123")

        assert access == "fake_token_access"
        assert refresh == "fake_token_refresh"

        mock_refresh.assert_called_once_with(mock_user)
        mock_access.assert_called_once_with("fake_token_refresh")


def test_login_but_user_email_not_found(service: AuthService, user_repo: Mock):
    user_repo.get_by_email.return_value = None

    with pytest.raises(UserNotFoundByEmail):
        service.login("j@gmail.com", "password")


def test_login_but_user_password_verification_incorrect(
    service: AuthService, user_repo: Mock
):
    mock_user = create_autospec(User, instance=True)
    mock_user.verify_password.return_value = False

    user_repo.get_by_email.return_value = mock_user

    with pytest.raises(InvalidCredencials):
        service.login(email="j@gmail.com", password="password")


@patch("app.entities.user.User.hash_password")
def test_register_new_user(hash_password: Mock, service: AuthService, user_repo: Mock):
    user_repo.get_by_email.return_value = None
    result_user = User(
        id=1,
        name="john",
        email="j@gmail.com",
        password="hash_password",
        role=Role.client,
    )

    user_repo.create.return_value = result_user

    hash_password.return_value = "hash_password"

    dto_test = CreateUserDTO(
        email="j@gmail.com",
        password="plain_password",
        name="john",
        role=Role.client,
    )

    user = service.register_new_user(dto_test)
    assert user == result_user

    user_repo.get_by_email.assert_called_once_with(dto_test.email)

    hash_password.assert_called_once_with("plain_password")

    user_repo.create.assert_called_once_with(dto_test)


def test_register_new_user_if_email_has_register_before(
    service: AuthService,
    user_repo: Mock,
):
    user_mock = create_autospec(User, instance=True)
    dto_mock = create_autospec(CreateUserDTO, instance=True)
    dto_mock.email = "mail@mail.com"
    user_repo.get_by_email.return_value = user_mock

    with pytest.raises(DuplicateUser):
        service.register_new_user(dto_mock)
