from tortoise.fields import (
    BinaryField,
    BooleanField,
    CharField,
    DatetimeField,
    ForeignKeyField,
    IntField,
    ManyToManyField,
    OneToOneField,
    UUIDField,
)
from tortoise.models import Model


class BaseModel(Model):
    """Абстрактный класс для моделей."""

    id = IntField(pk=True)

    class Meta:
        """Класс с метаданными."""

        abstract = True


class TimesBaseModel(BaseModel):
    """Абстрактный класс для моделей."""

    time_created = DatetimeField(auto_now_add=True)
    time_updated = DatetimeField(auto_now=True)
    time_deleted = DatetimeField(null=True)

    class Meta:
        """Класс с метаданными."""

        abstract = True


class User(TimesBaseModel):
    """Модель базы данных для пользователя"""

    email = CharField(max_length=30, unique=True)

    username = CharField(max_length=30, unique=True)
    first_name = CharField(max_length=30)
    last_name = CharField(max_length=30)
    password = CharField(max_length=100)

    is_admin = BooleanField(default=False)

    email_validated = BooleanField(default=False)
    code = CharField(max_length=10)
