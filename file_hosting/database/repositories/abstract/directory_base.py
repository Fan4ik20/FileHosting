from abc import ABC, abstractmethod
from typing import Type

from sqlalchemy.orm import sessionmaker

from database.models import Directory as DirectoryModel
from database.repositories.representations import \
    DirectoryRepr, DirectoryReprUpdate

from .base import BaseRepository


__all__ = ['ADirectoryRepository']


class ADirectoryRepository(ABC, BaseRepository[DirectoryModel, DirectoryRepr]):
    def __init__(
            self, db: sessionmaker,
            model: Type[DirectoryModel] = DirectoryModel
    ) -> None:
        super().__init__(db, model)

    @abstractmethod
    def _convert_to_repr(self, model_object: DirectoryModel) -> DirectoryRepr:
        pass

    @abstractmethod
    def _convert_to_model(self, repr_object: DirectoryRepr) -> DirectoryModel:
        pass

    @abstractmethod
    def _update_model(
            self, dir_model: DirectoryModel, dir_repr: DirectoryRepr
    ) -> None:
        pass

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
    def get_by_name(self, user_id: int, name: str) -> DirectoryRepr | None:
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
