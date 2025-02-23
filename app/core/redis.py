from typing import Optional, Any
from redis import asyncio as aioredis
from app.core.config import settings


class RedisClient:
    def __init__(self):
        self.redis_url = f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}"
        if settings.REDIS_PASSWORD:
            self.redis_url = f"redis://:{settings.REDIS_PASSWORD}@{settings.REDIS_HOST}:{settings.REDIS_PORT}"
        self.pool = None

    async def get_connection(self):
        if self.pool is None:
            self.pool = aioredis.ConnectionPool.from_url(
                self.redis_url, max_connections=10, decode_responses=True
            )
        return aioredis.Redis(connection_pool=self.pool)

    async def get(self, key: str) -> Optional[Any]:
        redis = await self.get_connection()
        try:
            return await redis.get(key)
        finally:
            await redis.close()

    async def set(self, key: str, value: Any, expire: int = None):
        redis = await self.get_connection()
        try:
            await redis.set(key, value, ex=expire)
        finally:
            await redis.close()

    async def delete(self, key: str):
        redis = await self.get_connection()
        try:
            await redis.delete(key)
        finally:
            await redis.close()


redis_client = RedisClient()
