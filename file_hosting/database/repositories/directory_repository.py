from typing import Type, Iterable

from sqlalchemy import select, delete
from sqlalchemy.sql import Select
from sqlalchemy.orm import sessionmaker, selectinload

from database.models import Directory

from .abstract.directory_base import ADirectoryRepository
from .representations import DirectoryRepr, DirectoryReprUpdate
from .converters import DirectoryConverter


__all__ = ['DirectoryRepository']


class DirectoryRepository(ADirectoryRepository):
    def __init__(
            self, db: sessionmaker,
            model: Type[Directory] = Directory,
            converter: Type[DirectoryConverter] = DirectoryConverter
    ) -> None:
        super().__init__(db, model, converter)

    def _update_model(
            self, dir_model: Directory, dir_repr: DirectoryReprUpdate
    ) -> None:
        for attr, value in vars(dir_repr).items():
            if value and hasattr(dir_model, attr):
                setattr(dir_model, attr, value)

    def _select_directories(self, user_id: int) -> Select:
        return select(self._model).filter_by(user_id=user_id)

    def _select_ind_directory(self, user_id: int, directory_id: int) -> Select:
        return self._select_directories(
            user_id
        ).filter_by(id=directory_id)

    def get_by_id(self, user_id: int, id_: int) -> DirectoryRepr | None:
        with self._transaction() as session:
            directory = session.scalar(
                self._select_ind_directory(user_id, id_)
            )
        if directory:
            return self._converter.convert_to_repr(directory)

    def get_by_id_with_related(
            self, user_id: int, id_: int
    ) -> DirectoryRepr | None:
        with self._transaction() as session:
            directory = session.scalar(
                self._select_ind_directory(user_id, id_)
                .options(
                    selectinload(self._model.inner_dirs),
                    selectinload(self._model.files)
                )
            )

        if directory:
            return self._converter.convert_to_repr(directory, related=True)

    def get_by_name(
            self, user_id: int, name: str, out_directory_id: int | None = None
    ) -> DirectoryRepr | None:
        with self._transaction() as session:
            directory = session.scalar(
                self._select_directories(user_id)
                    .filter_by(name=name, directory_id=out_directory_id)
            )
        if directory:
            return self._converter.convert_to_repr(directory)

    def get_all_without_parent(
            self, user_id: int, offset: int = 0, limit: int = 100
    ) -> Iterable[DirectoryRepr]:
        with self._transaction() as session:
            directories = session.scalars(
                self._select_directories(user_id).filter(
                    self._model.directory_id.is_(None)
                ).offset(offset).limit(limit)
            ).all()

        return self._converter.convert_to_repr_list(directories)

    def get_all(
            self, user_id: int, offset: int = 0, limit: int = 100
    ) -> Iterable[DirectoryRepr]:
        with self._transaction() as session:
            directories = session.scalars(
                self._select_directories(user_id).offset(offset).limit(limit)
            ).all()

        return self._converter.convert_to_repr_list(directories)

    def delete(self, id_: int) -> None:
        with self._transaction() as session:
            session.execute(delete(self._model).filter_by(id=id_))

            session.commit()

    def update(
            self, user_id: int, id_: int, dir_repr: DirectoryReprUpdate
    ) -> DirectoryRepr | None:
        with self._transaction() as session:
            directory = session.scalar(
                self._select_ind_directory(user_id, id_)
            )

            if not directory:
                return None

            self._update_model(directory, dir_repr)

            session.commit()
            session.refresh(directory)

        return self._converter.convert_to_repr(directory)
