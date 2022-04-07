from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class AuthLogin(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=255)


class AuthToken(BaseModel):
    access_token: str
    token_type: str


class AuthTokenData(BaseModel):
    email: Optional[EmailStr] = None
