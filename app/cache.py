import redis
import json

try:
    redis_client = redis.Redis(
        host="localhost",
        port=6379,
        decode_responses=True
    )
    redis_client.ping()
    CACHE_AVAILABLE = True
except Exception:
    redis_client = None
    CACHE_AVAILABLE = False


def get_cached_status(user_id: int):
    if not CACHE_AVAILABLE:
        return None

    key = f"status:user:{user_id}"
    data = redis_client.get(key)
    if data:
        return json.loads(data)
    return None


def set_cached_status(user_id: int, data: list, ttl: int = 30):
    if not CACHE_AVAILABLE:
        return

    key = f"status:user:{user_id}"
    redis_client.setex(key, ttl, json.dumps(data))


def invalidate_status_cache(user_id: int):
    if not CACHE_AVAILABLE:
        return

    key = f"status:user:{user_id}"
    redis_client.delete(key)
