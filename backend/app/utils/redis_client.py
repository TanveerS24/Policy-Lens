from redis.asyncio import Redis, from_url

from app.config.settings import settings


class RedisClient:
    def __init__(self):
        self._client: Redis | None = None

    async def get_client(self) -> Redis:
        if self._client is None:
            self._client = from_url(settings.REDIS_URL, decode_responses=True)
        return self._client


redis_client = RedisClient()
