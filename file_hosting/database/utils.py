from typing import Type

from sqlalchemy import create_engine as _create_engin
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker, DeclarativeMeta

from config import DatabaseSettings


def create_engine(config: DatabaseSettings) -> Engine:
    return _create_engin(config.DB_URL)


def create_session_maker(engine: Engine) -> sessionmaker:
    return sessionmaker(bind=engine, autoflush=False)


def create_tables(base_class: Type[DeclarativeMeta], engine: Engine) -> None:
    base_class.metadata.create_all(bind=engine)
