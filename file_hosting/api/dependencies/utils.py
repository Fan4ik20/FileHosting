from fastapi import Depends
from fastapi_jwt_auth import AuthJWT

from database.repositories.representations import UserRepr

from services import UserService
from services import exceptions as service_exc

from .stubs.services import UserServiceS


class PaginationParams:
    def __init__(self, offset: int = 0, limit: int = 100) -> None:
        self.offset = offset
        self.limit = limit


def login_required(auth: AuthJWT = Depends()) -> None:
    auth.jwt_required()


def get_current_user(
        auth: AuthJWT = Depends(),
        user_service: UserService = Depends(UserServiceS),
        _=Depends(login_required)
) -> UserRepr:
    user_id = auth.get_jwt_subject()

    try:
        user = user_service.get(user_id)
    except service_exc.UserNotFound:
        raise ValueError

    return user
