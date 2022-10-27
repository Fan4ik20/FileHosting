from dataclasses import dataclass


__all__ = ['DirectoryRepr', 'DirectoryReprUpdate']


@dataclass
class DirectoryRepr:
    name: str
    user_id: int

    directory_id: int | None = None
    inner_dirs: list | None = None
    files: list | None = None
    id: int | None = None


@dataclass
class DirectoryReprUpdate(DirectoryRepr):
    name: str | None = None
    user_id: int | None = None
