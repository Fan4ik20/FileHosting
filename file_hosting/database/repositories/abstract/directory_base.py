from abc import ABC, abstractmethod

from database.models import Directory as DirectoryModel
from database.repositories.representations import \
    DirectoryRepr, DirectoryReprUpdate
from database.repositories.converters import DirectoryConverter

from .base import BaseRepository


__all__ = ['ADirectoryRepository']


class ADirectoryRepository(
    ABC, BaseRepository[DirectoryModel, DirectoryRepr, DirectoryConverter]
):
    @abstractmethod
    def get_by_id(
            self, user_id: int, directory_id: int
    ) -> DirectoryRepr | None:
        pass

    @abstractmethod
    def get_by_id_with_related(
            self, user_id: int, id_: int
    ) -> DirectoryRepr | None:
        pass

    @abstractmethod
    def get_by_name(
            self, user_id: int, name: str, out_directory_id: int | None = None
    ) -> DirectoryRepr | None:
        pass

    @abstractmethod
    def get_all_without_parent(
            self, user_id: int, offset: int = 0, limit: int = 100
    ) -> list[DirectoryRepr]:
        pass

    @abstractmethod
    def get_all(
            self, user_id: int, offset: int = 0, limit: int = 100
    ) -> list[DirectoryRepr]:
        pass

    @abstractmethod
    def delete(self, id_: int) -> None:
        pass

    @abstractmethod
    def update(
            self, user_id: int, id_: int, dir_repr: DirectoryReprUpdate
    ) -> DirectoryRepr:
        pass
