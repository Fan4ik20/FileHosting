from typing import Generic, TypeVar, Type, TypeAlias

from database.repositories.typing_ import DbSession


Model = TypeVar('Model')
Repr = TypeVar('Repr')
Converter = TypeVar('Converter')

identifier: TypeAlias = int | str


class BaseRepository(Generic[Model, Repr, Converter]):
    def __init__(
            self, session: DbSession, model: Type[Model],
            converter: Type[Converter]
    ) -> None:
        self._session = session
        self._model = model
        self._converter = converter

    def get_by_id(self, *args) -> Repr:
        raise NotImplementedError

    def get_all(
            self, *args
    ) -> list[Repr]:
        raise NotImplementedError

    def create(self, repr_object: Repr) -> Repr:
        new_object = self._converter.convert_to_model(repr_object)

        self._session.add(new_object)
        self._session.commit()

        self._session.refresh(new_object)

        return self._converter.convert_to_repr(new_object)

    def delete(self, *args) -> None:
        raise NotImplementedError
