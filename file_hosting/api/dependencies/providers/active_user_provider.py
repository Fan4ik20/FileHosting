from fastapi import Depends
from fastapi_jwt_auth import AuthJWT

from api.dependencies.stubs import UserServiceS

from services import IUserService
from database.repositories.dto import UserDTO


__all__ = ['ActiveUserProvider']


def login_required(auth: AuthJWT = Depends(AuthJWT)) -> None:
    auth.jwt_required()


class ActiveUserProvider:
    def __call__(
            self, auth: AuthJWT = Depends(),
            user_service: IUserService = Depends(UserServiceS),
            _: None = Depends(login_required)
    ) -> UserDTO:
        user_id = auth.get_jwt_subject()

        return user_service.get(user_id)
