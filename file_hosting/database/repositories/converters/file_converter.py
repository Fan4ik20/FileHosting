from .base import BaseConverter

from database.models import File as FileModel
from database.repositories.dto import FileDTO, FileUpdateDTO, FileCreateDTO


__all__ = ['FileConverter']


class FileConverter(
    BaseConverter[FileModel, FileCreateDTO, FileDTO, FileUpdateDTO]
):
    @staticmethod
    def convert_to_repr(model: FileModel) -> FileDTO:
        return FileDTO(
            id=model.id,
            time_added=model.time_added,
            url=model.url,
            directory_id=model.directory_id,
            type=model.type,
            name=model.name
        )

    @staticmethod
    def convert_to_model_create(repr_obj: FileCreateDTO) -> FileModel:
        return FileModel(
            name=repr_obj.name,
            url=repr_obj.url,
            type=repr_obj.type,
            directory_id=repr_obj.directory_id
        )

    @staticmethod
    def convert_to_model_update(repr_obj: FileUpdateDTO) -> FileModel:
        return FileModel(
            name=repr_obj.name,  # type: ignore
            directory_id=repr_obj.directory_id  # type: ignore
        )
