from dataclasses import dataclass

from .file import FileRepr


__all__ = ['DirectoryRepr', 'DirectoryReprUpdate']


@dataclass
class DirectoryRepr:
    name: str
    user_id: int

    directory_id: int | None = None
    inner_dirs: list['DirectoryRepr'] | None = None
    files: list[FileRepr] | None = None
    id: int | None = None


@dataclass
class DirectoryReprUpdate(DirectoryRepr):
    name: str | None = None
    user_id: int | None = None
