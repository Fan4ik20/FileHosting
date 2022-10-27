from typing import TypeVar, Generic, Iterable


Repository = TypeVar('Repository')
Repr = TypeVar('Repr')


__all__ = ['ServiceBase']


class ServiceBase(Generic[Repository, Repr]):
    def __init__(self, repository: Repository) -> None:
        self._repository = repository

    def get(self, *args) -> Repr:
        raise NotImplementedError

    def get_all(self, *args) -> Iterable[Repr]:
        raise NotImplementedError

    def create(self, *args) -> Repr:
        raise NotImplementedError

    def delete(self, *args) -> None:
        raise NotImplementedError
