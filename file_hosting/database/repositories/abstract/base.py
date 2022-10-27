from typing import Generic, TypeVar, Type, TypeAlias

from contextlib import contextmanager

from sqlalchemy.orm import sessionmaker, Session


Model = TypeVar('Model')
Repr = TypeVar('Repr')
Converter = TypeVar('Converter')

identifier: TypeAlias = int | str


class BaseRepository(Generic[Model, Repr, Converter]):
    def __init__(
            self, db: sessionmaker, model: Type[Model],
            converter: Type[Converter]
    ) -> None:
        self._db = db
        self._model = model
        self._converter = converter

    @contextmanager
    def _transaction(self) -> Session:
        with self._db() as session:
            yield session

    def get_by_id(self, *args) -> Repr:
        raise NotImplementedError

    def get_all(
            self, *args
    ) -> list[Repr]:
        raise NotImplementedError

    def create(self, repr_object: Repr) -> Repr:
        new_object = self._converter.convert_to_model(repr_object)

        with self._transaction() as session:
            session.add(new_object)
            session.commit()

            session.refresh(new_object)

        return self._converter.convert_to_repr(new_object)

    def delete(self, *args) -> None:
        raise NotImplementedError
