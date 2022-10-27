from fastapi import APIRouter, Depends, status
from fastapi.responses import Response

from database.repositories.representations import UserRepr

from services import IUserService
from services import service_exc

from api.dependencies.stubs.services import UserServiceS
from api.dependencies.stubs.auth import ActiveUserS

from api.exceptions import exc as http_exc

from .schemas.user import UserGet


router = APIRouter(prefix='/users', tags=['Users'])


@router.get('/me/', response_model=UserGet)
def get_active_user(user: UserRepr = Depends(ActiveUserS)):
    return user


@router.delete(
    '/me/', response_class=Response, status_code=status.HTTP_204_NO_CONTENT
)
def delete_active_user(
        user: UserRepr = Depends(ActiveUserS),
        user_service: IUserService = Depends(UserServiceS)
):
    # FIXME.

    try:
        user_service.delete(user.id)
    except service_exc.NotFoundError as err:
        raise http_exc.ObjectNotExistInPath(err.model)
