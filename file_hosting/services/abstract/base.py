from typing import TypeVar, Generic


Repository = TypeVar('Repository')


__all__ = ['ServiceBase']


class ServiceBase(Generic[Repository]):
    def __init__(self, repository: Repository) -> None:
        self._repository = repository
