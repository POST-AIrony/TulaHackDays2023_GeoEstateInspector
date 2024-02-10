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


class PhotoFromUser(TimesBaseModel):
    from_user_id: int = IntField()
    reult_src: str = CharField(max_length=200)
