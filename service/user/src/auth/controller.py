from auth.service import AuthService, get_service
from fastapi import APIRouter, Depends, Request
from user import schemas

auth = APIRouter()


@auth.post("/sign-up")
async def sign_up(
    request: Request,
    data: schemas.SignUpRequest,
    service: AuthService = Depends(get_service),
):
    return await service.sign_up(data=data)


@auth.post("/sign-in")
async def sign_in(
    request: Request,
    data: schemas.SignInRequest,
    service: AuthService = Depends(get_service),
):
    return await service.sign_in(data=data)


@auth.post("/verify/email")
async def verify_email(
    request: Request,
    data: schemas.VerifyEmailRequest,
    service: AuthService = Depends(get_service),
):
    return await service.verify_email(data=data)


@auth.post("/verify/send")
async def verify_email_send(
    request: Request,
    data: schemas.BaseUserRequest,
    service: AuthService = Depends(get_service),
):
    return await service.verify_email_send(data=data)
