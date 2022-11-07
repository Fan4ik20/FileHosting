from uuid import UUID
from typing import Type, Iterable

from sqlalchemy import select, delete
from sqlalchemy.sql import Select

from database.models import File as FileModel, Directory as DirectoryModel

from .abstract.file_base import AFileRepository
from .dto import FileDTO, FileCreateDTO
from .converters import FileConverter
from .typing_ import DbSession


__all__ = ['FileRepository']


class FileRepository(AFileRepository):
    def __init__(
            self, session: DbSession, model: Type[FileModel] = FileModel,
            directory_model: Type[DirectoryModel] = DirectoryModel,
            converter: Type[FileConverter] = FileConverter
    ) -> None:
        self._directory_model = directory_model
        self._converter = converter

        super().__init__(session, model)

    def _select_files(self, user_id: int, directory_id: int) -> Select:
        return select(self._model).join(
            self._directory_model
        ).filter(
            self._directory_model.user_id == user_id,
            self._directory_model.id == directory_id
        )

    def get_by_id(
            self, user_id: int, directory_id: int, id_: UUID
    ) -> FileDTO | None:
        file = self._session.scalar(
            self._select_files(user_id, directory_id).filter(
                self._model.id == id_
            )
        )

        return self._converter.convert_to_repr(file) if file else None

    def get_all(
            self, user_id: int, directory_id: int,
            offset: int = 0, limit: int = 100
    ) -> Iterable[FileDTO]:
        files = self._session.scalars(
            self._select_files(
                user_id, directory_id
            ).offset(offset).limit(limit)
        ).all()

        return self._converter.convert_to_repr_list(files)

    def delete(self, id_: UUID) -> None:
        self._session.execute(delete(self._model).filter_by(id=id_))
        self._session.commit()

    def create(self, file_repr: FileCreateDTO) -> FileDTO:
        new_object = self._converter.convert_to_model_create(file_repr)

        self._session.add(new_object)
        self._session.commit()

        self._session.refresh(new_object)

        return self._converter.convert_to_repr(new_object)
