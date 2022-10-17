from abc import ABC, abstractmethod
from typing import Iterable

from .base import ServiceBase

from database.repositories.abstract.directory_base import \
    ADirectoryRepository, DirectoryRepr
from database.repositories.abstract.user_base import AUserRepository


class ADirectoryService(ABC, ServiceBase[ADirectoryRepository, DirectoryRepr]):
    def __init__(
            self, repository: ADirectoryRepository,
            user_repository: AUserRepository
    ) -> None:
        self._user_repository = user_repository

        super().__init__(repository)

    @abstractmethod
    def get(self, user_id: int, directory_id: int) -> DirectoryRepr:
        pass

    @abstractmethod
    def get_all(
            self, user_id: int, offset: int = 0, limit: int = 100
    ) -> Iterable[DirectoryRepr]:
        pass

    @abstractmethod
    def create(self, directory_repr: DirectoryRepr) -> DirectoryRepr:
        pass

    @abstractmethod
    def delete(self, user_id: int, directory_id: int) -> None:
        pass
