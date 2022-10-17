from typing import TypeAlias

import os
import uuid
import shutil

from uuid import UUID

from fastapi import UploadFile

path: TypeAlias = str


def _get_path_to_save(
        username: str, directory_id: int
) -> path:
    return (
        f'./media/users/{username}/directory_{directory_id}/files'
    )


def _get_path_to_file(path_to_save: path, file_id: UUID, file: UploadFile):
    filetype = file.filename.split('.')[-1]

    return f'{path_to_save}/{file_id}.{filetype}'


def write_and_get_file_path(
        username: str, directory_id: int, attachment: UploadFile
) -> path:
    path_to_save = _get_path_to_save(username, directory_id)

    os.makedirs(path_to_save, exist_ok=True)

    file_id = uuid.uuid4()
    file_path = _get_path_to_file(path_to_save, file_id, attachment)
    with open(file_path, 'wb') as file:
        shutil.copyfileobj(attachment.file, file)

    return file_path[1:]
