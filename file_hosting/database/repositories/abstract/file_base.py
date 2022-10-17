from typing import Type
from abc import ABC, abstractmethod
from uuid import UUID

from sqlalchemy.orm import sessionmaker

from database.models import File as FileModel, Directory as DirectoryModel
from database.repositories.representations.file import FileRepr

from .base import BaseRepository


class AFileRepository(ABC, BaseRepository[FileModel, FileRepr]):
    def __init__(
            self, db: sessionmaker, model: Type[FileModel] = FileModel,
            directory_model: Type[DirectoryModel] = DirectoryModel
    ) -> None:
        self._directory_model = directory_model

        super().__init__(db, model)

    @abstractmethod
    def _convert_to_repr(self, model_object: FileModel) -> FileRepr:
        pass

    @abstractmethod
    def _convert_to_model(self, repr_object: FileRepr) -> FileModel:
        pass

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
