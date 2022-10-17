from abc import ABC, abstractmethod
from typing import Type

from sqlalchemy.orm import sessionmaker

from .base import BaseRepository

from database.models import User as UserModel
from database.repositories.representations.user import UserRepr


class AUserRepository(ABC, BaseRepository[UserModel, UserRepr]):
    def __init__(self, db: sessionmaker, model: Type[UserModel] = UserModel):
        super().__init__(db, model)

    @abstractmethod
    def _convert_to_repr(self, model_object: UserModel) -> UserRepr:
        pass

    @abstractmethod
    def _convert_to_model(self, repr_object: UserRepr) -> UserModel:
        pass

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
