from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `user` MODIFY COLUMN `password` VARCHAR(100) NOT NULL;
        ALTER TABLE `user` MODIFY COLUMN `password` VARCHAR(100) NOT NULL;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `user` MODIFY COLUMN `password` LONGBLOB;
        ALTER TABLE `user` MODIFY COLUMN `password` LONGBLOB;"""
