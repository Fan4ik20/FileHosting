from pydantic import BaseModel, PositiveInt, EmailStr


class UserBase(BaseModel):
    email: EmailStr
    username: str


class UserGet(UserBase):
    id: PositiveInt

    class Config:
        orm_mode = True


class UserCreate(UserBase):
    password: str


class UserLogin(BaseModel):
    username: str
    password: str
