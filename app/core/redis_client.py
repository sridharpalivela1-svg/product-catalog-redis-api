import redis
import json
from app.core.config import settings

try:
    redis_client = redis.Redis(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        decode_responses=True
    )
    redis_client.ping()
except Exception as e:
    print("Redis connection failed:", e)
    redis_client = None
