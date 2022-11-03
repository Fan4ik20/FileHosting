from abc import ABC, abstractmethod
from typing import Iterable

from .base import BaseRepository

from database.models import User as UserModel

from database.repositories.dto import UserDTO, UserCreateDTO, UserUpdateDTO
from ..converters import UserConverter


__all__ = ['AUserRepository']


class AUserRepository(
    ABC, BaseRepository[
        UserModel, UserCreateDTO, UserDTO, UserUpdateDTO, UserConverter
    ]
):
    @abstractmethod
    def get_by_id(self, id_: int) -> UserDTO | None:
        pass

    @abstractmethod
    def get_by_username(self, username: str) -> UserDTO | None:
        pass

    @abstractmethod
    def get_by_email(self, email: str) -> UserDTO | None:
        pass

    @abstractmethod
    def get_all(self, offset: int = 0, limit: int = 100) -> Iterable[UserDTO]:
        pass

    @abstractmethod
    def delete(self, id_: int) -> None:
        pass
