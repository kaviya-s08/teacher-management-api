
import json
from fastapi.encoders import jsonable_encoder
from cache import redis_client

CACHE_KEY = "teachers:list"
CACHE_TTL = 300


def get_cached_teachers():
    cached_data = redis_client.get(CACHE_KEY)

    if cached_data:
        return json.loads(cached_data)

    return None


def set_cached_teachers(teachers):
    encoded_data = jsonable_encoder(teachers)

    redis_client.set(
        CACHE_KEY,
        json.dumps(encoded_data),
        ex=CACHE_TTL
    )


def clear_teacher_cache():
    redis_client.delete(CACHE_KEY)
