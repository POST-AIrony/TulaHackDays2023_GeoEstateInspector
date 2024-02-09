import datetime
import random

from core import settings
from jose import jwt
from passlib.context import CryptContext

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_access_token(subject: int, expires_delta: int = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.datetime.utcnow() + datetime.timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )

    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, settings.ALGORITHM)
    return encoded_jwt


async def decode_token(token: str) -> dict:
    payload = jwt.decode(
        token, settings.JWT_SECRET_KEY, algorithms=[settings.ALGORITHM]
    )

    if (
        datetime.datetime.fromtimestamp(payload.get("exp")) < datetime.datetime.now()
    ):  # TODO: check if err
        raise TimeoutError

    return payload


def get_hashed_password(password: str) -> str:
    return password_context.hash(password)


def verify_password(password: str, hashed_pass: str) -> bool:
    return password_context.verify(password, hashed_pass)


async def generate_email_verification_code(lenght: int = 6) -> str:
    return "".join(random.choice(list("1234567890")) for _ in range(lenght))
