from typing import Iterable
from uuid import UUID

from database.repositories.directory_repository import \
    DirectoryRepository, DirectoryRepr
from database.repositories.user_repository import UserRepository, UserRepr
from database.repositories.file_repository import FileRepository, FileRepr

from .base import ServiceBase
from .exceptions import user_exc, directory_exc, file_exc


class FileService(ServiceBase[FileRepository, FileRepr]):
    def __init__(
            self, repository: FileRepository,
            user_repository: UserRepository,
            directory_repository: DirectoryRepository
    ) -> None:
        self._user_repository = user_repository
        self._directory_repository = directory_repository

        super().__init__(repository)

    def _get_user_or_raise_exc(self, user_id: int) -> UserRepr:
        user = self._user_repository.get_by_id(user_id)

        if user is None:
            raise user_exc.UserNotFound

        return user

    def _get_directory_or_raise_exc(
            self, user_id: int, directory_id: int
    ) -> DirectoryRepr:
        directory = self._directory_repository.get_by_id(user_id, directory_id)

        if directory is None:
            raise directory_exc.DirectoryNotFound

        return directory

    def _raise_exc_if_user_or_directory_is_none(
            self, user_id: int, directory_id: int
    ) -> None:
        self._get_user_or_raise_exc(user_id)
        self._get_directory_or_raise_exc(user_id, directory_id)

    def _get_file_or_raise_exc(
            self, user_id: int, directory_id: int, file_id: UUID
    ):
        file = self._repository.get_by_id(
            user_id, directory_id, file_id
        )

        if file is None:
            raise file_exc.FileNotFound

        return file

    def get(
            self, user_id: int, directory_id: int, file_id: UUID
    ) -> FileRepr:
        """Raises: UserNotFound, DirectoryNotFound, FileNotFound"""

        self._raise_exc_if_user_or_directory_is_none(user_id, directory_id)

        return self._get_file_or_raise_exc(
            user_id, directory_id, file_id
        )

    def get_all(
            self, user_id: int, directory_id: int,
            offset: int = 0, limit: int = 100
    ) -> Iterable[FileRepr]:
        """Raises: UserNotFound, DirectoryNotFound"""

        self._raise_exc_if_user_or_directory_is_none(user_id, directory_id)

        return self._repository.get_all(user_id, directory_id, offset, limit)

    def create(self, user_id: int, file_repr: FileRepr) -> FileRepr:
        """Raises: UserNotFound, DirectoryNotFound"""

        self._raise_exc_if_user_or_directory_is_none(
            user_id, file_repr.directory_id
        )

        return self._repository.create(file_repr)

    def delete(
            self, user_id: int, directory_id: int, file_id: UUID
    ) -> None:
        """Raises: UserNotFound, DirectoryNotFound, FileNotFound"""

        self._raise_exc_if_user_or_directory_is_none(user_id, directory_id)

        self._repository.delete(file_id)
