from pydantic import BaseModel, Field, EmailStr


class UserBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr

    class Config:
        orm_mode = True


class UserList(UserBase):
    id: int
    is_admin: bool


class UserCreate(UserBase):
    password: str = Field(..., min_length=8, max_length=255)
    confirm_password: str = Field(..., min_length=8, max_length=255)
    description: str


class UserView(UserBase):
    id: int
    description: str = Field(..., max_length=1000)
    is_admin: bool


class UserUpdate(BaseModel):
    first_name: str
    last_name: str
    description: str = Field(..., max_length=1000)


