from abc import ABC, abstractmethod
from typing import Iterable
from uuid import UUID

from database.models import File as FileModel
from database.repositories.dto import FileDTO, FileCreateDTO, FileUpdateDTO

from .base import BaseRepository
from ..converters import FileConverter


__all__ = ['AFileRepository']


class AFileRepository(
    ABC, BaseRepository[
        FileModel, FileCreateDTO, FileDTO, FileUpdateDTO, FileConverter
    ]
):
    @abstractmethod
    def get_by_id(
            self, user_id: int, directory_id: int, file_id: UUID
    ) -> FileDTO | None:
        pass

    @abstractmethod
    def get_all(
            self, user_id: int, directory_id: int,
            offset: int = 0, limit: int = 100
    ) -> Iterable[FileDTO]:
        pass

    @abstractmethod
    def delete(self, id_: UUID) -> None:
        pass
