from tortoise.transactions import in_transaction
from user import models, schemas


class UserRepository:
    def __init__(self, model: models.User):
        self.model = model

    async def exitst_by_username(self, username: str) -> bool:
        return await self.model.exists(username=username)

    async def exitst_by_email(self, email: str) -> bool:
        return await self.model.exists(email=email)

    async def get_by_id(self, user_id: int) -> models.User:
        return await self.model.get(id=user_id)

    async def get_by_email(self, email: str) -> models.User:
        return await self.model.get(email=email)

    async def get_by_username(self, username: str) -> models.User:
        return await self.model.get(username=username)

    async def get_by_uuid(self, uuid: str) -> models.User:
        return await self.model.get(uuid=uuid)

    async def email_verify(self, user: models.User):
        user.email_validated = True
        await user.save()

    async def create(self, data: schemas.CreateUserRepo, is_admin=False):

        async with in_transaction() as transaction:
            user: models.User = self.model(
                first_name=data.first_name,
                last_name=data.last_name,
                username=data.username,
                email=data.email,
                password=data.password,
                code=data.code,
            )
            if is_admin:
                # TODO: alert
                user.is_admin = True

            await user.save(using_db=transaction)
        return user
