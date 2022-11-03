from typing import Iterable

from database.repositories.dto import (
    DirectoryDTO, DirectoryCreateDTO, DirectoryUpdateDTO, UserDTO
)

from .abstract.directory_base import ADirectoryService
from .exceptions import user_exc, directory_exc


__all__ = ['DirectoryService']


class DirectoryService(ADirectoryService):
    def _get_user_or_raise_exc(self, user_id: int) -> UserDTO:
        user = self._user_repository.get_by_id(user_id)

        if user is None:
            raise user_exc.UserNotFound

        return user

    def _get_directory_or_raise_exc(
            self, user_id: int, directory_id: int, related: bool = False
    ) -> DirectoryDTO:
        directory = (
            self._repository.get_by_id(user_id, directory_id) if not related
            else self._repository.get_by_id_with_related(user_id, directory_id)
        )

        if directory is None:
            raise directory_exc.DirectoryNotFound

        return directory

    def get(
            self, user_id: int, directory_id: int,
            related: bool = False
    ) -> DirectoryDTO:
        """Raises: UserNotFound, DirectoryNotFound"""

        self._get_user_or_raise_exc(user_id)

        return self._get_directory_or_raise_exc(
            user_id, directory_id, related=related
        )

    def get_all(
            self, user_id: int, offset: int = 0, limit: int = 100,
    ) -> Iterable[DirectoryDTO]:
        """Raises: UserNotFound"""

        self._get_user_or_raise_exc(user_id)

        return self._repository.get_all_without_parent(user_id, offset, limit)

    def create(self, directory_repr: DirectoryCreateDTO) -> DirectoryDTO:
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

    def update(
            self, user_id: int, directory_id: int,
            dir_repr: DirectoryUpdateDTO
    ) -> DirectoryDTO:
        """Raises: UserNotFound, DirectoryNotFound"""

        self._get_user_or_raise_exc(user_id)

        if dir_repr.name and self._repository.get_by_name(
                user_id, dir_repr.name, dir_repr.directory_id
        ):
            raise directory_exc.DirectoryWithNameAlreadyExist

        updated_directory = self._repository.update(
            user_id, directory_id, dir_repr
        )

        if updated_directory is None:
            raise directory_exc.DirectoryNotFound

        return updated_directory
