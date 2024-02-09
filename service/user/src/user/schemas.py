from pydantic import BaseModel, EmailStr, Field


class CreateUser(BaseModel):
    username: str
    first_name: str
    last_name: str
    password: str
    email: EmailStr


class CreateUserRepo(CreateUser):
    code: str


class SignUpRequest(CreateUser):
    pass


class SignInRequest(BaseModel):
    email: EmailStr
    password: str


class BaseUserRequest(BaseModel):
    token: str


class VerifyEmailRequest(BaseUserRequest):
    code: str


class UserModel(BaseModel):
    email: str
    email_validated: bool
    username: str
    first_name: str
    last_name: str
    is_admin: bool
