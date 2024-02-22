from typing import Optional
from pydantic import BaseModel, EmailStr


class CreateUserRequestBody(BaseModel):
    email: EmailStr
    password: str
    confirm_password: str
    full_name: Optional[str] = None


class AuthenticateUserRequestBody(BaseModel):
    email: EmailStr
    password: str


class SettingsRequestBody(BaseModel):
    email: Optional[EmailStr]
    full_name: Optional[str]
    allow_kudos: Optional[bool] = True
    allow_subscriptions: Optional[bool] = True
