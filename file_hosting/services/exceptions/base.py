class NotFoundError(Exception):
    model: str


class AlreadyExistError(Exception):
    model: str
    attr: str


class CantDeleteError(Exception):
    model: str
