from uuid import UUID
from typing import Type

from sqlalchemy import select, delete
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import Select

from database.models import File as FileModel, Directory as DirectoryModel

from .abstract.file_base import AFileRepository
from .representations import FileRepr
from .converters import FileConverter


__all__ = ['FileRepository']


class FileRepository(AFileRepository):
    def __init__(
            self, db: sessionmaker, model: Type[FileModel] = FileModel,
            directory_model: Type[DirectoryModel] = DirectoryModel,
            converter: Type[FileConverter] = FileConverter
    ) -> None:
        self._directory_model = directory_model

        super().__init__(db, model, converter)

    def _select_files(self, user_id: int, directory_id: int) -> Select:
        return select(self._model).join(
            self._directory_model
        ).filter(
            self._directory_model.user_id == user_id,
            self._directory_model.id == directory_id
        )

    def get_by_id(
            self, user_id: int, directory_id: int, id_: UUID
    ) -> FileRepr:
        with self._transaction() as session:
            file = session.scalar(
                self._select_files(user_id, directory_id).filter(
                    self._model.id == id_
                )
            )

        if file:
            return self._converter.convert_to_repr(file)

    def get_all(
            self, user_id: int, directory_id: int,
            offset: int = 0, limit: int = 100
    ) -> list[FileRepr]:
        with self._transaction() as session:
            files = session.scalars(
                self._select_files(
                    user_id, directory_id
                ).offset(offset).limit(limit)
            ).all()

        return self._converter.convert_to_repr_list(files)

    def delete(self, id_: UUID) -> None:
        with self._transaction() as session:
            session.execute(delete(self._model).filter_by(id=id_))
