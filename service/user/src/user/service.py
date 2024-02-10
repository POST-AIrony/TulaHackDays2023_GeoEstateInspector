from core import handlers  # Импорт модуля handlers из пакета core
from user import models  # Импорт модулей из пакета user
from user import exceptions, repository, schemas, service, utils


class UserService:
    # Класс UserService для работы с пользователями
    def __init__(self, userRepo: repository.UserRepository):
        # Конструктор класса, принимает объект репозитория пользователей
        self.userRepo = userRepo

    async def me(self, data: schemas.BaseUserRequest) -> schemas.UserModel:
        # Метод для получения информации о текущем пользователе
        token_data = await handlers.token_decode_handler(data.token)
        # Расшифровка токена с использованием handlers.token_decode_handler
        try:
            user = await self.userRepo.get_by_id(user_id=int(token_data.get("sub")))
            # Получение пользователя по его идентификатору
        except:
            raise exceptions.UserNotFound
            # Если пользователя не найдено, вызывается исключение UserNotFound
        return schemas.UserModel(
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
            email_validated=user.email_validated,
            is_admin=user.is_admin,
            username=user.username,
        )
        # Возвращается модель пользователя

    async def history(self, data: schemas.BaseUserRequest):
        pass  # TODO: call adapter and send API query to ML-Service
        # Метод для получения истории пользователя, пока не реализован

    async def user_feedback(self, data: schemas.BaseUserRequest) -> schemas.UserModel:
        return await self.me(data)
        # Метод для обработки обратной связи пользователя, вызывает метод me для получения информации о пользователе


def get_service():
    return UserService(repository.UserRepository(models.User))
    # Функция get_service, возвращающая экземпляр класса UserService, инициализированный с помощью репозитория UserRepository и модели User
