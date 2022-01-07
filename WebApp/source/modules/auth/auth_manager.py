from redis import Redis

from source.modules.common.redis_connection import get_redis


def authenticate_user(form_data: dict):
    redis: Redis = get_redis()

    login = form_data.get("login", None)
    password = form_data.get("password", None)

    user_credentials = redis.hget("credentials", login).decode("UTF-8") if redis.hget("credentials",
                                                                                      login) is not None else None

    return user_credentials == password
