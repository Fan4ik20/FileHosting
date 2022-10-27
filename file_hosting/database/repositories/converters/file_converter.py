from .base import BaseConverter

from database.models import File as FileModel
from database.repositories.representations import FileRepr


__all__ = ['FileConverter']


class FileConverter(BaseConverter):
    @staticmethod
    def convert_to_repr(model: FileModel) -> FileRepr:
        return FileRepr(
            id=model.id,
            time_added=model.time_added,
            url=model.url,
            directory_id=model.directory_id,
            type=model.type,
            name=model.name
        )

    @staticmethod
    def convert_to_model(repr_obj: FileRepr) -> FileModel:
        return FileModel(
            url=repr_obj.url,
            directory_id=repr_obj.directory_id,
            type=repr_obj.type,
            name=repr_obj.name
        )
