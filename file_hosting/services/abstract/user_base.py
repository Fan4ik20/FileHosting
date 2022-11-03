from abc import ABC, abstractmethod
from typing import Iterable

from .base import ServiceBase

from database.repositories import IUserRepository
from database.repositories.dto import UserDTO, UserCreateDTO


__all__ = ['AUserService']


class AUserService(ABC, ServiceBase[IUserRepository]):
    @abstractmethod
    def get(self, user_id: int) -> UserDTO:
        pass

    @abstractmethod
    def get_by_username(self, username: str) -> UserDTO:
        pass

    @abstractmethod
    def get_by_email(self, email: str) -> UserDTO:
        pass

    @abstractmethod
    def get_all(self, offset: int = 0, limit: int = 100) -> Iterable[UserDTO]:
        pass

    @abstractmethod
    def create(self, user_repr: UserCreateDTO) -> UserDTO:
        pass

    @abstractmethod
    def delete(self, user_id: int) -> None:
        pass
