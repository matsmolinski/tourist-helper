import os

from redis import StrictRedis


def get_redis() -> StrictRedis:
    redis_url = os.getenv("REDIS_URL")
    redis_port = os.getenv("REDIS_PORT")
    redis_password = os.getenv("REDIS_PASSWORD")
    redis = StrictRedis(host=redis_url, port=redis_port, password=redis_password, ssl=True, db=0)
    return redis
