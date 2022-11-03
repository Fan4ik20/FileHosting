from dataclasses import dataclass


__all__ = ['UserDTO', 'UserCreateDTO', 'UserUpdateDTO', 'UserBaseDTO']


class UserBaseDTO:
    pass


@dataclass(frozen=True)
class UserDTO(UserBaseDTO):
    id: int
    username: str
    email: str
    password: str


@dataclass
class UserCreateDTO(UserBaseDTO):
    username: str
    email: str
    password: str


@dataclass(frozen=True)
class UserUpdateDTO(UserBaseDTO):
    username: str | None = None
    email: str | None = None
    password: str | None = None
