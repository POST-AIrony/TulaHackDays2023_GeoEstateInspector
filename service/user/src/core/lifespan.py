from contextlib import asynccontextmanager

from core import database, settings
from fastapi import FastAPI


@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.init(
        db_url=settings.DATABASE.get("DB_URL"),
        modules=settings.DATABASE.get("MODULES"),
        generate_schemas=settings.DATABASE.get("GENERATE_SCHEMAS"),
    )
    yield
    await database.close()
