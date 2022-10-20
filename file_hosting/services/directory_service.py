from typing import Iterable

from database.repositories.directory_repository import DirectoryRepr
from database.repositories.user_repository import UserRepr

from services.abstract.directory_base import ADirectoryService
from .exceptions import user_exc, directory_exc


class DirectoryService(ADirectoryService):
    def _get_user_or_raise_exc(self, user_id: int) -> UserRepr:
        user = self._user_repository.get_by_id(user_id)

        if user is None:
            raise user_exc.UserNotFound

        return user

    def _get_directory_or_raise_exc(
            self, user_id: int, directory_id: int, with_inner: bool = False
    ) -> DirectoryRepr:
        directory = (
            self._repository.get_by_id(user_id, directory_id) if not with_inner
            else self._repository.get_by_id_with_inner(user_id, directory_id)
        )

        if directory is None:
            raise directory_exc.DirectoryNotFound

        return directory

    def get(
            self, user_id: int, directory_id: int,
            with_inner: bool = False
    ) -> DirectoryRepr:
        """Raises: UserNotFound, DirectoryNotFound"""

        self._get_user_or_raise_exc(user_id)

        return self._get_directory_or_raise_exc(
            user_id, directory_id, with_inner
        )

    def get_all(
            self, user_id: int, offset: int = 0, limit: int = 100,
    ) -> Iterable[DirectoryRepr]:
        """Raises: UserNotFound"""

        self._get_user_or_raise_exc(user_id)

        return self._repository.get_all(user_id, offset, limit)

    def create(self, directory_repr: DirectoryRepr) -> DirectoryRepr:
        """Raises: UserNotFound, DirectoryWithNameAlreadyExist"""

        self._get_user_or_raise_exc(directory_repr.user_id)

        if self._repository.get_by_name(
                directory_repr.user_id, directory_repr.name
        ):
            raise directory_exc.DirectoryWithNameAlreadyExist

        return self._repository.create(directory_repr)

    def delete(self, user_id: int, directory_id: int) -> None:
        """Raises: UserNotFound, DirectoryNotFound"""

        self._get_user_or_raise_exc(user_id)
        directory = self._get_directory_or_raise_exc(user_id, directory_id)

        self._repository.delete(directory.id)
