import os

from dotenv import load_dotenv

# Load the stored environment variables
load_dotenv()
print(os.getenv("DB_URL"))
# -------- Server URL settings -------- #
HOST = "127.0.0.1"
PORT = 8001
# -------- Server URL settings -------- #

# -------- Microservice URL settings -------- #
USER_SERVICE = "127.0.0.1:8000"
# -------- Microservice URL settings -------- #

# -------- DataBase settings -------- #
DATABASE = {  # Основной кофиг БД
    "DB_URL": os.getenv("DB_URL"),
    "GENERATE_SCHEMAS": True,
    "MODULES": {
        "models": [
            "ml.models",
            "aerich.models",
        ],  #  Добавь в модели путь д освоего нового приложения которое ты создаешь в папке apps
    },
}

TORTOISE_ORM = {  # Нужно для миграций aerich
    "connections": {"default": DATABASE.get("DB_URL")},
    "apps": {
        "models": {
            "models": DATABASE.get("MODULES").get("models"),
            "default_connection": "default",
        },
    },
}
# -------- DataBase settings -------- #
