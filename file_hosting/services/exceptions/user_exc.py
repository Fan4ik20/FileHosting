from .base import NotFoundError, AlreadyExistError, CantDeleteError


__all__ = [
    'UserNotFound', 'UserWithEmailExist',
    'UserWithUsernameExist', 'UserCantBeDeleted'
]


class _BaseUserError(Exception):
    model = 'User'


class UserNotFound(NotFoundError, _BaseUserError):
    pass


class UserWithUsernameExist(AlreadyExistError, _BaseUserError):
    attr = 'username'


class UserWithEmailExist(AlreadyExistError, _BaseUserError):
    attr = 'email'


class UserCantBeDeleted(CantDeleteError, _BaseUserError):
    pass
