from typing import Generic, TypeVar, Type, TypeAlias

from contextlib import contextmanager

from sqlalchemy.orm import sessionmaker, Session


Model = TypeVar('Model')
Repr = TypeVar('Repr')

identifier: TypeAlias = int | str


class BaseRepository(Generic[Model, Repr]):
    def __init__(
            self, db: sessionmaker, model: Type[Model]
    ) -> None:
        self._db = db
        self._model = model

    @contextmanager
    def _transaction(self) -> Session:
        with self._db() as session:
            yield session

    def _convert_to_repr_list(self, model_list: list[Model]) -> list[Repr]:
        return [self._convert_to_repr(model_obj) for model_obj in model_list]

    def _convert_to_repr(self, model_object: Model) -> Repr:
        raise NotImplementedError

    def _convert_to_model(self, repr_object: Repr) -> Model:
        raise NotImplementedError

    def get_by_id(self, *args) -> Repr:
        raise NotImplementedError

    def get_all(
            self, *args
    ) -> list[Repr]:
        raise NotImplementedError

    def create(self, repr_object: Repr) -> Repr:
        new_object = self._convert_to_model(repr_object)

        with self._transaction() as session:
            session.add(new_object)
            session.commit()

            session.refresh(new_object)

        return self._convert_to_repr(new_object)

    def delete(self, *args) -> None:
        raise NotImplementedError
