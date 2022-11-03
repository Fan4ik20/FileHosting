from typing import Iterable

from database.repositories.dto import UserDTO, UserCreateDTO

from common.utils.passwords import get_password_hash

from .abstract.user_base import AUserService
from .exceptions import user_exc


__all__ = ['UserService']


class UserService(AUserService):
    def _get_user_or_raise_exc(self, id_: int) -> UserDTO:
        user = self._repository.get_by_id(id_)

        if user is None:
            raise user_exc.UserNotFound

        return user

    def get(self, id_: int) -> UserDTO:
        """Raises: UserNotFound"""

        return self._get_user_or_raise_exc(id_)

    def get_by_username(self, username: str) -> UserDTO:
        """Raises: UserNotFound"""

        user = self._repository.get_by_username(username)

        if user is None:
            raise user_exc.UserNotFound

        return user

    def get_by_email(self, email: str) -> UserDTO:
        """Raises: UserNotFound"""

        user = self._repository.get_by_email(email)

        if user is None:
            raise user_exc.UserNotFound

        return user

    def get_all(self, offset: int = 0, limit: int = 100) -> Iterable[UserDTO]:
        return self._repository.get_all()

    def create(self, user_repr: UserCreateDTO) -> UserDTO:
        """Raises: UserWithUsernameExist, UserWithEmailExist"""

        if self._repository.get_by_username(user_repr.username):
            raise user_exc.UserWithUsernameExist

        if self._repository.get_by_email(user_repr.email):
            raise user_exc.UserWithEmailExist

        user_repr.password = get_password_hash(user_repr.password)

        return self._repository.create(user_repr)

    def delete(self, id_: int) -> None:
        """Raises: UserNotFound"""

        user = self._get_user_or_raise_exc(id_)

        self._repository.delete(user.id)
