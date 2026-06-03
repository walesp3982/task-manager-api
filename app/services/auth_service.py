from app.entities import CreateToken, Token, User
from app.entities.payload import Payload
from app.exceptions.auth_exception import InvalidCredencials
from app.exceptions.token_exception import TokenExpired, TokenNotFound
from app.exceptions.user_exceptions import UserNotFoundByEmail, UserNotFoundById
from app.repository.protocol import token, user
from app.services import JWTService


class AuthService:
    def __init__(
        self,
        user_repository: user.UserRepositoryProtocol,
        token_repository: token.TokenRepositoryProtocol,
        jwt_service: JWTService,
        user_session_time: int,
        token_session_time: int,
    ):
        """
        user_session_time: in minutes

        token_session_time: in minutes
        """
        self._user_repository = user_repository
        self._token_repository = token_repository
        self._jwt_service = jwt_service
        self._user_session_minutes = user_session_time
        self._token_session_minutes = token_session_time

    def generate_access_token(self, user: User) -> str:
        """
        Get a access_token through the id of user

        Args:
            user: type(User) object represents a user
            who access to system

        Return:
            (str) access_token
        """

        # Generate token and hashed_token
        str_token = Token.generate_token()
        hashed_token = Token.encript_token(str_token)

        new_token = CreateToken(
            token=hashed_token,
            user_id=user.id,
            expires_at=Token.get_datetime_expired(self._user_session_minutes),
        )

        # Save new token
        self._token_repository.create(new_token)

        # Return access token
        return str_token

    def generate_refresh_token(self, token_str: str) -> str:
        """
        Generate a refresh token through of a token_str

        Args:
            token_str: Access token in the repository

        Return:
            type str: The jwt token with all information of user
        """
        token_hash = Token.encript_token(token_str)
        token: Token | None = self._token_repository.get_by_token(token_str=token_hash)

        if token is None:
            raise TokenNotFound

        if token_hash != token.token:
            raise ValueError("Token aren't not equals")

        if token.is_expired():
            raise TokenExpired()
        # Get user data for fill Payload
        user = self._user_repository.get_by_id(token.user_id)
        if user is None:
            raise UserNotFoundById(token.user_id)

        # Creating payload
        payload = Payload.create(
            sub=str(user.id),
            name=user.name,
            role=user.role,
            minutes_expired=self._token_session_minutes,
        )

        return self._jwt_service.encode(payload)

    def logout(self, token_str: str):
        """
        Close Session of user and delete the token the repository
        """
        token: Token | None = self._token_repository.get_by_token(token_str)

        if token is None:
            raise TokenNotFound

        if not self._token_repository.delete(token.id):
            raise TokenNotFound

    def login(self, email: str, password: str) -> tuple[str, str]:
        """
        Method about funcionality is:

        1) Generate a access token and save and repository.
        2) Generate a refresh token to base a access token.

        Returns:
            (access_token, refresh_token) -> type (str, str)
        """
        user = self._user_repository.get_by_email(email=email)

        # user = None raise Exception
        if user is None:
            raise UserNotFoundByEmail(email=email)

        # Verification password
        if not user.verify_password(password):
            raise InvalidCredencials()

        access_token = self.generate_access_token(user)
        refresh_token = self.generate_refresh_token(access_token)

        return (access_token, refresh_token)
