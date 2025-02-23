from datetime import datetime
from app.core.redis import RedisClient


class RateLimitExceeded(Exception):
    pass


async def check_rate_limit(
    redis: RedisClient,
    user_id: str,
    limit: int = 60,  # requests per minute
    window: int = 60,  # window in seconds
) -> bool:
    """
    Check if the user has exceeded their rate limit.
    Uses a sliding window counter implementation.
    """
    current_timestamp = datetime.utcnow().timestamp()
    window_start = current_timestamp - window

    # Key for storing user's request timestamps
    key = f"rate_limit:{user_id}"

    async def cleanup_old_requests():
        """Remove requests older than the window"""
        redis_conn = await redis.get_connection()
        await redis_conn.zremrangebyscore(key, "-inf", window_start)

    async def add_request():
        """Add current request to the sorted set"""
        redis_conn = await redis.get_connection()
        pipeline = redis_conn.pipeline()
        pipeline.zadd(key, {str(current_timestamp): current_timestamp})
        pipeline.expire(key, window * 2)  # Set TTL for the key
        await pipeline.execute()

    async def get_request_count():
        """Get the number of requests in the current window"""
        redis_conn = await redis.get_connection()
        return await redis_conn.zcount(key, window_start, "+inf")

    # Execute rate limiting logic
    await cleanup_old_requests()
    await add_request()
    request_count = await get_request_count()

    return request_count <= limit


class RateLimiter:
    """Rate limiter class for more complex rate limiting scenarios"""

    def __init__(
        self,
        redis: RedisClient,
        prefix: str = "rate_limit",
        default_limit: int = 60,
        default_window: int = 60,
    ):
        self.redis = redis
        self.prefix = prefix
        self.default_limit = default_limit
        self.default_window = default_window

    async def is_allowed(self, key: str, limit: int = None, window: int = None) -> bool:
        """
        Check if the request is allowed based on rate limiting rules
        """
        limit = limit or self.default_limit
        window = window or self.default_window

        redis_key = f"{self.prefix}:{key}"
        current_time = datetime.utcnow().timestamp()

        # Get current count
        count = await self.redis.get(redis_key) or 0
        count = int(count)

        if count >= limit:
            return False

        # Increment count
        pipeline = await self.redis.get_connection()
        async with pipeline.pipeline() as pipe:
            await pipe.incr(redis_key)
            await pipe.expire(redis_key, window)
            await pipe.execute()

        return True

    async def get_remaining(self, key: str) -> int:
        """Get remaining requests allowed"""
        redis_key = f"{self.prefix}:{key}"
        count = await self.redis.get(redis_key) or 0
        return max(0, self.default_limit - int(count))

    async def reset(self, key: str) -> bool:
        """Reset rate limit counter for key"""
        redis_key = f"{self.prefix}:{key}"
        return await self.redis.delete(redis_key)


# Custom rate limiters for different scenarios
api_limiter = RateLimiter(
    redis=RedisClient(), prefix="api_rate_limit", default_limit=60, default_window=60
)

analysis_limiter = RateLimiter(
    redis=RedisClient(),
    prefix="analysis_rate_limit",
    default_limit=10,  # Lower limit for analysis requests
    default_window=60,
)

webhook_limiter = RateLimiter(
    redis=RedisClient(),
    prefix="webhook_rate_limit",
    default_limit=100,
    default_window=60,
)
