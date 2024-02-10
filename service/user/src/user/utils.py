import datetime  # Импорт модуля datetime для работы с датой и временем
import random  # Импорт модуля random для генерации случайных чисел

from core import handlers, settings  # Импорт модуля handlers и settings из пакета core
from jose import jwt  # Импорт модуля jwt для работы с JSON Web Tokens
from passlib.context import (
    CryptContext,
)  # Импорт модуля CryptContext из пакета passlib для хеширования паролей

password_context = CryptContext(
    schemes=["bcrypt"], deprecated="auto"
)  # Инициализация контекста хеширования паролей с использованием схемы bcrypt


async def create_access_token(subject: int, expires_delta: int = None) -> str:
    # Функция для создания доступного токена аутентификации
    if expires_delta is not None:
        expires_delta = datetime.datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.datetime.utcnow() + datetime.timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    # Вычисление времени истечения токена
    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, settings.ALGORITHM)
    # Кодирование токена с использованием секретного ключа и алгоритма
    return encoded_jwt


async def decode_token(token: str) -> dict:
    # Функция для расшифровки токена
    payload = jwt.decode(
        token, settings.JWT_SECRET_KEY, algorithms=[settings.ALGORITHM]
    )
    # Расшифровка токена с использованием секретного ключа и алгоритма
    if datetime.datetime.fromtimestamp(payload.get("exp")) < datetime.datetime.now():
        raise TimeoutError
    # Проверка истечения срока действия токена
    return payload


async def get_hashed_password(password: str) -> str:
    # Функция для получения хешированного пароля
    return password_context.hash(password)
    # Хеширование пароля с использованием контекста хеширования


async def verify_password(password: str, hashed_pass: str) -> bool:
    # Функция для проверки пароля
    return password_context.verify(password, hashed_pass)
    # Проверка соответствия пароля и хешированного пароля


async def generate_email_verification_code(lenght: int = 6) -> str:
    # Функция для генерации кода подтверждения электронной почты
    return "".join(random.choice(list("1234567890")) for _ in range(lenght))
    # Генерация случайной последовательности цифр указанной длины
