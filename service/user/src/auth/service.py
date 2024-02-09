from core import tdq
from user import models, repository, schemas, utils


class AuthService:
    def __init__(self, userRepo: repository.UserRepository):
        self.userRepo = userRepo

    async def sign_up(self, data: schemas.SignUpRequest):

        if await self.userRepo.exitst_by_username(data.username):
            raise
        if await self.userRepo.exitst_by_email(data.email):
            raise
        try:
            user = await self.userRepo.create(
                schemas.CreateUserRepo(
                    first_name=data.first_name,
                    last_name=data.last_name,
                    email=data.email,
                    password=utils.get_hashed_password(data.password),
                    username=data.username,
                    code=await utils.generate_email_verification_code(),
                )
            )
        except Exception as e:
            raise e

        tdq.send_email_verification_code.send(user.email, user.code)

        return utils.create_access_token(user.id)

    async def sign_in(self, data: schemas.SignInRequest):
        try:
            user = await self.userRepo.get_by_email(email=data.email)
        except Exception as e:
            raise e

        if utils.verify_password(data.password, user.password):
            return utils.create_access_token(user.id)
        raise  # TODO:

    async def verify_email(self, data: schemas.VerifyEmailRequest):
        token_data = await utils.decode_token(data.token)
        print(token_data.get("sub"))

        try:
            user = await self.userRepo.get_by_id(user_id=int(token_data.get("sub")))
        except Exception as e:
            raise e  # TODO:
        print(user.code, data.code)

        if user.code == data.code:
            await self.userRepo.email_verify(user)
            return "OK"
        raise  # TODO:

    async def verify_email_send(self, data: schemas.BaseUserRequest):
        token_data = await utils.decode_token(data.token)
        try:
            user = await self.userRepo.get_by_id(user_id=int(token_data.get("sub")))
        except Exception as e:
            raise e  # TODO:

        tdq.send_email_verification_code.send(user.email, user.code)
        return "OK"


def get_service():
    return AuthService(repository.UserRepository(models.User))
