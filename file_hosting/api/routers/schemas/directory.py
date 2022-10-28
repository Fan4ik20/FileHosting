from pydantic import BaseModel, PositiveInt, Field

from .file import FileGet


class DirectorySchemaBase(BaseModel):
    name: str = Field(..., max_length=100)
    directory_id: int | None = None


class DirectoryCreate(DirectorySchemaBase):
    pass


class DirectoryGet(DirectorySchemaBase):
    id: PositiveInt
    user_id: PositiveInt

    class Config:
        orm_mode = True


class DirectoryGetDetail(DirectorySchemaBase):
    id: PositiveInt
    user_id: PositiveInt

    files: list[FileGet] | None = None
    inner_dirs: list[DirectoryGet] | None = None

    class Config:
        orm_mode = True


class DirectoryPatch(BaseModel):
    name: str | None = None
    directory_id: PositiveInt | None = None
