from fastapi import Depends
from fastapi_jwt_auth import AuthJWT

from services.user_service import UserService, UserRepr
from services.exceptions import user_exc

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
    except user_exc.UserNotFound:
        raise ValueError

    return user
