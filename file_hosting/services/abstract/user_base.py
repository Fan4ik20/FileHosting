from abc import ABC, abstractmethod
from typing import Iterable

from .base import ServiceBase

from database.repositories import IUserRepository
from database.repositories.representations import UserRepr


class AUserService(ABC, ServiceBase[AUserRepository, UserRepr]):
    @abstractmethod
    def get(self, user_id: int) -> UserRepr:
        pass

    @abstractmethod
    def get_by_username(self, username: str) -> UserRepr:
        pass

    @abstractmethod
    def get_by_email(self, email: str) -> UserRepr:
        pass

    @abstractmethod
    def get_all(self, offset: int = 0, limit: int = 100) -> Iterable[UserRepr]:
        pass

    @abstractmethod
    def create(self, user_repr: UserRepr) -> UserRepr:
        pass

    @abstractmethod
    def delete(self, user_id: int) -> None:
        pass
