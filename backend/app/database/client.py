from motor.motor_asyncio import AsyncIOMotorClient

from app.config.settings import settings


class MongoClientManager:
    def __init__(self):
        self._client: AsyncIOMotorClient | None = None

    def get_client(self) -> AsyncIOMotorClient:
        if self._client is None:
            self._client = AsyncIOMotorClient(settings.MONGO_URI)
        return self._client

    def get_db(self):
        return self.get_client().get_default_database()


mongo_client = MongoClientManager()

def get_db():
    return mongo_client.get_db()
