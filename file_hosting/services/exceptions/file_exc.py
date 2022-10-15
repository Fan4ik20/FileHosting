from .base import NotFoundError


class _FileExcBase(Exception):
    model = 'File'


class FileNotFound(_FileExcBase, NotFoundError):
    pass
