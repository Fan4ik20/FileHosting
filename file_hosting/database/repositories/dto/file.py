from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


__all__ = ['FileDTO', 'FileCreateDTO', 'FileUpdateDTO', 'FileBaseDTO']


class FileBaseDTO:
    pass


@dataclass(frozen=True)
class FileDTO(FileBaseDTO):
    id: UUID
    url: str
    directory_id: int
    type: str
    name: str
    time_added: datetime


@dataclass(frozen=True)
class FileCreateDTO(FileBaseDTO):
    url: str
    directory_id: int
    type: str
    name: str


@dataclass(frozen=True)
class FileUpdateDTO(FileBaseDTO):
    name: str | None = None
    directory_id: int | None = None
