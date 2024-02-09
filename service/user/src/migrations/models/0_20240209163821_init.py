from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS `user` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `time_created` DATETIME(6) NOT NULL  DEFAULT CURRENT_TIMESTAMP(6),
    `time_updated` DATETIME(6) NOT NULL  DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    `time_deleted` DATETIME(6),
    `email` VARCHAR(30) NOT NULL UNIQUE,
    `username` VARCHAR(30) NOT NULL UNIQUE,
    `first_name` VARCHAR(30) NOT NULL,
    `last_name` VARCHAR(30) NOT NULL,
    `password` LONGBLOB,
    `is_admin` BOOL NOT NULL  DEFAULT 0,
    `email_validated` BOOL NOT NULL  DEFAULT 0,
    `code` VARCHAR(10) NOT NULL
) CHARACTER SET utf8mb4 COMMENT='Модель базы данных для пользователя';
CREATE TABLE IF NOT EXISTS `aerich` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `version` VARCHAR(255) NOT NULL,
    `app` VARCHAR(100) NOT NULL,
    `content` JSON NOT NULL
) CHARACTER SET utf8mb4;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
