from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from .enums import FileTypeEnum


class FileBase(BaseModel):
    url: str
    name: str
    type: FileTypeEnum


class FilePost(FileBase):
    pass


class FileGet(FileBase):
    id: UUID
    time_added: datetime
    directory_id: int

    class Config:
        orm_mode = True
