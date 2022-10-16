from pydantic import BaseModel, PositiveInt, Field


class DirectorySchemaBase(BaseModel):
    name: str = Field(..., max_length=100)


class DirectoryCreate(DirectorySchemaBase):
    pass


class DirectoryGet(DirectorySchemaBase):
    id: PositiveInt
    user_id: PositiveInt

    class Config:
        orm_mode = True
