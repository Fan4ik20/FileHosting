from typing import Type

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from sqlalchemy.orm import DeclarativeMeta

from config import DatabaseSettings

from database import utils as db_utils
from database.models import HostingBase

from .routers import hosting_router


def _include_routers(app: FastAPI) -> None:
    app.include_router(hosting_router.router, prefix='api/v1')


def _include_handlers(app: FastAPI) -> None:
    pass


def _include_database(
        app: FastAPI, config: DatabaseSettings, base: Type[DeclarativeMeta]
):
    engine = db_utils.create_engine(config)
    session_maker = db_utils.create_session_maker(engine)

    db_utils.create_tables(base, engine)


def _include_cors(app: FastAPI, origins: list[str]) -> None:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


def create_app() -> FastAPI:
    app = FastAPI(docs_url='/api/v1/docs/', redoc_url=None)
    db_config = DatabaseSettings(_env_file='.env')

    origins = ['*']

    _include_database(app, db_config, HostingBase)
    _include_routers(app)
    _include_handlers(app)
    _include_cors(app, origins)

    return app


api = create_app()
