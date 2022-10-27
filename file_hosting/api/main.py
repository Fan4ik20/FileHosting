import os
from typing import Type

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from fastapi_jwt_auth import AuthJWT

from sqlalchemy.orm import DeclarativeMeta, sessionmaker

from config import DatabaseSettings, JWTSettings

from database import utils as db_utils
from database.models import HostingBase

from .dependencies.stubs import auth as auth_s
from .dependencies.stubs import services as services_s

from .dependencies import utils as dependency_utils

from database.repositories import (
    UserRepository, DirectoryRepository, FileRepository
)

from services import UserService, DirectoryService, FileService

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


def _include_services(app: FastAPI, session_maker: sessionmaker) -> None:
    user_rep = UserRepository(session_maker)
    directory_rep = DirectoryRepository(session_maker)
    file_rep = FileRepository(session_maker)

    app.dependency_overrides[services_s.UserServiceS] = \
        lambda: UserService(user_rep)
    app.dependency_overrides[services_s.DirectoryServiceS] = \
        lambda: DirectoryService(directory_rep, user_rep)
    app.dependency_overrides[services_s.FileServiceS] = \
        lambda: FileService(file_rep, user_rep, directory_rep)


def _include_database(
        app: FastAPI, config: DatabaseSettings, base: Type[DeclarativeMeta]
):
    engine = db_utils.create_engine(config)
    session_maker = db_utils.create_session_maker(engine)

    _include_services(app, session_maker)

    db_utils.create_tables(base, engine)


def _include_auth(app: FastAPI) -> None:
    app.dependency_overrides[auth_s.ActiveUserS] = \
        dependency_utils.get_current_user


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
