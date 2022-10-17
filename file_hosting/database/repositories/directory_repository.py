from typing import Type

from sqlalchemy import select, delete
from sqlalchemy.sql import Select
from sqlalchemy.orm import sessionmaker

from database.models import Directory

from .abstract.directory_base import ADirectoryRepository
from .representations.directory import DirectoryRepr


class DirectoryRepository(ADirectoryRepository):
    def __init__(
            self, db: sessionmaker, model: Type[Directory] = Directory,
    ) -> None:
        super().__init__(db, model)

    def _convert_to_repr(self, model_object: Directory) -> DirectoryRepr:
        return DirectoryRepr(
            id=model_object.id,
            user_id=model_object.user_id,
            name=model_object.name
        )

    def _convert_to_model(self, repr_object: DirectoryRepr) -> Directory:
        return self._model(
            user_id=repr_object.user_id,
            name=repr_object.name
        )

    def _select_directories(self, user_id: int) -> Select:
        return select(self._model).filter_by(user_id=user_id)

    def get_by_id(self, user_id: int, id_: int) -> DirectoryRepr | None:
        with self._transaction() as session:
            directory = session.scalar(
                self._select_directories(user_id).filter_by(id=id_)
            )
        if directory:
            return self._convert_to_repr(directory)

    def get_by_name(self, user_id: int, name: str) -> DirectoryRepr | None:
        with self._transaction() as session:
            directory = session.scalar(
                self._select_directories(user_id).filter_by(name=name)
            )
        if directory:
            return self._convert_to_repr(directory)

    def get_all(
            self, user_id: int, offset: int = 0, limit: int = 100
    ) -> list[DirectoryRepr]:
        with self._transaction() as session:
            directories = session.scalars(
                self._select_directories(user_id).offset(offset).limit(limit)
            ).all()

        return self._convert_to_repr_list(directories)

    def delete(self, id_: int) -> None:
        with self._transaction() as session:
            session.execute(delete(self._model).filter_by(id=id_))

            session.commit()
