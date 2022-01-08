import os

from redis import Redis


def get_redis() -> Redis:
    redis_url = os.getenv("REDIS_URL")
    redis_port = os.getenv("REDIS_PORT")
    redis = Redis(host=redis_url, port=redis_port)
    return redis
