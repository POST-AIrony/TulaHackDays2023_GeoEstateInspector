import os

from dotenv import load_dotenv

# Load the stored environment variables
load_dotenv()
# -------- Server URL settings -------- #
HOST = "127.0.0.1"
PORT = 8000
# -------- Server URL settings -------- #

# -------- JWT settings -------- #
ACCESS_TOKEN_EXPIRE_MINUTES = 1 * 60 * 24 * 7  # 7 days
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 days
ALGORITHM = os.getenv("ALGORITHM")
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")  # should be kept secret
JWT_REFRESH_SECRET_KEY = os.getenv("JWT_REFRESH_SECRET_KEY")  # should be kept secret
# -------- JWT settings -------- #

# -------- DataBase settings -------- #
DATABASE = {  # Основной кофиг БД
    "DB_URL": os.getenv("DB_URL"),
    "GENERATE_SCHEMAS": True,
    "MODULES": {
        "models": [
            "user.models",
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


# -------- Redis settings -------- #
REDIS_URL = "localhost:6379"
# -------- Redis settings -------- #

# -------- SMTP settings -------- #
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
SMTP_NAME = "test1"
SMTP_USER = os.getenv("SMTP_USER")
SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = "465"
# -------- SMTP settings -------- #
