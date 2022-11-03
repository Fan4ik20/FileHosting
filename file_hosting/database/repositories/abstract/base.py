from typing import Generic, TypeVar, Type, TypeAlias

from database.repositories.typing_ import DbSession
from database.repositories.converters.base import BaseConverter


Model = TypeVar('Model')

DTO = TypeVar('DTO')
DTOCreate = TypeVar('DTOCreate')
DTOUpdate = TypeVar('DTOUpdate')
Converter = TypeVar('Converter')
Converter_: TypeAlias = BaseConverter[Model, DTOCreate, DTO, DTOUpdate]

identifier: TypeAlias = int | str

# TODO. Mypy Converter


class BaseRepository(Generic[Model, DTOCreate, DTO, DTOUpdate, Converter]):
    def __init__(
            self, session: DbSession, model: Type[Model],
            converter: Type[Converter]
    ) -> None:
        self._session = session
        self._model = model
        self._converter = converter

    def create(self, repr_object: DTOCreate) -> DTO:
        new_object = self._converter.convert_to_model_create(repr_object)

        self._session.add(new_object)
        self._session.commit()

        self._session.refresh(new_object)

        return self._converter.convert_to_repr_create(new_object)
