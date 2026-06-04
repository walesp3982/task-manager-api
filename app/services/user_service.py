from app.entities import User
from app.exceptions.user_exceptions import UserNotFoundById
from app.repository.protocol import user


class UserService:
    def __init__(self, user_repository: user.UserRepositoryProtocol):
        self._user_repo = user_repository

    def get_by_id(self, id: int) -> User:
        """
        Get a user by id

        Args:
            id: identifier for user in repository

        Return:
            (User) entity that represents a user in the system

        Raises:
            UserNotFoundById
        """
        user = self._user_repo.get_by_id(id)

        if user is None:
            raise UserNotFoundById(id)

        return user
