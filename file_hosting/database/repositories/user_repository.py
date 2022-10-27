from typing import Type

from sqlalchemy import delete, select
from sqlalchemy.orm import sessionmaker

from database.models import User as UserModel

from common.utils.passwords import get_password_hash

from .abstract.user_base import AUserRepository
from .representations import UserRepr
from .converters import UserConverter


__all__ = ['UserRepository']


class UserRepository(AUserRepository):
    def __init__(
            self, db: sessionmaker, model: Type[UserModel] = UserModel,
            converter: Type[UserConverter] = UserConverter
    ):
        super().__init__(db, model, converter)

    def create(self, repr_object: UserRepr) -> UserRepr:
        repr_object.password = get_password_hash(repr_object.password)

        return super(UserRepository, self).create(repr_object)

    def get_by_id(self, id_: int) -> UserRepr | None:
        with self._transaction() as session:
            user = session.get(self._model, id_)

        if user:
            return self._converter.convert_to_repr(user)

    def get_by_username(self, username: str) -> UserRepr | None:
        with self._transaction() as session:
            user = session.scalar(
                select(self._model).filter_by(username=username)
            )

        if user:
            return self._converter.convert_to_repr(user)

    def get_by_email(self, email: str) -> UserRepr | None:
        with self._transaction() as session:
            user = session.scalar(
                select(self._model).filter_by(email=email)
            )

        if user:
            return self._converter.convert_to_repr(user)

    def get_all(self, offset: int = 0, limit: int = 100) -> list[UserRepr]:
        with self._transaction() as session:
            users = session.scalars(
                select(self._model).offset(offset).limit(limit)
            ).all()

        return self._converter.convert_to_repr_list(users)

    def delete(self, id_: int) -> None:
        with self._transaction() as session:
            session.execute(delete(self._model).filter_by(id=id_))

            session.commit()
