from fastapi.responses import JSONResponse
from fastapi.requests import Request

from fastapi_jwt_auth.exceptions import AuthJWTException

from . import base_exc


def authjwt_exception_handler(
        _: Request, exc: AuthJWTException
) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message}
    )


def object_not_exist_handler(
        _: Request, exc: base_exc.ObjectNotExist
) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={
            'message': f'{exc.model} with given identifier not found',
            'place': f'{exc.place}'
        }
    )


def object_already_exist_handler(
        _: Request, exc: base_exc.ObjectAlreadyExist
) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={
            'message': f'{exc.model} with given {exc.attr} already exist',
            'place': f'{exc.place}'
        }
    )


def invalid_data_handler(
        _: Request, exc: base_exc.InvalidData
) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={
            'message': f'You passed wrong {exc.model} {exc.attr}',
            'place': f'{exc.place}'
        }
    )
