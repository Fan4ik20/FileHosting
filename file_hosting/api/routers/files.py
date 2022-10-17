from uuid import UUID

from fastapi import APIRouter, Depends, status
from fastapi.responses import Response

from database.repositories.representations.user import UserRepr

from services.abstract.file_base import AFileService, FileRepr
from services.exceptions import base as service_exc

from api.dependencies.stubs.services import FileServiceS
from api.dependencies.stubs.auth import ActiveUserS

from api.exceptions import exc as http_exc

from api.dependencies.utils import PaginationParams

from .schemas.file import FileGet, FilePost


def _map_schema_to_repr(directory_id: int, file_sch: FilePost) -> FileRepr:
    return FileRepr(
        url=file_sch.url,
        directory_id=directory_id,
        type=file_sch.type,
        name=file_sch.type
    )


router = APIRouter(prefix='/directories/{directory_id}/files', tags=['Files'])


@router.get('/', response_model=list[FileGet])
def get_files(
        directory_id: int, pagination: PaginationParams = Depends(),
        user: UserRepr = Depends(ActiveUserS),
        file_service: AFileService = Depends(FileServiceS)
):
    try:
        return file_service.get_all(
            user.id, directory_id, pagination.offset, pagination.limit
        )
    except service_exc.NotFoundError as err:
        raise http_exc.ObjectNotExistInPath(err.model)


@router.post('/', response_model=FileGet, status_code=status.HTTP_201_CREATED)
def create_file(
        directory_id: int, file_sch: FilePost,
        user: UserRepr = Depends(ActiveUserS),
        file_service: AFileService = Depends(FileServiceS)
):
    file_repr = _map_schema_to_repr(directory_id, file_sch)

    try:
        return file_service.create(user.id, file_repr)
    except service_exc.NotFoundError as err:
        raise http_exc.ObjectNotExistInPath(err.model)


@router.get('/{file_id}/', response_model=FileGet)
def get_file(
        directory_id: int, file_id: UUID,
        user: UserRepr = Depends(ActiveUserS),
        file_service: AFileService = Depends(FileServiceS)
):
    try:
        return file_service.get(user.id, directory_id, file_id)
    except service_exc.NotFoundError as err:
        raise http_exc.ObjectNotExistInPath(err.model)


@router.delete(
    '/{file_id}/', response_class=Response,
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_file(
        directory_id: int, file_id: UUID,
        user: UserRepr = Depends(ActiveUserS),
        file_service: AFileService = Depends(FileServiceS)
):
    try:
        return file_service.delete(user.id, directory_id, file_id)
    except service_exc.NotFoundError as err:
        raise http_exc.ObjectNotExistInPath(err.model)
