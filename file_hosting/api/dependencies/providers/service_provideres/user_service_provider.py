from fastapi import Depends

from api.dependencies.stubs import SessionS

from database.repositories import UserRepository
from services import UserService

from ..typing_ import DbSession


__all__ = ['UserServiceProvider']


class UserServiceProvider:
    def __call__(self, session: DbSession = Depends(SessionS)) -> UserService:
        repository = UserRepository(session)
        return UserService(repository)
