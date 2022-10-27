from .base import NotFoundError


__all__ = ['FileNotFound']


class _FileExcBase(Exception):
    model = 'File'


class FileNotFound(_FileExcBase, NotFoundError):
    pass
