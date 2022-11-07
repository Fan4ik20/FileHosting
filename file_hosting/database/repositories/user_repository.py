from typing import Type, Iterable

from sqlalchemy import delete, select

from database.models import User as UserModel

from .abstract.user_base import AUserRepository
from .dto import UserDTO, UserCreateDTO
from .converters import UserConverter
from .typing_ import DbSession


__all__ = ['UserRepository']


class UserRepository(AUserRepository):
    def __init__(
            self, session: DbSession, model: Type[UserModel] = UserModel,
            converter: Type[UserConverter] = UserConverter
    ):
        self._converter = converter

        super().__init__(session, model)

    def get_by_id(self, id_: int) -> UserDTO | None:
        user = self._session.get(self._model, id_)

        return self._converter.convert_to_repr(user) if user else None

    def get_by_username(self, username: str) -> UserDTO | None:
        user = self._session.scalar(
            select(self._model).filter_by(username=username)
        )

        return self._converter.convert_to_repr(user) if user else None

    def get_by_email(self, email: str) -> UserDTO | None:
        user = self._session.scalar(
            select(self._model).filter_by(email=email)
        )

        return self._converter.convert_to_repr(user) if user else None

    def get_all(self, offset: int = 0, limit: int = 100) -> Iterable[UserDTO]:
        users = self._session.scalars(
            select(self._model).offset(offset).limit(limit)
        ).all()

        return self._converter.convert_to_repr_list(users)

    def delete(self, id_: int) -> None:
        self._session.execute(delete(self._model).filter_by(id=id_))

        self._session.commit()

    def create(self, user_repr: UserCreateDTO) -> UserDTO:
        new_object = self._converter.convert_to_model_create(user_repr)

        self._session.add(new_object)
        self._session.commit()

        self._session.refresh(new_object)

        return self._converter.convert_to_repr(new_object)
