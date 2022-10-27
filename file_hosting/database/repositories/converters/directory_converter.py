from .base import BaseConverter

from database.repositories.representations import DirectoryRepr

from database.models import Directory as DirectoryModel

from .file_converter import FileConverter


__all__ = ['DirectoryConverter']


class DirectoryConverter(BaseConverter):
    @classmethod
    def convert_to_repr(
            cls, model: DirectoryModel, related: bool = False
    ) -> DirectoryRepr:
        return DirectoryRepr(
            id=model.id,
            name=model.name,
            user_id=model.user_id,
            directory_id=model.directory_id,
            inner_dirs=[
                cls.convert_to_repr(dir_) for dir_ in model.inner_dirs
            ] if related else None,
            files=[
                FileConverter.convert_to_repr(file) for file in model.files
            ] if related else None
        )

    @staticmethod
    def convert_to_model(repr_obj: DirectoryRepr) -> DirectoryModel:
        return DirectoryModel(
            name=repr_obj.name,
            user_id=repr_obj.user_id,
            directory_id=repr_obj.directory_id
        )
