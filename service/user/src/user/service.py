from user import exceptions, models, repository, schemas, service, utils


class UserService:
    def __init__(self, userRepo: repository.UserRepository):
        self.userRepo = userRepo

    async def me(self, data: schemas.BaseUserRequest) -> schemas.UserModel:
        token_data = await utils.decode_token(data.token)

        try:
            user = await self.userRepo.get_by_id(user_id=int(token_data.get("sub")))
        except:
            raise exceptions.UserNotFound

        return schemas.UserModel(
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
            email_validated=user.email_validated,
            is_admin=user.is_admin,
            username=user.username,
        )

    async def history(self, data: schemas.BaseUserRequest):
        pass  # TODO: call adapter and send API query to ML-Service

    async def user_feedback(self, data: schemas.BaseUserRequest) -> schemas.UserModel:
        return await self.me(data)


def get_service():
    return UserService(repository.UserRepository(models.User))
