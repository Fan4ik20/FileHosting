from uuid import uuid4

from sqlalchemy import (
    Column, Integer, String, ForeignKey, DateTime, func, UniqueConstraint
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base, relationship

HostingBase = declarative_base()


class User(HostingBase):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)

    username = Column(String(100), unique=True, nullable=False)
    email = Column(String(150), unique=True, nullable=False)
    password = Column(String, nullable=False)


class Directory(HostingBase):
    __tablename__ = 'directories'

    id = Column(Integer, primary_key=True)

    name = Column(String(100), nullable=False)

    user_id = Column(
        Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False
    )
    user = relationship('User', backref='directories')

    __table_args__ = (UniqueConstraint('name', 'user_id'),)


class File(HostingBase):
    __tablename__ = 'files'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)

    url = Column(String, nullable=False)
    name = Column(String, nullable=False)
    type = Column(String, nullable=False)
    time_added = Column(DateTime, server_default=func.now())

    directory_id = Column(
        Integer, ForeignKey('directories.id', ondelete='CASCADE'),
        nullable=False
    )
    user = relationship('Directory', backref='files')
