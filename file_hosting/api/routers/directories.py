from fastapi import APIRouter, Depends, status
from fastapi.responses import Response

from database.repositories.representations.directory import DirectoryRepr
from database.repositories.representations.user import UserRepr

from services.directory_service import DirectoryService
from services.exceptions import base as service_exc

from api.dependencies.stubs.services import DirectoryServiceS
from api.dependencies.stubs.auth import ActiveUserS

from api.dependencies.utils import PaginationParams

from api.exceptions import exc as http_exc

from .schemas import directory as directory_sch


router = APIRouter(prefix='/directories', tags=['directories'])


def _map_schema_to_repr(
        directory: directory_sch.DirectoryCreate, user_id: int
) -> DirectoryRepr:
    return DirectoryRepr(
        name=directory.name,
        user_id=user_id
    )


@router.get('/', response_model=list[directory_sch.DirectoryGet])
def get_directories(
        active_user: UserRepr = Depends(ActiveUserS),
        directory_service: DirectoryService = Depends(DirectoryServiceS),
        pagination: PaginationParams = Depends()
):
    try:
        return directory_service.get_all(
            active_user.id, pagination.offset, pagination.limit
        )
    except service_exc.NotFoundError as err:
        raise http_exc.ObjectNotExistInPath(err.model)


@router.post(
    '/', response_model=directory_sch.DirectoryGet,
    status_code=status.HTTP_201_CREATED
)
def create_directory(
        directory: directory_sch.DirectoryCreate,
        active_user: UserRepr = Depends(ActiveUserS),
        directory_service: DirectoryService = Depends(DirectoryServiceS)
):
    directory_repr = _map_schema_to_repr(directory, active_user.id)

    try:
        return directory_service.create(
            directory_repr
        )
    except service_exc.NotFoundError as err:
        raise http_exc.ObjectNotExistInPath(err.model)
    except service_exc.AlreadyExistError as err:
        raise http_exc.ObjectAlreadyExistInBody(err.model, err.attr)


@router.get('/{directory_id}/', response_model=directory_sch.DirectoryGet)
def get_directory(
        directory_id: int,
        active_user: UserRepr = Depends(ActiveUserS),
        directory_service: DirectoryService = Depends(DirectoryServiceS)
):
    try:
        return directory_service.get(active_user.id, directory_id)
    except service_exc.NotFoundError as err:
        raise http_exc.ObjectNotExistInPath(err.model)


@router.delete(
    '/{directory_id}/', response_class=Response,
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_directory(
        directory_id: int,
        active_user: UserRepr = Depends(ActiveUserS),
        directory_service: DirectoryService = Depends(DirectoryServiceS)
):
    try:
        directory_service.delete(active_user.id, directory_id)
    except service_exc.NotFoundError as err:
        raise http_exc.ObjectNotExistInPath(err.model)
