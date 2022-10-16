from fastapi.responses import JSONResponse
from fastapi.requests import Request

from fastapi_jwt_auth.exceptions import AuthJWTException


def authjwt_exception_handler(_: Request, exc: AuthJWTException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message}
    )
