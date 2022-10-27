from .base import NotFoundError, AlreadyExistError, CantDeleteError


__all__ = [
    'DirectoryNotFound', 'DirectoryWithNameAlreadyExist',
    'DirectoryCantBeDeleted'
]


class _DirectoryBaseError(Exception):
    model = 'Directory'


class DirectoryNotFound(_DirectoryBaseError, NotFoundError):
    pass


class DirectoryWithNameAlreadyExist(_DirectoryBaseError, AlreadyExistError):
    attr = 'name'


class DirectoryCantBeDeleted(_DirectoryBaseError, CantDeleteError):
    pass
