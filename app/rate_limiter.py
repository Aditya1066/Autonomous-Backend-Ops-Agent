import time
from fastapi import HTTPException

try:
    from app.cache import redis_client, CACHHE_AVAILABLE
except Exception:
    CACHE_AVAILABLE = False

_MEMORY_LIMITS = {}

def rate_limit(*, key:str, limit: str, window_seconds: int):
    current_window = int(time.time() // window_seconds)

    redis_key = f"rate:{key}:{current_window}"


    if CACHE_AVAILABLE:
        count = redis_client.incr(redis_key)

        if count == 1:
            redis_client.expire(redis_key, window_seconds)

        if count > limit:
            raise HTTPException(
                status_code=429,
                detail="Rate limit exceeded"
            )
        return

    bucket = _MEMORY_LIMITS.setdefault(redis_key, 0)
    _MEMORY_LIMITS[redis_key] += 1

    if _MEMORY_LIMITS[redis_key] > limit:
        raise HTTPException(
            status_code=429,
            detail="Rate limit exceeded"
        )