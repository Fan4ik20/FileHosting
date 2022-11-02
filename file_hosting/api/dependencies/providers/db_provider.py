from typing import Generator

from sqlalchemy.orm import sessionmaker
from .typing_ import DbSession


class DatabaseProvider:
    def __init__(self, session_maker: sessionmaker) -> None:
        self._session_maker = session_maker

    def __call__(self) -> Generator[DbSession, None, None]:
        with self._session_maker() as session:
            yield session
