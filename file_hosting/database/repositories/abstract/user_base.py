from abc import ABC, abstractmethod

from .base import BaseRepository

from database.models import User as UserModel
from database.repositories.representations import UserRepr
from database.repositories.converters import UserConverter


__all__ = ['AUserRepository']


class AUserRepository(ABC, BaseRepository[UserModel, UserRepr, UserConverter]):
    @abstractmethod
    def get_by_id(self, id_: int) -> UserRepr | None:
        pass

    @abstractmethod
    def get_by_username(self, username: str) -> UserRepr | None:
        pass

    @abstractmethod
    def get_by_email(self, email: str) -> UserRepr | None:
        pass

    @abstractmethod
    def get_all(self, offset: int = 0, limit: int = 100) -> list[UserRepr]:
        pass

    @abstractmethod
    def delete(self, id_: int) -> None:
        pass
