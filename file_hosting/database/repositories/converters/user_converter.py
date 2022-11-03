from .base import BaseConverter

from database.repositories.dto import UserDTO, UserUpdateDTO, UserCreateDTO
from database.models import User as UserModel


__all__ = ['UserConverter']


class UserConverter(
    BaseConverter[UserModel, UserCreateDTO, UserDTO, UserUpdateDTO]
):
    @staticmethod
    def convert_to_repr(model: UserModel) -> UserDTO:
        return UserDTO(
            id=model.id,
            username=model.username,
            password=model.password,
            email=model.email
        )

    @staticmethod
    def convert_to_model(repr_obj: UserDTO) -> UserModel:
        return UserModel(
            username=repr_obj.username,
            email=repr_obj.email,
        )

    @staticmethod
    def convert_to_model_create(repr_obj: UserCreateDTO) -> UserModel:
        return UserModel(
            username=repr_obj.username,
            email=repr_obj.email,
            password=repr_obj.password
        )

    @staticmethod
    def convert_to_model_update(repr_obj: UserUpdateDTO) -> UserModel:
        return UserModel(
            username=repr_obj.username,  # type: ignore
            email=repr_obj.email,  # type: ignore
            password=repr_obj.password  # type: ignore
        )
