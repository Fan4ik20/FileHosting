from uuid import UUID

from sqlalchemy import select, delete
from sqlalchemy.sql import Select

from database.models import File as FileModel

from .abstract.file_base import AFileRepository
from .representations.file import FileRepr


class FileRepository(AFileRepository):
    def _convert_to_repr(self, model_object: FileModel) -> FileRepr:
        return FileRepr(
            id=model_object.id,
            url=model_object.url,
            time_added=model_object.time_added,
            directory_id=model_object.directory_id,
            type=model_object.type,
            name=model_object.name
        )

    def _convert_to_model(self, repr_object: FileRepr) -> FileModel:
        return self._model(
            url=repr_object.url,
            directory_id=repr_object.directory_id,
            name=repr_object.name,
            type=repr_object.type
        )

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
            return self._convert_to_repr(file)

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

        return self._convert_to_repr_list(files)

    def delete(self, id_: UUID) -> None:
        with self._transaction() as session:
            session.execute(delete(self._model).filter_by(id=id_))
