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


class FileGet(BaseModel):
    id: UUID
    time_added: datetime

    class Config:
        orm_mode = True
