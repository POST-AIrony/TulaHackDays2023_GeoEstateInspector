from fastapi import APIRouter, Depends, Request
from user import schemas
from user.service import UserService, get_service

user = APIRouter()


@user.post("/me")
async def me(
    request: Request,
    data: schemas.BaseUserRequest,
    service: UserService = Depends(get_service),
) -> schemas.UserModel:
    return await service.me(data)


@user.post("/me/history")
async def history(
    request: Request,
    data: schemas.BaseUserRequest,
    service: UserService = Depends(get_service),
):
    return await service.history(
        data
    )  # TODO: call adapter and send API query to ML-Service


@user.post("/adapters/user_feedback", tags=["adapter"])
async def user_feedback(
    request: Request,
    data: schemas.BaseUserRequest,
    service: UserService = Depends(get_service),
):
    return await service.user_feedback(data=data)
