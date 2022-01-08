import json

from redis import Redis

from source.modules.common.redis_connection import get_redis
from source.modules.common.status_dict import StatusDict


def authenticate_user(form_data: dict):
    redis: Redis = get_redis()

    email = form_data.get("email", None)
    password = form_data.get("password", None)

    user_credentials = redis.hget("credentials", email).decode("UTF-8") if redis.hget("credentials",
                                                                                      email) is not None else None

    return user_credentials == password


def register_new_user(form_data: dict):
    redis: Redis = get_redis()

    email = form_data.get("email", None)
    password = form_data.get("password", None)
    repeat_password = form_data.get("repeat_password", None)

    login_exists = redis.hget("credentials", email).decode("UTF-8") if redis.hget("credentials",
                                                                                  email) is not None else None

    if password != repeat_password:
        return StatusDict.REPEAT_PASSWORD
    elif login_exists is not None:
        return StatusDict.LOGIN_EXISTS
    else:
        redis.hset("credentials", email, password)
        redis.hset("user_tokens", email, json.dumps([]))
        return StatusDict.ACCOUNT_CREATED
