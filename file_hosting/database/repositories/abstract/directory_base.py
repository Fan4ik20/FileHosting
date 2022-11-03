from abc import ABC, abstractmethod
from typing import Iterable

from database.models import Directory as DirectoryModel
from database.repositories.dto import \
    DirectoryDTO, DirectoryCreateDTO, DirectoryUpdateDTO

from ..converters import DirectoryConverter

from .base import BaseRepository


__all__ = ['ADirectoryRepository']


class ADirectoryRepository(
    ABC, BaseRepository[
        DirectoryModel, DirectoryCreateDTO, DirectoryDTO, DirectoryUpdateDTO, DirectoryConverter
    ]
):
    @abstractmethod
    def get_by_id(
            self, user_id: int, directory_id: int
    ) -> DirectoryDTO | None:
        pass

    @abstractmethod
    def get_by_id_with_related(
            self, user_id: int, id_: int
    ) -> DirectoryDTO | None:
        pass

    @abstractmethod
    def get_by_name(
            self, user_id: int, name: str, out_directory_id: int | None = None
    ) -> DirectoryDTO | None:
        pass

    @abstractmethod
    def get_all_without_parent(
            self, user_id: int, offset: int = 0, limit: int = 100
    ) -> Iterable[DirectoryDTO]:
        pass

    @abstractmethod
    def get_all(
            self, user_id: int, offset: int = 0, limit: int = 100
    ) -> Iterable[DirectoryDTO]:
        pass

    @abstractmethod
    def delete(self, id_: int) -> None:
        pass

    @abstractmethod
    def update(
            self, user_id: int, id_: int, dir_repr: DirectoryUpdateDTO
    ) -> DirectoryDTO | None:
        pass
