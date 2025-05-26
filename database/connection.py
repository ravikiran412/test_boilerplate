from motor.motor_asyncio import AsyncIOMotorClient
from config.database import db_settings

class Database:
    client: AsyncIOMotorClient = None
    db = None

    @classmethod
    async def connect_db(cls):
        cls.client = AsyncIOMotorClient(
            db_settings.MONGODB_URL,
            directConnection=db_settings.MONGODB_DIRECT_CONNECTION,
            serverSelectionTimeoutMS=db_settings.MONGODB_SERVER_SELECTION_TIMEOUT_MS
        )
        cls.db = cls.client[db_settings.MONGODB_DB_NAME]

    @classmethod
    async def close_db(cls):
        if cls.client:
            cls.client.close()

    @classmethod
    def get_db(cls):
        return cls.db 