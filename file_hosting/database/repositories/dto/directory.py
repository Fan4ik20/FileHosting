from dataclasses import dataclass

from .file import FileDTO


__all__ = [
    'DirectoryDTO', 'DirectoryUpdateDTO', 'DirectoryCreateDTO',
    'BaseDirectoryDTO'
]


class BaseDirectoryDTO:
    pass


@dataclass(frozen=True)
class DirectoryDTO(BaseDirectoryDTO):
    id: int
    name: str
    user_id: int

    directory_id: int | None = None
    inner_dirs: list['DirectoryDTO'] | None = None
    files: list[FileDTO] | None = None


@dataclass(frozen=True)
class DirectoryCreateDTO(BaseDirectoryDTO):
    name: str
    user_id: int

    directory_id: int | None = None


@dataclass(frozen=True)
class DirectoryUpdateDTO(BaseDirectoryDTO):
    name: str | None = None
    directory_id: int | None = None
