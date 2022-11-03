from abc import ABC, abstractmethod
from typing import Iterable
from uuid import UUID

from .base import ServiceBase

from database.repositories import (
    IUserRepository, IDirectoryRepository, IFileRepository
)
from database.repositories.dto import FileDTO, FileCreateDTO


__all__ = ['AFileService']


class AFileService(ABC, ServiceBase[IFileRepository]):
    def __init__(
            self, repository: IFileRepository,
            user_repository: IUserRepository,
            directory_repository: IDirectoryRepository
    ) -> None:
        self._user_repository = user_repository
        self._directory_repository = directory_repository

        super().__init__(repository)

    @abstractmethod
    def get(self, user_id: int, directory_id: int, file_id: UUID) -> FileDTO:
        pass

    @abstractmethod
    def get_all(
            self, user_id: int, directory_id: int,
            offset: int = 0, limit: int = 100
    ) -> Iterable[FileDTO]:
        pass

    @abstractmethod
    def create(self, user_id: int, file_repr: FileCreateDTO) -> FileDTO:
        pass

    @abstractmethod
    def delete(self, user_id: int, directory_id: int, file_id: UUID) -> None:
        pass
