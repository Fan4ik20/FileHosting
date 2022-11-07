from fastapi import Depends

from api.dependencies.stubs import SessionS

from database.repositories import DirectoryRepository, UserRepository
from services import DirectoryService

from ..typing_ import DbSession


__all__ = ['DirectoryServiceProvider']


class DirectoryServiceProvider:
    def __call__(
            self, session: DbSession = Depends(SessionS)
    ) -> DirectoryService:
        user_repository = UserRepository(session)
        directory_repository = DirectoryRepository(session)

        return DirectoryService(directory_repository, user_repository)
