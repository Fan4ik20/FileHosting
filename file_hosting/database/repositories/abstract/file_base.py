from abc import ABC, abstractmethod
from uuid import UUID

from database.models import File as FileModel
from database.repositories.representations import FileRepr
from database.repositories.converters import FileConverter

from .base import BaseRepository


__all__ = ['AFileRepository']


class AFileRepository(ABC, BaseRepository[FileModel, FileRepr, FileConverter]):
    @abstractmethod
    def get_by_id(
            self, user_id: int, directory_id: int, file_id: UUID
    ) -> FileRepr | None:
        pass

    @abstractmethod
    def get_all(
            self, user_id: int, directory_id: int,
            offset: int = 0, limit: int = 100
    ) -> list[FileRepr]:
        pass

    @abstractmethod
    def delete(self, id_: UUID) -> None:
        pass
