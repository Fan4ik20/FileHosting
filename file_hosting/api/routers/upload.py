from fastapi import APIRouter, status, Depends, UploadFile

from database.repositories.representations.user import UserRepr

from api.dependencies.stubs.auth import ActiveUserS

from api.utils.files import write_and_get_file_path


router = APIRouter(
    prefix='/directories/{directory_id}/files/upload',
    tags=['Files']
)


@router.post('/', status_code=status.HTTP_201_CREATED)
def upload_file(
        directory_id: int, files: list[UploadFile],
        active_user: UserRepr = Depends(ActiveUserS)
):
    urls = []

    for file in files:
        urls.append(write_and_get_file_path(
            active_user.username, directory_id, file
        ))

    return {'files': [{'url': url} for url in urls]}
