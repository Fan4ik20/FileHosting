from .base import BaseConverter

from database.repositories.representations import UserRepr
from database.models import User as UserModel


__all__ = ['UserConverter']


class UserConverter(BaseConverter):
    @staticmethod
    def convert_to_repr(model: UserModel) -> UserRepr:
        return UserRepr(
            id=model.id,
            username=model.username,
            email=model.email,
            password=model.password
        )

    @staticmethod
    def convert_to_model(repr_obj: UserModel) -> UserRepr:
        return UserModel(
            username=repr_obj.username,
            email=repr_obj.email,
            password=repr_obj.password
        )
