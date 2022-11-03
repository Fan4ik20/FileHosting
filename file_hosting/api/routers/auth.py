from fastapi import APIRouter, Depends, status
from fastapi_jwt_auth import AuthJWT

from common.utils.passwords import verify_password

from database.repositories.dto import UserCreateDTO

from services import UserService
from services import service_exc

from api.dependencies.stubs.services import UserServiceS
from api.exceptions import exc as http_exc

from .schemas import user_sch


router = APIRouter(tags=['Authentication'])


def _map_user_schema_to_repr(
        user_schema: user_sch.UserCreate
) -> UserCreateDTO:
    return UserCreateDTO(
        username=user_schema.username, email=user_schema.email,
        password=user_schema.password
    )


@router.post('/login/', status_code=status.HTTP_201_CREATED)
def login(
        user: user_sch.UserLogin,
        user_service: UserService = Depends(UserServiceS),
        auth: AuthJWT = Depends()
):

    try:
        db_user = user_service.get_by_username(user.username)
    except service_exc.NotFoundError as err:
        raise http_exc.InvalidDataInBody(err.model, 'username')

    if not verify_password(user.password, db_user.password):
        raise http_exc.InvalidDataInBody('User', 'password')

    access_token = auth.create_access_token(subject=db_user.id)

    return {'access_token': access_token}


@router.post(
    '/register/', status_code=status.HTTP_201_CREATED,
    response_model=user_sch.UserGet
)
def register(
        user: user_sch.UserCreate,
        user_service: UserService = Depends(UserServiceS)
):
    user_repr = _map_user_schema_to_repr(user)

    try:
        return user_service.create(user_repr)
    except service_exc.AlreadyExistError as err:
        raise http_exc.ObjectAlreadyExistInBody(err.model, err.attr)
