from abc import ABC, abstractmethod
from typing import Iterable
from uuid import UUID

from .base import ServiceBase

from database.repositories.abstract.user_base import AUserRepository
from database.repositories.abstract.directory_base import ADirectoryRepository
from database.repositories.abstract.file_base import AFileRepository, FileRepr


class AFileService(ABC, ServiceBase[AFileRepository, FileRepr]):
    def __init__(
            self, repository: AFileRepository,
            user_repository: AUserRepository,
            directory_repository: ADirectoryRepository
    ) -> None:
        self._user_repository = user_repository
        self._directory_repository = directory_repository

        super().__init__(repository)

    @abstractmethod
    def get(self, user_id: int, directory_id: int, file_id: UUID) -> FileRepr:
        pass

    @abstractmethod
    def get_all(
            self, user_id: int, directory_id: int,
            offset: int = 0, limit: int = 100
    ) -> Iterable[FileRepr]:
        pass

    @abstractmethod
    def create(self, user_id: int, file_repr: FileRepr) -> FileRepr:
        pass

    @abstractmethod
    def delete(self, user_id: int, directory_id, file_id: UUID) -> None:
        pass
