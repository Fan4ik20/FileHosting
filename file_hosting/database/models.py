from datetime import datetime
from uuid import uuid4, UUID as TUUID
from typing import Iterable, Type

from sqlalchemy import (
    Column, Integer, String, ForeignKey, DateTime, func, UniqueConstraint
)
from sqlalchemy.dialects.postgresql import UUID as UUID_C
from sqlalchemy.orm import \
    declarative_base, relationship, backref, Mapped, DeclarativeMeta

HostingBase: Type[DeclarativeMeta] = declarative_base()


class User(HostingBase):
    __tablename__ = 'users'

    id: Mapped[int] = Column(Integer, primary_key=True)

    username: Mapped[str] = Column(String(100), unique=True, nullable=False)
    email: Mapped[str] = Column(String(150), unique=True, nullable=False)
    password: Mapped[str] = Column(String, nullable=False)


class Directory(HostingBase):
    __tablename__ = 'directories'

    id: Mapped[int] = Column(Integer, primary_key=True)

    name: Mapped[str] = Column(String(100), nullable=False)

    user_id: Mapped[int] = Column(
        Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False
    )
    user: Mapped['User'] = relationship('User', backref='directories')

    directory_id: Mapped[int | None] = Column(
        Integer, ForeignKey('directories.id', ondelete='CASCADE')
    )

    inner_dirs: Mapped[Iterable['Directory']] = relationship(
        'Directory', backref=backref('external_dir', remote_side=[id])
    )
    files: Mapped[Iterable['File']] = relationship(
        'File', back_populates='directories'
    )

    __table_args__ = (UniqueConstraint('name', 'user_id', 'directory_id'),)


class File(HostingBase):
    __tablename__ = 'files'

    id: TUUID = Column(UUID_C(as_uuid=True), primary_key=True, default=uuid4)

    url: Mapped[str] = Column(String, nullable=False)
    name: Mapped[str] = Column(String, nullable=False)
    type: Mapped[str] = Column(String, nullable=False)
    time_added: Mapped[datetime] = Column(DateTime, server_default=func.now())

    directory_id: Mapped[int] = Column(
        Integer, ForeignKey('directories.id', ondelete='CASCADE'),
        nullable=False
    )
    directory: Mapped['Directory'] = relationship(
        'Directory', back_populates='files'
    )
