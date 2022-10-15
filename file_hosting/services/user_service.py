from typing import Iterable

from database.repositories.user_repository import UserRepository, UserRepr

from .base import ServiceBase
from .exceptions import user_exc


class UserService(ServiceBase[UserRepository, UserRepr]):
    def _get_user_or_raise_exc(self, id_: int) -> UserRepr:
        user = self._repository.get_by_id(id_)

        if user is None:
            raise user_exc.UserNotFound

        return user

    def get(self, id_: int) -> UserRepr:
        return self._get_user_or_raise_exc(id_)

    def get_all(self, offset: int = 0, limit: int = 100) -> Iterable[UserRepr]:
        return self._repository.get_all()

    def create(self, user_repr: UserRepr) -> UserRepr:
        if self._repository.get_by_username(user_repr.username):
            raise user_exc.UserWithUsernameExist

        if self._repository.get_by_email(user_repr.email):
            raise user_exc.UserWithEmailExist

        return self._repository.create(user_repr)

    def delete(self, id_) -> None:
        user = self._get_user_or_raise_exc(id_)

        self._repository.delete(user.id)
