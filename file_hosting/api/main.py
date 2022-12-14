import os
from typing import Type

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from fastapi_jwt_auth import AuthJWT

from sqlalchemy.orm import DeclarativeMeta

from config import DatabaseSettings, JWTSettings

from database import utils as db_utils
from database.models import HostingBase

from .dependencies import stubs
from .dependencies import providers

from .routers import hosting_router
from .exceptions import handlers
from .exceptions import base_exc


def _include_routers(app: FastAPI) -> None:
    app.include_router(hosting_router.router, prefix='/api/v1')


def _include_handlers(app: FastAPI) -> None:
    app.add_exception_handler(
        handlers.AuthJWTException, handlers.authjwt_exception_handler
    )
    app.add_exception_handler(
        base_exc.ObjectNotExist, handlers.object_not_exist_handler
    )
    app.add_exception_handler(
        base_exc.ObjectAlreadyExist, handlers.object_already_exist_handler
    )
    app.add_exception_handler(
        base_exc.InvalidData, handlers.invalid_data_handler
    )


def _include_services(app: FastAPI) -> None:
    app.dependency_overrides[stubs.UserServiceS] = \
        providers.UserServiceProvider()
    app.dependency_overrides[stubs.FileServiceS] = \
        providers.FileServiceProvider()
    app.dependency_overrides[stubs.DirectoryServiceS] = \
        providers.DirectoryServiceProvider()


def _include_database(
        app: FastAPI, config: DatabaseSettings, base: Type[DeclarativeMeta]
):
    engine = db_utils.create_engine(config)
    session_maker = db_utils.create_session_maker(engine)

    app.dependency_overrides[stubs.SessionS] = \
        providers.DatabaseProvider(session_maker)

    db_utils.create_tables(base, engine)


def _include_auth(app: FastAPI) -> None:
    app.dependency_overrides[stubs.ActiveUserS] = \
        providers.ActiveUserProvider()


def _include_cors(app: FastAPI, origins: list[str]) -> None:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


def _include_static(app: FastAPI) -> None:
    os.makedirs('./media/', exist_ok=True)

    app.mount('/media/', StaticFiles(directory='media'), name='media')


def create_app() -> FastAPI:
    app = FastAPI(docs_url='/api/v1/docs/', redoc_url=None)
    db_config = DatabaseSettings(_env_file='.env')

    origins = ['*']

    _include_database(app, db_config, HostingBase)
    _include_services(app)
    _include_routers(app)
    _include_handlers(app)
    _include_cors(app, origins)
    _include_auth(app)
    _include_static(app)

    return app


@AuthJWT.load_config
def get_config():
    return JWTSettings(_env_file='.env')


api = create_app()
