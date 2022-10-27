from dataclasses import dataclass


__all__ = ['UserRepr']


@dataclass
class UserRepr:
    username: str
    email: str
    password: str

    id: int | None = None
