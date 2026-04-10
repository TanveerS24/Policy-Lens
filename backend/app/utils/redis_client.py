import aioredis

from app.config.settings import settings


class RedisClient:
    def __init__(self):
        self._client: aioredis.Redis | None = None

    async def get_client(self) -> aioredis.Redis:
        if self._client is None:
            self._client = aioredis.from_url(settings.REDIS_URL, decode_responses=True)
        return self._client


redis_client = RedisClient()
