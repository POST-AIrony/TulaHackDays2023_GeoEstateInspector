from tortoise import Tortoise, connections


async def init(db_url, modules, generate_schemas: bool = False):
    """
    Инициализирует подключение к базе данных и генерирует схемы базы данных при необходимости.

    Параметры:
        db_url (str): URL базы данных.
        modules (list): Список модулей, содержащих модели базы данных.
        generate_schemas (bool, optional): Флаг, указывающий, нужно ли генерировать схемы базы данных.
            По умолчанию установлено значение False.

    Возвращает:
        None

    Примеры:
        >>> await init("postgresql://user:password@localhost:5432/mydatabase", ["models"])
    """
    await Tortoise.init(db_url=db_url, modules=modules)
    if generate_schemas:
        await Tortoise.generate_schemas()


async def close():
    """
    Закрывает все активные соединения с базой данных.

    Параметры:
        None

    Возвращает:
        None

    Примеры:
        >>> await close()
    """
    await connections.close_all()
