from fastapi import Depends

from api.dependencies.stubs import SessionS

from database.repositories import \
    UserRepository, FileRepository, DirectoryRepository
from services import FileService

from ..typing_ import DbSession


__all__ = ['FileServiceProvider']


class FileServiceProvider:
    def __call__(self, session: DbSession = Depends(SessionS)) -> FileService:
        user_rep = UserRepository(session)
        directory_rep = DirectoryRepository(session)
        file_rep = FileRepository(session)

        return FileService(file_rep, user_rep, directory_rep)
