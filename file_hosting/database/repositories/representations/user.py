from dataclasses import dataclass


@dataclass
class UserRepr:
    username: str
    email: str
    password: str

    id: int | None = None
