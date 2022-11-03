from abc import ABC, abstractmethod
from typing import Iterable

from .base import ServiceBase

from database.repositories import IDirectoryRepository, IUserRepository
from database.repositories.dto import \
    DirectoryDTO, DirectoryUpdateDTO, DirectoryCreateDTO


__all__ = ['ADirectoryService']


class ADirectoryService(ABC, ServiceBase[IDirectoryRepository]):
    def __init__(
            self, repository: IDirectoryRepository,
            user_repository: IUserRepository
    ) -> None:
        self._user_repository = user_repository

        super().__init__(repository)

    @abstractmethod
    def get(
            self, user_id: int, directory_id: int, related: bool = False
    ) -> DirectoryDTO:
        pass

    @abstractmethod
    def get_all(
            self, user_id: int, offset: int = 0, limit: int = 100
    ) -> Iterable[DirectoryDTO]:
        pass

    @abstractmethod
    def create(self, directory_repr: DirectoryCreateDTO) -> DirectoryDTO:
        pass

    @abstractmethod
    def delete(self, user_id: int, directory_id: int) -> None:
        pass

    @abstractmethod
    def update(
            self, user_id: int, directory_id: int,
            dir_repr: DirectoryUpdateDTO
    ) -> DirectoryDTO:
        pass
