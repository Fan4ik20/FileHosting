from typing import Generic, TypeVar, Type, TypeAlias

from database.repositories.typing_ import DbSession


Model = TypeVar('Model')

DTO = TypeVar('DTO')
DTOCreate = TypeVar('DTOCreate')

identifier: TypeAlias = int | str

# TODO. Mypy Converter


class BaseRepository(Generic[Model, DTOCreate, DTO]):
    def __init__(
            self, session: DbSession, model: Type[Model],
    ) -> None:
        self._session = session
        self._model = model
